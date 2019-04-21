from nltk.stem.porter import *
import nltk
from fuzzywuzzy import fuzz
import sys
import spacy 
from spacy.lemmatizer import Lemmatizer

def main():
    doc_filename = sys.argv[1]
    question = sys.argv[2]

    doc_file = open(doc_filename, 'r', encoding="utf-8")

    doc = doc_file.read()

    sentences = nltk.sent_tokenize(doc)
    print(matching_sentence(doc, question))


def matching_sentence(document, question):
    sentences = nltk.sent_tokenize(document)
    max_ratio = 0
    closest_sentence = ""
    for s in sentences:
        r = fuzz.partial_ratio(question, s)
        if r > max_ratio:
            max_ratio = r
            closest_sentence = s
    return closest_sentence

if __name__ == '__main__':
    main()
