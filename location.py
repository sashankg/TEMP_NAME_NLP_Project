import nltk
import spacy
import sys
from BinQ import getVP, parser, getBinQ, leftmost, sentences

parser.tagtype = 'ner'
l = list(parser.tag(('Rami Eid is studying at Stony Brook University in NY'.split())))
print(l)