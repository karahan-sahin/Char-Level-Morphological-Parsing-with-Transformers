import enum
import re
import sys
from collections import defaultdict

def parser(file_name, output_name):

    ud_file = open(f'{file_name}','r',encoding='utf-8').read()

    REGEX_BLOCK = '(\# sent_id = (.+?)\n# text = (.+?)\n)((.|\n)+?)\n(?=# sent_id)'

    parses = re.findall(REGEX_BLOCK, ud_file)

    output = []

    pos_unique = set()

    for parse in parses:

        idx = parse[1]
        lines = parse[3].split('\n')

        sent = ""
        forms = []

        for line in lines[:-1]:
            tokens = line.split('\t')

            form = tokens[1]
            lemma = tokens[2]
            POS = tokens[3] # Can be 4
            features = tokens[5]

            pos_unique.add(POS)

            if lemma == "_":

                forms[-1] = forms[-1]+form
            else:
                forms.append(form)

            feature_find = '+'.join([i for i in features.split('|')])

            features = '+'.join([i for i in features.split('|')])

            if lemma == "_":
                sent += f"+{features}"
            else:
                if POS == "PUNCT":
                    sent += f" {form}+{POS}"
                else:
                    if features:
                        sent += f" {lemma}+{POS}+{features}"
                    else:
                        sent += f" {lemma}+{POS}"

        output.append((forms,sent.lstrip().split(),idx))
        
    with open(f"{output_name}.txt","w+",encoding='utf-8') as f_out:
        for f,t,idx in output:
            for i,j in zip(f,t):
                f_out.write(f"{i}\t{j}\t{idx}\n")


parser("/home/kara/Documents/Courses/Fall 2021/LING412 - RESEARCH & WRITING/Data/turkish-treebanks/data/web.conllu",
       "/home/kara/Documents/Courses/Fall 2021/LING412 - RESEARCH & WRITING/Datasets/Phonological/web_data")

ud_file = open("/home/kara/Documents/Courses/Fall 2021/LING412 - RESEARCH & WRITING/Data/turkish-treebanks/data/wiki.conllu",'r',encoding='utf-8').read()

def parse_sentences(ud_file):
    REGEX_BLOCK = '(\# sent_id = (.+?)\n# text = (.+?)\n)((.|\n)+?)\n(?=# sent_id)'

    parses = re.findall(REGEX_BLOCK, ud_file)

    output = []

    pos_unique = set()

    for parse in parses:
        idx = parse[1]
        lines = parse[3].split('\n')

        sent = ""
        forms = []

        for line in lines[:-1]:
            tokens = line.split('\t')

            form = tokens[1]
            lemma = tokens[2]
            POS = tokens[3] # Can be 4
            features = tokens[5]

            pos_unique.add(POS)

            if lemma == "_":

                forms[-1] = forms[-1]+form
            else:
                forms.append(form)

            feature_find = '+'.join([i for i in features.split('|')])

            features = '+'.join([i for i in features.split('|')])

            if lemma == "_":
                sent += f"+{features}"
            else:
                if POS == "PUNCT":
                    sent += f" {form}+{POS}"
                else:
                    if features:
                        sent += f" {lemma}+{POS}+{features}"
                    else:
                        sent += f" {lemma}+{POS}"

        output.append((" ".join(forms),idx))
        
    with open(f"/home/kara/Documents/Courses/Fall 2021/LING412 - RESEARCH & WRITING/Datasets/Phonological/wiki_sentences.txt","w+",encoding='utf-8') as f_out:
        for sent,idx in output:
            f_out.write(f"{sent}\t{idx}\n")


# for idx, parse in enumerate(parses):
#     output.append((forms,sent.lstrip().split(),idx))