#!/usr/bin/python

import os
import spacy
from spacy import displacy
import sys

nlp = spacy.load("en_core_web_sm")

def main():
    file = sys.argv[1]
    f = open("./tests/set5/"+file, "r")
    text = []
    for line in f:
        line.rstrip('\n')
        temp = line.split(".")
        text += temp
    f.close()

    for line in text:
        print("\n\n")
        doc = nlp(line)
        print(doc.text)

        head = ""
        aux = ""
        chunk_text = ""
        ag = ""
        lefts = []
        past = False;
        agent = False;

        for token in doc:
            if token.dep_ == "ROOT":
                head = token.text
                lefts= [t.text for t in token.lefts]
                for child in token.children:
                    if child.pos_ == "ADP" and child.dep_ == "agent":
                        agent = True
                        ag = child.text
                    if child.pos_ == "VERB" and (child.dep_ in ["aux", "auxpass"]):
                        aux = child.text;

        for chunk in doc.noun_chunks:
            print(chunk.text + " is a " + chunk.root.dep_)
            if((chunk.root.dep_ == "nsubj" or chunk.root.dep_ == "nsubjpass")
                and chunk.root.text != "it" and chunk.root.text in lefts):
                chunk_text = chunk.text

        if aux != "" and agent:
            print("What " + aux + " " + chunk_text.strip() +  " " + head + " "+ ag + "?")
        elif agent:
            print("What " + chunk_text.strip() +  " " + head + " " + ad + "?")
        elif head != "" and chunk_text != "":
            print("What did " + chunk_text.strip() +" "+head + "?")



if __name__ == "__main__":
    main()
