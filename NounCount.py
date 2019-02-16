#!/usr/bin/python

import os
import nltk
import sys

def countNouns(sentence):
    tokens = nltk.word_tokenize(sentence)
    tagged = nltk.pos_tag(tokens)
    tags = ['PRP', 'PRP$', 'WP', 'WP$', 'NN', 'NNS', 'NNP', 'NNPS']
    #print(tags)
    #print('WP' in tags)
    #print([x[1] for x in tagged])

    #filter out the words with noun tags
    nounList = list(filter(lambda x: x[1] in tags, tagged))
    #print(nounList)
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
