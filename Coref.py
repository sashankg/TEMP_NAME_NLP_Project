import os
from stanfordcorenlp import StanfordCoreNLP
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English
import sys
import json

pros = {'annotators': 'coref', 'pinelineLanguage': 'en', 'timeout': 500000}
nlp = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

"""
def readFileLines(path):
    with open(path, 'r') as f:
        return f.readlines()

def getParagraphs(path):
    text = [x for x in readFileLines(path)]
    return text
"""

def sentenize(tokens):
    puncts = [".", ",", ":", "!", "?", "-", "'", "-RRB-", "-LRB-"]
    final = []
    for sent in tokens:
        curr_sent = sent[0]
        for token in sent[1:]:
            if token not in puncts or token[0] not in puncts:
                curr_sent += " " + token
            else:
                if(token == "-RRB-"):
                    curr_sent += ")"
                elif(token == "-LRB-"):
                    curr_sent += "("
                else:
                    curr_sent += token
        final.append(curr_sent)
    return final

def getCoref(paragraphs):
    final = []
    possess = ["its", "her", "his", "their", "theirs", "hers", "his"]
    for i in range(0, len(paragraphs)):
        result_dict = json.loads(nlp.annotate(paragraphs[i], properties=pros))
        toChange = []

        for sent in result_dict["sentences"]:
            tokens = sent["tokens"]
            curr_sent = []
            for tok in tokens:
                curr_sent.append(tok["word"])
            toChange.append(curr_sent)

        for idx, mentions in result_dict['corefs'].items():
            curr_word = ""
            for m in mentions:
                if ((m["isRepresentativeMention"] and m["type"] != "PRONOMINAL")
                    or m["type"] == "PROPER"):
                    curr_word = m["text"]
                    break

            for m in mentions:
                pos = m["sentNum"]
                in_sent = m["headIndex"]
                if m["type"] == "PRONOMINAL":
                    temp = toChange[pos - 1][in_sent - 1]
                    toChange[pos - 1][in_sent - 1] = curr_word
                    if(temp in possess):
                        toChange[pos - 1][in_sent - 1] += "'s"

        new_sents = sentenize(toChange)
        print(final)
        final = final + new_sents
    return final


"""
def main():
    paragraphs = getParagraphs("./training_data/set1/a2.txt")
    #print(sentences)
    getCoref(paragraphs)



if __name__ == "__main__":
    main()
"""
