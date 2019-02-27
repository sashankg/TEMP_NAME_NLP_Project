#!/usr/bin/python

import os
import nltk
import sys

def countNouns(sentence):
    tokens = nltk.word_tokenize(sentence)
    #print(tokens)
    tagged = nltk.pos_tag(tokens)
    tags = ['PRP', 'PRP$', 'WP', 'WP$', 'NN', 'NNS', 'NNP', 'NNPS']
    #print(tags)
    #print('WP' in tags)
    nounList = []
    tag_len = len(tagged)
    for tag_word in range(0, tag_len):
        tag = tagged[tag_word]
        noun_len = len(nounList)
        #print(tag)
        if tag[1] == "NNP" and tagged[tag_word - 1][1] == "NNP" and noun_len > 0:
            #print(nounList[len(nounList) - 1][0])
            #print(tag[0])
            temp = nounList[noun_len - 1][0] + " " +tag[0]
            #print(temp)
            nounList[noun_len - 1] = (temp, "NNP")
        elif tag[1] in tags:
            nounList.append(tag)

    #print('\n')
    #print('\n')
    #print(nounList)
    return len(nounList)

def main():
    #file = sys.argv[1]
    #f = open("./tests/"+file, "r")
    for i in range(1, 11):
        f = open("./tests/a"+ str(i) + ".txt", "r")
        totalCount = 0
        for line in f:
            line.rstrip('\n')
            totalCount += countNouns(line)
        f.close()
        print(totalCount)

if __name__ == "__main__":
    main()
