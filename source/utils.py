import pickle
import numpy as np

import tensorflow as tf
from tensorflow.keras.layers import TextVectorization


vocab_size = 15000
sequence_length = 20
batch_size = 64


def custom_standardization_raw(input_string):
    return tf.strings.lower(input_string)

def custom_standardization_morph(input_string):
    return input_string

def InputVectorizer(train_pairs):
    
    raw_vectorization = TextVectorization(
        max_tokens=vocab_size, 
        output_mode="int", 
        output_sequence_length=sequence_length, 
        standardize=custom_standardization_raw
    )
    morph_vectorization = TextVectorization(
        standardize=custom_standardization_morph,
        max_tokens=vocab_size,
        output_mode="int",
        output_sequence_length=sequence_length + 1,
    )

    train_raw_texts = [pair[0] for pair in train_pairs]
    train_morph_texts = [pair[1] for pair in train_pairs]

    raw_vectorization.adapt(train_raw_texts)
    morph_vectorization.adapt(train_morph_texts)

    pickle.dump({'config': raw_vectorization.get_config(),
             'weights': raw_vectorization.get_weights()}
            , open("raw_vectorizator.pkl", "wb"))

    pickle.dump({'config': morph_vectorization.get_config(),
             'weights': morph_vectorization.get_weights()}
            , open("morph_vectorizator.pkl", "wb"))

    return raw_vectorization, morph_vectorization

def import_vectorization(raw_object_source='raw_vectorizator.pkl', 
                         morph_object_source='morph_vectorizator.pkl'):

    from_disk = pickle.load(open("raw_vectorizator.pkl", "rb"))
    raw_vectorization = TextVectorization(output_sequence_length=20).from_config(from_disk['config'])
    raw_vectorization.adapt(tf.data.Dataset.from_tensor_slices(["k a l e m l e r"]))
    raw_vectorization.set_weights(from_disk['weights'])

    from_disk = pickle.load(open("morph_vectorizator.pkl", "rb"))
    morph_vectorization = TextVectorization(output_sequence_length=20).from_config(from_disk['config'])
    morph_vectorization.adapt(tf.data.Dataset.from_tensor_slices(["k a l e m [PersonNumber=A3pl]"]))
    morph_vectorization.set_weights(from_disk['weights'])

    return raw_vectorization, morph_vectorization

raw_vectorization, morph_vectorization = import_vectorization()

def format_dataset(raw, morph):

    raw = raw_vectorization(raw)
    morph = morph_vectorization(morph)

    return ({"encoder_inputs": raw, "decoder_inputs": morph[:, :-1],}, morph[:, 1:])

def make_dataset(pairs):

    raw_texts, morph_texts = zip(*pairs)
    raw_texts = list(raw_texts)
    morph_texts = list(morph_texts)
    dataset = tf.data.Dataset.from_tensor_slices((raw_texts, morph_texts))
    dataset = dataset.batch(batch_size)
    dataset = dataset.map(format_dataset)
    return dataset.shuffle(2048).prefetch(16).cache()


def decode_sequence(input_sentence,
                    model,
                    raw_vectorization,
                    morph_vectorization):
    """
    
    """
    raw_vectorization, morph_vectorization = import_vectorization()

    morph_vocab = morph_vectorization.get_vocabulary()
    morph_index_lookup = dict(zip(range(len(morph_vocab)), morph_vocab))
    max_decoded_sentence_length = 20

    tokenized_input_sentence = raw_vectorization([input_sentence])
    decoded_sentence = "[start]"
    for i in range(max_decoded_sentence_length):
        tokenized_target_sentence = morph_vectorization([decoded_sentence])[:, :-1]
        predictions = model([tokenized_input_sentence, tokenized_target_sentence])

        sampled_token_index = np.argmax(predictions[0, i, :])
        sampled_token = morph_index_lookup[sampled_token_index]
        decoded_sentence += " " + sampled_token

        if sampled_token == "[end]":
            break

    return decoded_sentence

def normalize(input):
    """
    
    """

    pos_unique = ['X', 
                  'PUNCT', 
                  'ADP', 
                  'NUM', 
                  'ADV', 
                  'PRON', 
                  'NOUN', 
                  'ADJ', 
                  'AFFIX',
                  'DET',
                  'ONOM',
                  'CONJ',
                  'VERB',
                  'PRT']

    pre = ""
    feats = ""
    tokens = input.split()
    match = False

    for idx,token in enumerate(tokens[0:-1]):
        if token in pos_unique and not match:
            pre += "".join(tokens[0:idx])+"["+token+"]"
            match=True
        elif match:
            feats += "["+token+"]"
    return pre+feats






