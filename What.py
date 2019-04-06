import os
import spacy
from spacy import displacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES
import sys

nlp = spacy.load("en_core_web_sm")
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

def is_tense(tag):
    return tag in ['VBD', 'VBZ', 'VBP', 'VBN']

def is_plural(tag):
  return tag.endswith('S')

def is_verb(tag):
  return tag.startswith('V') or label == 'MD'

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

def what(sent):
    doc = nlp(sent)
    head = ""
    aux = ""
    chunk_text = ""
    agent = ""
    xcomp = ""
    past = False
    lefts = []

    for token in doc:
        if token.dep_ == "ROOT":
            head = get_base(token)
            if token.nbor(1).dep_ == "prep":
                head += (" " + token.nbor(1).text)
            past = is_tense(token.tag_)
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
        if((chunk.root.dep_ == "nsubj" or chunk.root.dep_ == "nsubjpass")
            and chunk.root.text != "it" and chunk.root.text in lefts):
            chunk_text = connect_conj(chunk)

    if head in ["is", "was", "are"]:
        final_question = "What "+head+" "+chunk_text.strip()
        if xcomp:
            final_question += (" " + xcomp)

    else:
        final_question = "What "
        if aux:
            final_question += (aux + " ")
        else:
            if past:
                final_question += ("did ")
            else:
                final_question += ("do ")
        final_question += (chunk_text.strip() + " " + head)
        if agent:
            final_question += (" " + agent)
        if xcomp:
            final_question += (" " + xcomp)
        final_question += "?"
    return (final_question)
