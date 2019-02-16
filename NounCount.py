#!/usr/bin/python

import os
import nltk
import sys

def countNouns(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    tags = ['NN', 'NNS', 'NNP', 'NNPS', 'PRP', 'WP', 'WP$']
    #print(tagged)
    nounList = list(filter(lambda x: x[1] in tags, tagged))
    print(nounList)
    return len(nounList)

def main():
    file = sys.argv[1]
    f = open("./tests/"+file, "r")
    s = ""
    for line in f:
        s += line + " "
    f.close()
    print(countNouns(s))

if __name__ == "__main__":
    main()
