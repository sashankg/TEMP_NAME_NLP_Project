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
from What import what
import multiprocessing as mp

NUM_PROCESSES = mp.cpu_count()     # Uses all cores available
PROCESSOR_RATIO = 2

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
    binQs = []
    whatQs = []
    spacy_nlp = spacy.load('en')
    stop = ['bibliography', 'references', 'see also']
    parser.tagtype = 'ner'

    for sent in sentences:
        if sent.strip(' ').lower() in stop:
            break
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
        try:
            nertags = parser.tag(sent.split())
        except:
            nertags = []
            s1 = spacy_nlp(sent) 
            for w in s1:
                nertags.append((str(w), w.ent_type_))
           
        whereQ = where(const_tree1, nertags)
        whenQ = when(const_tree2, nertags)
        whoQ = who(const_tree3)
        whyQ = why(const_tree4)
        howQ = how(const_tree5)
        whatQ = what(sent)
        binQ = None
        
        if (const_tree6[0][0]):
            binQ = getBinQ(const_tree6)
            if binQ and len(binQ) < 200:
                binQs.append(binQ)
                #print(binQ)
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
        if (len(whatQ.split()) > 3): #filter potentially bad qs
            whatQs.append(whatQ)
    return whereQs, whenQs, whoQs, whyQs, howQs, binQs, whatQs
    

def chunks(l, n):
    chunk_size = len(l) // n
    return [[l[i:i + chunk_size]] for i in range(0, len(l), chunk_size)]

def main():
    sentences = []
    sentences += getSentences(sys.argv[1])
    nquestions = int(sys.argv[2])
    if len(sentences) <= NUM_PROCESSES * PROCESSOR_RATIO:
        results = getQs(sentences, nquestions)

    # Otherwise divide workload amongst process threads
    else:
        slices = chunks(sentences, NUM_PROCESSES)
        pool = mp.Pool(processes=NUM_PROCESSES)        
        # starmap 
        results = pool.starmap(getQs, slices)
    whereQs = []
    whenQs = []
    whoQs = []
    whyQs = []
    howQs = []
    binQs = []
    whatQs = []
    for r in results:
        whereQs += (r[0])
        whenQs += r[1]
        whoQs += r[2]
        whyQs += r[3]
        howQs += r[4]
        binQs += r[5]
        whatQs += r[6]
    final_qs = []
    goodWho, b1 = goodQs((whoQs))
    goodWhere, b2 = goodQs((whereQs))
    goodWhen, b3 = goodQs((whenQs))
    goodWhy, b4 = goodQs((whyQs))
    goodWhat, b5 = goodQs((whatQs))
    goodHow, b6 = goodQs((howQs))
    goodBi, b7 = goodQs((binQs))
    bads = [goodBi, goodWhat, b1, b2, b3, b4, b6, b7, b5] #who, what, where, when, why, how
    while len(goodWho) + len(goodWhere) + len(goodWhen) + len(goodWhy) +len(goodHow) > 0:
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
        if goodBi:
            final_qs.append(goodBi.pop(0))
    for b in bads:
        if len(final_qs) < nquestions:
            final_qs += b
    while(len(final_qs) < nquestions):
        final_qs.append('Is this a question?')
    for q in final_qs[0:nquestions]:
        print(q)

if __name__ == "__main__":
    main()