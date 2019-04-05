#!/usr/bin/python

import os
import spacy
from spacy import displacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import sys

nlp = spacy.load("en_core_web_sm")
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

def is_tense(tag):
    return tag in ['VBD', 'VBZ', 'VBP']

def is_plural(tag):
  return tag.endswith('S')

def is_verb(tag):
  return tag.startswith('V') or label == 'MD'

def is_noun(tag):
  return tag.startswith('NN')

def is_adjective(tag):
  return tag.startswith('JJ')

def connect_conj(chunk):
    fin = chunk.text
    conjs = chunk.conjuncts
    if(conjs):
        if(len(conjs) > 1):
            for word in conjs[0:len(conjs) - 1]:
                fin += (", " + word.text)
        fin += (" and " + conjs[len(conjs) - 1].text)
    return fin

def get_base(token):
    keep = ["is", "was", "are"]
    if token.text in keep:
        return token.text
    return lemmatizer(token.text, token.pos_)[0]

def create_question(doc):
    head = ""
    aux = ""
    chunk_text = ""
    ag = ""
    xc = ""
    lefts = []
    past = False;
    agent = False;
    xcomp = False

    for token in doc:
        if token.dep_ == "ROOT":
            head = get_base(token)
            past = is_tense(token.pos_)
            lefts= [t.text for t in token.lefts]
            for child in token.lefts:
                if child.dep_ == "neg":
                    head = child.text + " " + head
                if child.pos_ == "ADP" and child.dep_ == "agent":
                    agent = True
                    ag = child.text
                if child.pos_ == "VERB" and (child.dep_ in ["aux", "auxpass"]):
                    aux = child.text;
            for child in token.rights:
                if child.dep_ in ["xcomp", "acomp"]:
                    xcomp = True
                    if child.nbor(-1).dep_ == "aux":
                        xc = child.nbor(-1).text + " " + child.text
                    else:
                        xc = child.text


    for chunk in doc.noun_chunks:
        print(chunk.text + " is a " + chunk.root.dep_)
        #print(chunk.root.conjuncts)
        if((chunk.root.dep_ == "nsubj" or chunk.root.dep_ == "nsubjpass")
            and chunk.root.text != "it" and chunk.root.text in lefts):
            chunk_text = connect_conj(chunk)

    if head in ["is", "was", "are"]:
        final_question = "What "+head+" "+chunk_text.strip()
        if xcomp:
            final_question += (" " + xc)
        print(final_question+"?")


    else:
        final_question = "What "
        if aux != "":
            final_question += (aux + " ")
        else:
            final_question += ("do ")
        final_question += (chunk_text.strip() + " " + head)
        if agent:
            final_question += (" " + ag)
        if xcomp:
            final_question += (" " + xc)
        final_question += "?"
        print(final_question)

def main():
    file = sys.argv[1]
    f = open("./tests/set5/"+file, "r")
    text = []
    for line in f:
        temp = line.split(".")
        for sentence in temp:
            if sentence != "\n":
                text.append(sentence)
    f.close()

    for line in text:
        print("\n\n")
        doc = nlp(line)
        print(doc.text)
        create_question(doc)


if __name__ == "__main__":
    main()
