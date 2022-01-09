import enum
import re
import sys
from collections import defaultdict

def parser(file_names, output_name):

    output = []

    for file_name in file_names:

        ud_file = open(f'{file_name}','r',encoding='utf-8').read()

        REGEX_BLOCK = '(\# sent_id = (.+?)\n# text = (.+?)\n)((.|\n)+?)\n(?=# sent_id)'

        parses = re.findall(REGEX_BLOCK, ud_file)    

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

                print(line)

                if lemma == "_":

                    forms[-1] = forms[-1]+form
                else:
                    forms.append(form)

                feature_find = '+'.join([i for i in features.split('|')])

                features = '+'.join([i for i in features.split('|')])

                if lemma == "_":
                    sent += f"DB^{POS}+{features}"
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



# parser(["Datasets/Usable/web.conllu","Datasets/Usable/wiki.conllu"],
#         "parse_dataset")


def parse_sentences(file_names, output_name):

    output = []

    for file_name in file_names:

        print(file_name)

        ud_file = open(f'{file_name}','r',encoding='utf-8').read()
        REGEX_BLOCK = '(\# sent_id = (.+?)\n# text = (.+?)\n)((.|\n)+?)\n(?=# sent_id)'

        parses = re.findall(REGEX_BLOCK, ud_file)

        for parse in parses:

            output.append((parse[2],parse[1]))
            
        
    with open(f"{output_name}","w+",encoding='utf-8') as f_out:
        for sent,idx in output:
            f_out.write(f"{sent}\t{idx}\n")


parse_sentences(["Datasets/Usable/web.conllu","Datasets/Usable/wiki.conllu"],
         "parse_sentences")
