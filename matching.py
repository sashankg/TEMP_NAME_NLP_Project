from nltk.stem.porter import *
import nltk
from fuzzywuzzy import fuzz
import sys
import spacy 
from spacy.lemmatizer import Lemmatizer

nlp = spacy.load('en_core_wb_lg')

def main():
    doc_filename = sys.argv[1]
    question = sys.argv[2]

    doc_file = open(doc_filename, 'r', encoding="utf-8")

    doc = doc_file.read()

    sentences = nltk.sent_tokenize(doc)
    print(matching_sentence(doc, question))


def matching_sentence(document, question):
    q = nlp(question)
    keywords = [x for x in q if not x.is_stop]
    print(keywords)
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
