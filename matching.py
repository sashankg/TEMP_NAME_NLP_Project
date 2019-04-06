from nltk.stem.porter import *
import nltk
from fuzzywuzzy import fuzz
import sys


doc_filename = sys.argv[1]
question = sys.argv[2]

doc_file = open(doc_filename, 'r', encoding="utf-8")

doc = doc_file.read()

sentences = nltk.sent_tokenize(doc)

max_ratio = 0
closest_sentence = ""

stemmer = PorterStemmer()

for s in sentences:
    r = fuzz.ratio(s, question)
    if r > max_ratio:
        max_ratio = r
        closest_sentence = s

print(question)

print(closest_sentence)