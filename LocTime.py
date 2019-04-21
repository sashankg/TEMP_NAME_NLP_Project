import nltk
import spacy
import sys
from BinQ import getVP, getBinQ, leftmost

#parser.tagtype = 'ner'

def searchPhrase(const_tree, phraseType):
    phrases = ['ADJP', 'ADVP', 'CONJP', 'FRAG', 'INTJ', 'LST', 'NAC', 'NP', 'NX', 'PP', 'PRN', 'PRT', 'QP', 'RRC', 'UCP', 'VP', 'WHADJP', 'WHAVP', 'WHNP', 'WHPP', 'X']
    if const_tree.label() not in phrases:
        return []
    phrases = []
    q = [const_tree]
    while (len(q) > 0):
        t = q.pop(0)
        for subtree in t:
            if subtree in phrases:
                q.append(subtree)
            if subtree.label() == phraseType:
                phrases.append(subtree)
    return phrases
def searchAndRem(const_tree, phraseType):
    phrases = []
    q = [const_tree]
    while (len(q) > 0):
        t = q.pop(0)
        if not t:
            break
        for subtree in t:
            if len(subtree) > 1:
                q.append(subtree)
            if subtree.label() == phraseType:
                phrases.append(subtree)
                t.remove(subtree)
    return const_tree, phrases

def is_where(const_tree, nertags, answering):
    locationtags = ['LOC', 'GPE', 'STATE_OR_PROVINCE', 'LOCATION', 'CITY', 'COUNTRY']
    #prepositions = ['TO', 'IN']
    (const_tree, preps) = searchAndRem(const_tree, 'PP')
    ans = ''
    for p in preps:
        npTree = searchPhrase(p, 'NP')
        if len(npTree) > 0:
            np = ' '.join(npTree[0].leaves())
        else:
            break
        for i in range(len(nertags)):
            #oversimplifying; make more robust
            if nertags[i][1] in locationtags and (nertags[i][0]) == np.split()[0] and i > 0 and (nertags[i-1][0]).lower() != 'of':    
                return const_tree, ' '.join(p.leaves())
    if answering and len(preps) > 0: #return some rand non-loc PP as ans
        return const_tree, ' '.join(preps[0].leaves())
    else:
        return None, None

def is_time(const_tree, nertags, answering):
    timetags = ['DATE', 'TIME']
    vp = getVP(const_tree, len(const_tree))
    for phr in const_tree: #if on same level
        if phr.label() == 'PP':
            npTree = searchPhrase(phr, 'NP')
            if len(npTree) > 0:
                np = ' '.join(npTree[0].leaves()).split()
            else:
                break
            for n in nertags:
                if n[1] in timetags and np[0] == (n[0]):
                    const_tree.remove(phr)
                    return const_tree, phr
    if vp:
        for phr in vp:
            #TODO should be more robust but works for now
            npTree = searchPhrase(phr, 'NP')
            if phr.label() == 'PP':
                if len(npTree) > 0:
                    np = ' '.join(npTree[0].leaves()).split()
                else:
                    break
                for n in nertags:
                    if n[1] in timetags and np[0] == (n[0]):
                        vp.remove(phr)
                        return const_tree, phr
    if answering:
        res = ''
        for n in nertags:
            if n[1] in timetags:
                res += n[0] + ' '
            if len(res) > 0 and n[1] not in timetags:
                break
        if len(res) > 0:
            return const_tree, res
    return None, None
    

def where(const_tree, nertags):
    (const_tree, _) = is_where(const_tree, nertags, False)
    if const_tree:
        q = getBinQ(const_tree)
        if q:
            return 'Where ' + q[:1].lower() + q[1:]
        else:
            return None
    else:
        return None
def when(const_tree, nertags): #TODO identify pairs of dates and determine how to ask some question about it
    (const_tree, phr) = is_time(const_tree, nertags, False)
    if const_tree:
        q = getBinQ(const_tree)
        if q:
            return 'When ' + q[:1].lower() + q[1:]
        else:
            return None
    else:
        return None
