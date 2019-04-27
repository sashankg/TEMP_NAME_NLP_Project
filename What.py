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
    return tag in ['VBD','VBN']

def is_plural(tag):
  return tag.endswith('S')

def is_verb(tag):
  return tag.startswith('V') or label == 'MD'

def connect_conj(chunk):
    fin = ""
    temp = ""
    first_tag = ""
    try:
        first_tag = chunk[0].nbor(-1)
    except:
        pass
    if(first_tag):
        if chunk[0].nbor(-1).tag_ in ["npadvmod", "nmod"]:
            fin = chunk[0].nbor(-1).text + " "
    if(chunk[0].tag_ not in  ["PROPN", "NNS"]):
        fin += chunk[0].text.lower() + " "
    else:
        fin += chunk[0].text + " "
    fin += chunk[1:].text
    conjs = chunk.conjuncts
    cs = ""
    if(conjs):
        if(len(conjs) > 1):
            for word in conjs[0:len(conjs) - 1]:
                fin += (", " + word.text)
        fin += (" and " + conjs[len(conjs) - 1].text)
        cs = conjs[len(conjs) - 1].nbor(1)
    else:
        cs = chunk[len(chunk) - 1].nbor(1)
    if(cs.dep_ == "prep"):
        temp = get_prep(cs)
    if(temp != ""):
        fin += " " + temp
    return fin

def get_prep(prep):
    fin = ""
    while(prep.dep_ not in ["pobj", "dobj", "attr", "punct"]):
        fin += prep.text.lower() + " "
        temp = [p for p in prep.rights]
        if(temp != []):
            prep = temp[0]
        else:
            prep = prep.nbor(1)
        if(prep.dep_ in ["nsubj", "nsubjpass"]):
            break
        if(prep.dep_ in ["pobj", "dobj", "attr", "punct"]):
            for temp_pre in prep.lefts:
                if(temp_pre.dep_ in ["aux", "auxpass", "det", "amod", "compound"]):
                    fin += temp_pre.text + " "
            temp = [p for p in prep.rights]
            temp_prep = None
            if(temp != []):
                temp_prep = temp[0]
            try:
                temp_prep = prep.nbor(1)
            except:
                pass
            if(not (temp_prep == None)):
                if prep.text == "," and temp_prep.dep_ in ["nummod", "appos"]:
                    fin += prep.text + " " + temp_prep.text
                elif temp_prep.dep_ in ["prep", "cc", "nummod", "appos", "acl"]:
                    fin += prep.text + " "
                    prep = temp_prep
    if(prep.dep_ not in ["punct", "nsubj", "nsubjpass"]):
        fin += prep.text
    return fin.strip()

def get_base(token):
    keep = ["is", "was", "are"]
    if token.text in keep:
        return token.text
    return lemmatizer(token.text, token.pos_)[0]

auxs = ["were", "was", "has", "have", "are", "would", "could"]

def what(sent):
    doc = nlp(sent)
    head = ""
    aux = []
    chunk_text = ""
    agent = ""
    xcomp = ""
    prep = ""
    obj = ""
    prep = ""
    prep2 = ""
    past = False
    lefts = []
    neg = ""

    for token in doc:
        if token.dep_ == "ROOT":
            head = token
            try:
                if token.nbor(1).dep_ in ["dobj", "pobj"]:
                    obj += token.nbor(1).text
                    if(token.nbor(2).dep_ == "prep"):
                        obj += " " + token.nbor(2).text
            except:
                pass

            first = True
            past = is_tense(token.tag_)
            lefts= [t.text for t in token.lefts]
            for child in token.lefts:
                if child.dep_ == "neg":
                    neg = child.text
                if child.pos_ == "VERB" and (child.dep_ in ["aux", "auxpass"]):
                    aux.append(child.text);
                if child.dep_ == "prep":
                    prep = get_prep(child)

            for child in token.rights:
                if child.dep_ in ["xcomp", "acomp"]:
                    temp = ""
                    aux_ex = False
                    gch_prep = False
                    for gchild in child.lefts:
                        if gchild.dep_ == "aux":
                            aux_ex = True
                            xcomp = gchild.text + " "
                            break
                    for gchild in child.rights:
                        if gchild.dep_ in ["acomp", "xcomp"]:
                            if(gchild.nbor(-1).dep_ in ["aux", "auxpass"]):
                                xcomp += gchild.nbor(-1).text + " " + gchild.text + " "
                        if gchild.dep_ == "prep":
                            xcomp += child.text + " " + gchild.text
                            gch_prep = True
                    if(aux_ex):
                        xcomp += "do"
                    elif not gch_prep:
                        xcomp += child.text
                    if temp != "":
                        xcomp += " " + temp
                if child.pos_ == "ADP" and child.dep_ == "agent":
                    first = False
                    agent = child.text

                if child.dep_ == "prep" and first:
                    first = False
                    prep2 = child.text

    for chunk in doc.noun_chunks:
        if((chunk.root.dep_ == "nsubj" or chunk.root.dep_ == "nsubjpass")
            and chunk.root.text != "it" and chunk.root.text in lefts):
            chunk_text = connect_conj(chunk)

    if head.text in ["is", "was", "are"] and chunk_text != "":
        final_question = "What "+ head.text + " " +chunk_text.strip()
        if xcomp:
            final_question += (" " + xcomp)
        final_question += "?"

    else:
        final_question = ""
        if(head.text != "" and chunk_text != ""):
            final_question = "What "
            if len(aux) == 1:
                final_question += (aux[0] + " ")
                if(aux[0] in auxs):
                    if neg:
                        final_question += (chunk_text.strip() + " " + neg + " " + (head.text))
                    else:
                        final_question += (chunk_text.strip() + " " + (head.text))
                else:
                    if neg:
                        final_question += (chunk_text.strip() + " " + neg + " " + get_base(head))
                    else:
                        final_question += (chunk_text.strip() + " " + get_base(head))
            elif len(aux) == 2:
                final_question += (aux[0] + " ")
                if(aux[0] in auxs):
                    if neg:
                        final_question += (chunk_text.strip() + " " + aux[1] + " " + neg + " " + (head.text))
                    else:
                        final_question += (chunk_text.strip() + " " + aux[1] + " " + (head.text))
                else:
                    if neg:
                        final_question += (chunk_text.strip() + " " + aux[1] + " " +  neg + " " + get_base(head))
                    else:
                        final_question += (chunk_text.strip() + " " + aux[1] + " " + get_base(head))
            else:
                if past:
                    final_question += ("did ")
                elif not is_plural(head.tag_):
                    final_question += ("does ")
                else:
                    final_question += ("do ")
                if(neg):
                    final_question += (chunk_text.strip() + " " + neg + " " + get_base(head))
                else:
                    final_question += (chunk_text.strip() + " " +get_base(head))
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
    for i in range(1, 6):
        for j in range(1, 11):
            sents = getSentences("./training_data/set"+str(i) + "/a" + str(j) + ".txt")
            for sent in sents:
                temp = what(sent)
                if temp != None:
                    print(what(sent))

if __name__ == "__main__":
    main()
"""
