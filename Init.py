import nltk
from nltk.parse import CoreNLPParser
from nltk.tree import Tree
from BinQ import getBinQ
from LocTime import where, when
from Who import who
from WhyHow import why, how
import sys
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English


parser = CoreNLPParser(url='http://localhost:9000')

#for simple sentences: subj + pred, NP + VP + .
#figure out when sentence form is ^
def readFileLines(path):
    with open(path, 'r') as f:
        return f.readlines()
def writeFile(path, contents):
    with open(path, 'w') as f:
        f.write(contents)

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

def test():
    sentences = []
    sentences += getSentences('training_data/set1/a1.txt')
    sentences += getSentences('training_data/set1/a2.txt')
    for sent in sentences:
        try:
            const_tree1 = list(parser.raw_parse(sent))[0][0]
            const_tree2 = const_tree1.copy(deep=True)
            const_tree3 = const_tree1.copy(deep=True)
            const_tree4 = const_tree1.copy(deep=True)
            const_tree5 = const_tree1.copy(deep=True)
            const_tree6 = const_tree1.copy(deep=True)
        except:
            #print('Exception at: ' + str(sent))
            continue
        nertags = []
        spacy_nlp = spacy.load('en')
        s1 = spacy_nlp(sent) 
        for w in s1.ents:
            nertags.append(w.label_)
        whereQ = where(const_tree1, nertags)
        whenQ = when(const_tree2, nertags)
        whoQ = who(const_tree3)
        whyQ = why(const_tree4)
        howQ = how(const_tree5)
        binQ = None
        whereQs = []
        whenQs = []
        whoQs = []
        whyQs = []
        howQs = []
        binQs = []
        if (const_tree6[0][0]):
            binQ = getBinQ(const_tree6)
            if binQ and len(binQ) < 200:
                print(binQ)
                binQs.append(binQs)
        if whereQ:
            whereQs.append(whereQ)
            print(whereQ)
        if whenQ:
            whenQs.append(whenQ)
            print(whenQ)
        if whoQ:
            whoQs.append(whoQ)
            print(whoQ)
        if whyQ:
            whyQs.append(whyQ)
            print(whyQ)
        if howQ:
            howQs.append(howQ)
            print(howQ)
    questions = []

test()