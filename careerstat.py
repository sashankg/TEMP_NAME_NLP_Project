
from stanfordcorenlp import StanfordCoreNLP
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English
from nltk import Tree
from WhyHow import how
from BinQ import getBinQ
from fuzzywuzzy import fuzz


#parser = StanfordCoreNLP(r'stanford-corenlp-full-2018-02-27')

def readFileLines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.readlines()
def getSentences(path):
    text = [x.strip() for x in readFileLines(path)]
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    sentences = []
    clubs = []
    intl = []
    indvl = []
    pfmcs = []
    numLines = len(text)
    name = text[0]
    for i in range(numLines): #won't work for beckham 
        if text[i] == 'Club':
            i = i + 1
            while i < numLines and text[i] != "":
                clubs.append(text[i])
                i += 1
        if text[i] == 'International':
            i  = i + 1
            while i < numLines and text[i] != "" and text[i] != 'Individual':
                intl.append(text[i])
                i += 1
        if text[i] == 'Individual':
            i += 1
            justaspace = False
            if i + 1 < numLines and text[i+1] != "":
                justaspace = True
            while i < numLines and (text[i] != "" or justaspace):
                justaspace=False
                indvl.append(text[i])
                i += 1
        if text[i] == 'Performances':
            i  = i + 1
            while i < numLines and text[i] != "":
                pfmcs.append(text[i])
                i += 1
        if i < numLines and len(text[i]) > 30:
            sentences += [str(sent) for sent in nlp(text[i]).sents]
    return clubs, intl, indvl, pfmcs, name, sentences

def askCareerStat(clubs, intl, indvl, pfmcs, name):
    questions = []
    cnt = 0
    if len(indvl) > 0:
        questions.append("What is the first individual honour " + name + ' won?')
    
    for c in intl:
        winyr = c.split(':')
        if cnt < 3 and len(winyr) > 1:
            questions.append("What year(s) did " + name + " win the " + winyr[0] + '?')
            cnt += 1
    cnt = 0
    for c in clubs: #add at most three of these
        winyr = c.split(':')
        if cnt < 3 and len(winyr) > 1:
            winyrs = winyr[1].split()
            for w in winyrs:
                if w != "Runner-up":
                    word = 'in '
                    yr = w.strip().strip(',')
                    if len(yr) > 4:
                        word = 'from '
                        w = w[:4]
                    questions.append("What club honour did " + name + " win " +  word + yr + '?')
                    cnt += 1
                    break    
    if len(pfmcs) > 0:
        questions.append("What are some of " + name + "'s top performances?")
    return questions


def matching_stat(honours, question):
    max_ratio = 0
    closest_sentence = ""
    for s in honours:
        r = fuzz.partial_ratio(question.lower(), s.lower())
        if r > max_ratio:
            max_ratio = r
            closest_sentence = s
    return closest_sentence, max_ratio
    

def matching_sentence(sentences, question):
    max_ratio = 0
    closest_sentence = ""
    for s in sentences:
        r = fuzz.partial_ratio(question.lower(), s.lower())
        if r > max_ratio:
            max_ratio = r
            closest_sentence = s
    return closest_sentence, max_ratio

def finalMatch(clubs, intl, indvl, pfmcs, sentences, question):
    #find matching career stat for question
    club_sent, ratc = matching_stat(clubs, question)
    intl_sent, ratint = matching_stat(intl, question)
    indvl_sent, ratidv = matching_stat(indvl, question)
    pfmcs_sent, ratp = matching_stat(pfmcs, question)
    sents = [club_sent, intl_sent, indvl_sent, pfmcs_sent]
    ques = question.lower()
    if 'club' in ques:
        match = club_sent
        final_ratio = ratc
    elif 'international' in ques:
        match = intl_sent
        final_ratio = ratint
    elif 'individual' in ques:
        match = indvl_sent
        final_ratio = ratidv
    elif 'performance' in ques:
        match = pfmcs_sent
        final_ratio = ratp
    else:
        rats = [ratc, ratint, ratidv, ratp]
        ind = max(zip(rats, range(len(rats))))[1]
        match = sents[ind]
        final_ratio = rats[ind]
    #print(match)
    #print(close_other)
    return match

def answerStats(clubs, intl, indvl, pfmcs, sentences, question):
    match = finalMatch(clubs, intl, indvl, pfmcs, sentences, question)
    if ('What year(s)' in question):
        m = match.split(':')
        if len(m) > 1:
            return m[1].strip()
    if ('What club honour' in question):
        for match in clubs:
            l = question.strip('?').split()
            if l[len(l) - 1] in match:
                m = match.split(':')
                if len(m) > 1:
                    return m[0]
    if ('What is the first individual honour' in question):
        minYr = 2020
        firstwin = 'I can\'t find it.'
        for hon in indvl: #hon is "award: year, year, ..."
            winyr = hon.split(':')
            if len(winyr) > 1:
                winyrs = winyr[1].split() #winyrs is "yr, yr, yr"
                for w in winyrs:
                    if w != "Runner-up":
                        #print(w)
                        if len(w) > 4:
                            w = w[:4]
                        if str.isdigit(w):
                            yr = int(w)
                            if yr < minYr:
                                minYr = yr
                                firstwin = winyr[0]
        return firstwin
    if ('What are some of' in question):
        if len(pfmcs) > 1:
            return (pfmcs[0] + ' and ' + pfmcs[1])
                        

"""clubs, intl, indvl, pfmcs, name, sentences = getSentences('data/set1/a8.txt')
questions = askCareerStat(clubs, intl, indvl, pfmcs, name)
for q in questions:
    print(q)
    print(answerStats(clubs, intl, indvl, pfmcs, sentences, q))"""
"""from LocTime import where
for sent in sentences:
    nertags = parser.ner(sent)
    tree = (Tree.fromstring(parser.parse(sent))[0])
    whereQ = (where(tree, nertags))
    print(whereQ)
parser.close()"""

##appositive stuff that doesn't work
"""


#works for:
#    NP(NP, NP)
#    NP(NP, SBAR(WHNP(WP)(S (VP NP)))), where VP is 'to be'

def leftmost(phr):
    tmp = phr
    while isinstance(tmp[0], Tree):
        tmp = tmp[0]
    return tmp

def getFirstNP(const_tree):
#gets first NP in const_tree on the first level/second for VPs
    const_tree = const_tree[0]
    for phr in const_tree:
        if phr.label() == 'NP':
            return phr
        if phr.label() == 'VP':   
            vb = (leftmost(phr))
            if vb[0] == ('is' or 'are' or 'was' or 'were'):
                for p in phr:
                    if p.label() == 'NP':
                        #print(p)
                        return p
    return None


def getNounEquiv(const_tree):
    q = [const_tree]
    while len(q) > 0:
        tree = q.pop(0)
        for phr in tree:
            if phr.label() == 'NP':
                if (len(phr) > 2 and phr[0].label() == 'NP' and phr[1].label() == ','):
                    if (phr[2].label() == 'NP'):
                        return phr[0], phr[2]
                    elif (phr[2].label() == 'SBAR' and len(phr[2]) > 0 and phr[2][0].label() == 'WHNP'):
                        np = getFirstNP(phr[2][1:])
                        if np is None:
                            return None, None
                        return phr[0], getFirstNP(phr[2][1:])
                elif(len(phr) > 2 and phr[0].label() == 'NP' and phr[1].label() == 'SBAR' and phr[1][0].label() == 'WHNP'):
                    np2 = getFirstNP(phr[1][1:])
                    if np2 is None:
                        return None, None
                    return phr[0], getFirstNP(phr[1][1:])
            if len(phr) > 1 and hasattr(phr[0], 'label'):
                q.append(phr)
    return None, None


def askEquiv(np1, np2):
    for p in np1:
        if p.label() == ('NN' or 'NP'):
            return "Is " + ' '.join(np1.leaves()) + ' '.join(np2.leaves())
    for p in np2:
        if p.label() == ('NNS' or 'NNPS'):
            return "Are " + ' '.join(np1.leaves()) + ' '.join(np2.leaves())
    return None

"""
