import nltk
from nltk.corpus import wordnet as wn
import spacy

def getPOS(pos):
    if pos in ['JJ', 'JJR', 'JJS']:
        return wn.ADJ
    if pos in ['NN']: #TODO: get it working for NNS after figuring out conjugation
        return wn.NOUN
    if pos in ['RB', 'RBR', 'RBS']:
        return wn.ADV
    if pos in ['VB']: #, 'VBD', 'VBG', 'VBN', 'VBP']: #how to conjugate verb
        return wn.VERB

def getSynonyms(word, pos): 
    syns = wn.synsets(word, getPOS(pos))
    flatten = lambda l: [item for sublist in l for item in sublist]
    lemmas = (flatten([word.lemma_names() for word in syns]))
    rets = (set(lemmas))
    return [w for w in rets if w != word]

def getAntonyms(word, pos):
    ants = wn.synsets(word, getPOS(pos))
    antonyms = []
    for s in ants:
        for l in s.lemmas():
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())
    rets = (set(antonyms))
    return [w for w in rets if w != word]

spacy_nlp = spacy.load('en')

def changeHelp(doc, token, opp, i):
    if opp:
        words = getAntonyms(token.text, token.tag_)
    else:
        words = getSynonyms(token.text, token.tag_)
    ques = str(doc[:i])
    if len(words) > 0:
        ques += ' ' + words[0]
    else:
        return None
    if len(doc) > i+1:
        ques += ' ' + str(doc[i+1:])
    return ques

def change(question, nlp, opp):
    doc = nlp(u''+question)
    for i, token in enumerate(doc):
        if token.tag_ in ['JJ', 'JJR', 'JJS']:
            ques = changeHelp(doc, token, opp, i)
            if ques:
                return ques
    for i, token in enumerate(doc):
        if token.tag_ in ['RB', 'RBR', 'RBS']:
            ques = changeHelp(doc, token, opp, i)
            if ques:
                return ques
    for i, token in enumerate(doc):
        if token.tag_ in ['NN', 'VB']:
            ques = changeHelp(doc, token, opp, i)
            if ques:
                return ques
    return question

def posSets(sentence, nlp):
    doc = nlp(u''+sentence)
    adjs = set([])
    advs = set([])
    vbs = set([])
    nns = set([])
    for i, token in enumerate(doc):
        if token.tag_ in ['JJ', 'JJR', 'JJS']:
            adjs.add(token)
        elif token.tag_ in ['RB', 'RBR', 'RBS']:
            advs.add(token)
        elif token.tag_  == 'NN':
            nns.add(token)
        elif token.tag_ == 'VB':
            vbs.add(token)
    return adjs, advs, vbs, nns

def addSyn(question, nlp):
    return change(question, nlp, False)

def addAnt(question, nlp):
    return change(question, nlp, True)

def answerBinQ(sentence, question, nlp):
    pos = True
    adjQ, advQ, vbQ, nnQ = posSets(question, nlp)
    adjS, advS, vbS, nnS = posSets(sentence, nlp)
    adjDifQ = adjQ - adjS
    adjDifS = set([w.text for w in adjS - adjQ])
    advDifQ = advQ - advS
    advDifS = set([w.text for w in advS - advQ])
    vbDifQ = vbQ - vbS
    vbDifS = set([w.text for w in vbS - vbQ])
    nnDifQ = nnQ - nnS
    nnDifS = set([w.text for w in nnS - nnQ])
    for s in sentence: #contractions
        if s == 'not':
            pos = False
            break
    for adj in adjDifQ:
        if len(adjDifS.intersection(getAntonyms(adj.text, adj.tag_))) > 0:
            if not pos:
                return 'Yes'
            else:
                return 'No'
    for adv in advDifQ:
        if len(advDifS.intersection(getAntonyms(adv.text, adv.tag_))) > 0:
            if not pos:
                return 'Yes'
            else:
                return 'No'
    for vb in vbDifQ:
        if len(vbDifS.intersection(getAntonyms(vb.text, vb.tag_))) > 0:
            if not pos:
                return 'Yes'
            else:
                return 'No'
    for nn in nnDifQ:
        if len(nnDifS.intersection(getAntonyms(nn.text, nn.tag_))) > 0:
            if not pos:
                return 'Yes'
            else:
                return 'No'
    if pos:
        return 'Yes'
    else:
        return 'No'
"""
from stanfordcorenlp import StanfordCoreNLP
from BinQ import getBinQ
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English

parser = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

def readFileLines(path):
    with open(path, 'r') as f:
        return f.readlines()
def getSentences(path):
    text = [x.strip() for x in readFileLines(path)]
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    sentences = []
    for txtline in text:
        if len(txtline) < 30:
            continue
        sentences += [str(sent) for sent in nlp(txtline).sents]
    return sentences

sentences = getSentences('./training_data/set4/a3.txt')

for sent in sentences:
    const_tree = nltk.Tree.fromstring(parser.parse(sent))[0]
    l = getBinQ(const_tree)
    if l:
        print(l)
        print('Syn: ' + addSyn(l, spacy_nlp))
        print('Ant: ' + addAnt(l, spacy_nlp))
"""