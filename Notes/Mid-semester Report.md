# Mid-Semester Report

## Index

[TOC]

## Dataset

### Data Statistics

| Data          | Count |
| ------------- | ----- |
| Wiki Token    | 39932 |
| Web Token     | 26508 |
| Wiki Sentence | 2310  |
| Web Sentence  | 2541  |

| POS Tag |       |
| ------- | ----- |
| NOUN    | 28973 |
| VERB    | 11755 |
| PUNCT   | 9048  |
| ADJ     | 2943  |
| ADP     | 2761  |
| CONJ    | 2672  |
| DET     | 2421  |
| ADV     | 1591  |
| PRT     | 1004  |

### Feature Distribution

- Initial Random distribution

- NOUN category dominates and functions as in dump category

- 80:10:10 Feature Distr

- 80:10:10 with Phonological Normalization

- > **The major problem is the distribution of feature since it is not diverse as the random test set**
  >
  > - The distribution of train and test sets of distributions of other should be further demonstrated
  > - The scores are dropping drastically
  > - Should the models used in this dataset

### Feature Normalization

- I have turned semantic features into different POS tags 

  - ADP+ComplementType=? -> ADP^ComplementType
    - This token is due to the previous tokens Case, there should be a separate token
  - PRON+PronType=? -> PRON^PronType
  - ConjunctionType
    - `re.sub("CONJ\+ConjunctionType=","",decode)`

- Multiple Polarity around Derivation=Able as

  - ```
    atabiliyor:	at+VERB+*Polarity=Pos*+Derivation=Able+Polarity=Pos+TenseAspectMood=Prog1+Copula=PresCop+PersonNumber=V3sg
    to
    at+VERB+Derivation=Able+Polarity=Pos+TenseAspectMood=Prog1+Copula=PresCop+PersonNumber=V3sg
    ```

  - Capabiility vs possibility --> subsampling

    - Scope general --> disambiguation
    - Modality disambiguatior (Case Study)

  - To further demonstrate overt morphology

- Should extra feature further eliminated

  - Case=Bare before the derivation the derivation

- > Main reason why I do this is to capture **overt morphology** which more features can create **a noise to the model**

- Proper=True+ ..
  - Proper=True within the morphology
  - Ali - siz
  - `re.sub("Proper=True+", "", decode)`
  
- Case=Bare within the morphology
  - While `Case=Loc` can be within the lemma
  - `Case=(?<!Bare)+?\+(?<!Proper=True)`
    - Talk these cases
    - kitap(Case=Nom) - tır
    - 
  - Bare case has no overt usE
  
- `Possessive=Pnon` also null 

  - **Generally null features are redundant**
  - This is a one way of

- A3sg vs V3pl

- `üyelArIYdI	üye+VERB+PersonNumber=A3pl+Possessive=P3sg+Case=Bare+Copula=PastCop+PersonNumber=V3pl`
  
  - POS!!!! --> lemma pos or token pos
  - PersonNumber --> Nominal pred
    - üye**leri**ydi **V3pl is null**
    - *güzeller-di-ler
    - kitaplar-dır vs kitaplarım-dı vs *kitaplarım-dır 
    - also an error
    - Also nullness hypothesis

### Phonological Normalization

- Mostly done however cannot decide on the lemma alternation
  - kitap -> kitab-ı??
- lemma[-1] `d->t ,ğ->k, `
- Rfx passfix

### Model 

- **Since embeddings are learned, it vocab size might cause under fitting** 
- Model is a Transformers architecture with the default hyper-parameters

| Parameter                   | Value                          |
| --------------------------- | ------------------------------ |
| Vocab Size                  | **322 (Dataset char + feats)** |
| Sequence Length             | 20                             |
| Embedding Dimensions        | 256                            |
| Latent Dimensions           | 2048                           |
| Number of (Attention) Heads | 8                              |
| Batch Size                  | 64                             |
| Epoch                       | 5                              |

- Sequence Length at max(wiki_token_length,web_token_length)
- I use Epoch at 5 since I saw that Epoch > 10 (Overfitting)
- **Random seed added to the distribution**

## Evaluation

### Metrics

- Partial Match: Calculates in terms of subset of common features
- Exact Match: Literal string Match of sequences
  - 0.1 ~ 0.2
- BLEU Score: Feature-wise edit distance between y_pred and y_true
- Further Analysis
  - edit_distance(lemma_pred vs lemma_true)
  - precision, recall of POS tagging

|                                | Par-Pre   | Par-Rec   | BLEU  | POS  | Lemma |
| ------------------------------ | --------- | --------- | ----- | ---- | ----- |
| Baseline (Random - Token)      | 0.763     | 0.774     | 0.77  |      |       |
| Feature Distribution           | 0.35      | 0.35      |       |      |       |
| Random Dist with Normalization | **0.825** | **0.805** | 0.827 |      | 0.955 |
| Feat Dist with Normalization   | 0.645     | 0.645     | 0.62  | 0.32 |       |
| Context Embedding (TO-DO)      |           |           |       |      |       |
| **Upsampling**                 | 0.757     | 0.743     | 0.808 | 0.82 |       |
|                                |           |           |       |      |       |

- Upsampling is done with **Epoch=2**

```
için-de-ki
cas=loc
isim-Case=Bare-siz
```

#### POS Scores - Bset

```
              precision    recall  f1-score   support

           0       0.00      0.00      0.00       164
           1       0.00      0.00      0.00        36
         ADJ       0.71      0.45      0.55       433
         ADV       0.65      0.47      0.55       231
        CONJ       0.88      0.94      0.90       376
         DET       0.13      0.15      0.14        47
        NOUN       0.85      0.96      0.90      4318
         NUM       0.90      0.96      0.93       233
        ONOM       0.00      0.00      0.00         4
        PRON       0.89      0.35      0.51       192
         PRT       0.92      0.91      0.92       139
       PUNCT       0.99      1.00      1.00      1342
        VERB       0.94      0.91      0.93      1714
           X       0.77      0.43      0.55        63

    accuracy                           0.88      9292
   macro avg       0.62      0.54      0.56      9292
weighted avg       0.86      0.88      0.86      9292
```

### TODO:

- ERROR ANALYSIS
- FURTHER FEATURE ELIMINATION
  - MODEL AMB
- 
- CONTEXT EMBEDDING

Context Information

- `gelmIş	gel+VERB+Polarity=Pos+TenseAspectMood=Nar+Copula=PresCop+PersonNumber=V3sg`
- `şu+NOUN+PersonNumber=A3sg+Possessive=Pnon+Case=Bare	şu+DET+DeterminerType=Dem
  yer+NOUN+PersonNumber=A3pl+Possessive=Pnon+Case=Loc	yer+NOUN+PersonNumber=A3pl+Possessive=Pnon+Case=Loc`
- Proper=True
- NOUN vs ADJ



## Case Based Example

- Acc vs Possessive

