import nltk
from nltk.parse import CoreNLPParser
from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree
from BinQ import getBinQ
from LocTime import where, when
from Who import who
from WhyHow import why, how
from HowMany import howmany
import sys
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English
from What import what
from SynAnt import addAnt
from careerstat import getSentences, askCareerStat

parser = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

#for simple sentences: subj + pred, NP + VP + .
#figure out when sentence form is ^
def readFileLines(path):
    with open(path, 'r') as f:
        return f.readlines()
def writeFile(path, contents):
    with open(path, 'w') as f:
        f.write(contents)

'''def getSentences(path):
    text = [x.strip() for x in readFileLines(path)]
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    sentences = []
    for txtline in text:
        if len(txtline) < 30:
            continue
        sentences += [str(sent) for sent in nlp(txtline).sents]
    return sentences'''

def goodQs(l): #filter q by len
    if not l:
        return [],[]
    good = []
    bad = []
    for q in l:
        qlen = len(q.split())
        if (5 < qlen < 25):
            good.append(q)
        else:
            bad.append(q)
    return good, bad

def getQs(sentences):
    whereQs = []
    whenQs = []
    whoQs = []
    whyQs = []
    howQs = []
    howmanyQs = []
    binQs = []
    whatQs = []
    
    spacy_nlp = spacy.load('en')
    stop = ['bibliography', 'references', 'see also']
    #parser.tagtype = 'ner'
    for sent in sentences:
        whereQ = None
        whenQ = None
        whoQ = None
        whyQ = None
        howQ = None
        howmanyQ = None
        binQ = None
        whatQ = None
        question = None
        if sent.strip(' ').lower() in stop:
            break
        try:
            const_tree1 = Tree.fromstring(parser.parse(sent))[0]
            const_tree2 = const_tree1.copy(deep=True)
            const_tree3 = const_tree1.copy(deep=True)
            const_tree4 = const_tree1.copy(deep=True)
            const_tree5 = const_tree1.copy(deep=True)
            const_tree6 = const_tree1.copy(deep=True)
            const_tree7 = const_tree1.copy(deep=True)
        except:
            continue
        try:
            nertags = parser.ner(sent)
        except:
            nertags = []
            s1 = spacy_nlp(sent) 
            for w in s1:
                nertags.append((str(w), w.ent_type_))
        if (question == None):
            if (const_tree6[0][0]):
                binQ = getBinQ(const_tree6)
                if binQ and len(binQ) < 200:
                    binQs.append(addAnt(binQ, spacy_nlp))
                    #print(binQ)
        if (question == None):
            try:
                whyQ = why(const_tree4)
                question = whyQ
            except:
                continue
        if (question == None):
            try:
                howQ = how(const_tree5)
                question = howQ
            except:
                continue
        if (question == None):
            try:
                whereQ = where(const_tree1, nertags)
                question = whereQ
            except:
                continue
        if (question == None):
            try:
                whenQ = when(const_tree2, nertags)
                question = whenQ
            except:
                continue
        if (question == None):
            try:
                whoQ = who(const_tree3, nertags)
                question = whoQ
            except:
                continue
        if (question == None):
            try:
                howmanyQ = howmany(const_tree7, nertags)
                question = howmanyQ
            except:
                continue
        if (question == None):
            try:
                whatQ = what(sent)
                question = whatQ
            except:
                continue
        if whereQ:
            whereQs.append(whereQ)
            #print(whereQ)
        if whenQ:
            whenQs.append(whenQ)
            #print(whenQ)
        if whoQ:
            whoQs.append(whoQ)
            #print(whoQ)
        if whyQ:
            whyQs.append(whyQ)
            #print(whyQ)
        if howQ:
            howQs.append(howQ)
            #print(howQ)
        if howmanyQ:
            howmanyQs.append(howmanyQ)
        if whatQ:
            if (len(whatQ.split()) > 3): #filter potentially bad qs
                if not (whereQ or whenQ or whoQ):
                    whatQs.append(whatQ)
    return whereQs, whenQs, whoQs, whyQs, howQs, howmanyQs, binQs, whatQs

def main(path, n):
    sentences = []
    clubs, intl, indvl, pfmcs, name, sentences = getSentences(path)
    #sentences += getSentences(path)
    nquestions = n
    whereQs = []
    whenQs = []
    whoQs = []
    whyQs = []
    howQs = []
    howmanyQs = []
    binQs = []
    whatQs = []
    statQs = []
    spacy_nlp = spacy.load('en')
    stop = ['Bibliography', 'References', 'See also']
    (whereQs, whenQs, whoQs, whyQs, howQs, howmanyQs, binQs, whatQs) = getQs(sentences)
    goodStats = askCareerStat(clubs, intl, indvl, pfmcs, name)
    final_qs = []
    goodWho, b1 = goodQs((whoQs))
    goodWhere, b2 = goodQs((whereQs))
    goodWhen, b3 = goodQs((whenQs))
    goodWhy, b4 = goodQs((whyQs))
    goodWhat, b5 = goodQs((whatQs))
    goodHow, b6 = goodQs((howQs))
    goodBi, b7 = goodQs((binQs))
    goodHowMany, b8 = goodQs((howmanyQs))
    #print(whatQs)
    bads = [goodBi, goodWhat, b1, b2, b3, b4, b6, b7, b5, b8] #who, what, where, when, why, how, howmany
    while len(goodWho) + len(goodWhere) + len(goodWhen) + len(goodWhy) +len(goodHow) + len(goodHowMany) + len(goodStats)> 0:
        if len(final_qs) > nquestions:
            break
        if goodWho:
            final_qs.append(goodWho.pop(0))
        if goodWhere:
            final_qs.append(goodWhere.pop(0))
        if goodWhen:
            final_qs.append(goodWhen.pop(0))
        if goodWhy:
            final_qs.append(goodWhy.pop(0))
        if goodWhat:
            final_qs.append(goodWhat.pop(0))
        if goodHow:
            final_qs.append(goodHow.pop(0))
        if goodHowMany:
            final_qs.append(goodHowMany.pop(0))
        if goodBi:
            final_qs.append(goodBi.pop(0))
        if goodStats:
            final_qs.append(goodStats.pop(0))
    for b in bads:
        if len(final_qs) < nquestions:
            final_qs += b
    while(len(final_qs) < nquestions):
        final_qs.append('Is this a question?')
    for q in final_qs[0:nquestions]:
        print(q.replace('-LRB- ', '(').replace(' -RRB-', ')').replace(" ,", ",").replace( " '", "'").replace(" .", "").replace("  ", " "))
    #parser.close()

if __name__ == "__main__":
    main(sys.argv[1], int(sys.argv[2]))
    #for i in range(int(sys.argv[2])):
    #    print("Who is Cleopatra?")
