import os
import spacy
from spacy import displacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English
import sys

nlp = spacy.load("en")
lemmatizer = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

"""
def readFileLines(path):
    with open(path, 'r') as f:
        return f.readlines()
def writeFile(path, contents):
    with open(path, 'w') as f:
        f.write(contents)

def getSentences(path):
    text = [x.strip() for x in readFileLines(path)]
    nl = English()
    nl.add_pipe(nlp.create_pipe('sentencizer'))
    sentences = []
    for txtline in text:
        if len(txtline) < 30:
            continue
        sentences += [str(sent) for sent in nl(txtline).sents]
    return sentences
"""

def is_tense(tag):
    return tag in ['VBD', 'VBZ', 'VBP', 'VBN']

def is_plural(tag):
  return tag.endswith('S')

def is_verb(tag):
  return tag.startswith('V') or label == 'MD'

def connect_conj(chunk):
    fin = ""
    if(chunk[0].tag_ not in  ["PROPN", "NNS"]):
        fin += chunk[0].text.lower() + " "
    else:
        fin += chunk[0].text + " "
    fin += chunk[1:].text
    conjs = chunk.conjuncts
    if(conjs):
        if(len(conjs) > 1):
            for word in conjs[0:len(conjs) - 1]:
                fin += (", " + word.text)
        fin += (" and " + conjs[len(conjs) - 1].text)
    return fin

def get_prep(prep):
    fin = prep.text.lower()
    prep = prep.nbor(1)
    while(prep.dep_ not in ["pobj", "dobj", "attr", "punct"]):
        fin += " " + prep.text
        prep = prep.nbor(1)
    if(prep.dep != "punct"):
        fin += " " + prep.text
    return fin

def get_base(token):
    keep = ["is", "was", "are"]
    if token.text in keep:
        return token.text
    return lemmatizer(token.text, token.pos_)[0]

def what(sent):
    doc = nlp(sent)
    head = ""
    aux = []
    chunk_text = ""
    agent = ""
    xcomp = ""
    prep = ""
    obj = ""
    past = False
    lefts = []

    for token in doc:
        if token.dep_ == "ROOT":
            head = get_base(token)
            try:
                if token.nbor(1).dep_ == "prep":
                    head += (" " + token.nbor(1).text)
                elif token.nbor(1).dep_ in ["dobj", "pobj", "attr"]:
                    obj += token.nbor(1).text
            except:
                pass

            first = True
            past = is_tense(token.tag_)
            lefts= [t.text for t in token.lefts]
            for child in token.lefts:
                if child.dep_ == "neg":
                    head = child.text + " " + head
                if child.pos_ == "VERB" and (child.dep_ in ["aux", "auxpass"]):
                    aux.append(child.text);
                if child.dep_ == "prep":
                    prep = get_prep(child)

            for child in token.rights:
                if child.dep_ in ["xcomp", "acomp"]:
                    for gchild in child.lefts:
                        if gchild.dep_ == "aux":
                            xcomp = gchild.text + " "
                            break
                    for gchild in child.rights:
                        if gchild.dep_ == "prep":
                            xcomp += gchild.text + " "
                    xcomp += child.text
                if child.pos_ == "ADP" and child.dep_ == "agent":
                    agent = child.text
                if child.dep_ == "prep" and not first:
                    first = False
                    head += (" " + child.text)

    for chunk in doc.noun_chunks:
        if((chunk.root.dep_ == "nsubj" or chunk.root.dep_ == "nsubjpass")
            and chunk.root.text != "it" and chunk.root.text in lefts):
            chunk_text = connect_conj(chunk)

    if head in ["is", "was", "are"] and chunk_text != "":
        final_question = "What "+head+" "+chunk_text.strip()
        if xcomp:
            final_question += (" " + xcomp)
        final_question += "?"

    else:
        final_question = ""
        if(head != "" and chunk_text != ""):
            final_question = "What "
            if len(aux) == 1:
                final_question += (aux[0] + " ")
                final_question += (chunk_text.strip() + " " + head)
            elif len(aux) == 2:
                final_question += (aux[0] + " ")
                final_question += (chunk_text.strip() + " " + aux[1] + " " + head)
            else:
                if past:
                    final_question += ("did ")
                else:
                    final_question += ("do ")
                final_question += (chunk_text.strip() + " " + head)
            if obj:
                final_question += (" " + obj)
            if agent:
                final_question += (" " + agent)
            if xcomp:
                final_question += (" " + xcomp)
            if prep:
                final_question += (" " + prep)
            final_question += "?"
    if(final_question == ""):
        return None

    return (final_question)

"""
def main():
    sents = getSentences("./training_data/set2/a3.txt")
    for sent in sents:
        temp = what(sent)
        if temp != None:
            print(what(sent))

if __name__ == "__main__":
    main()
"""
