import nltk
import spacy
import sys
from BinQ import getVP, parser, getBinQ, leftmost, sentences

#frequency
#number

def vb_past(label):
  return label in ['VBD', 'VBN']

"""TODO: how often/frequency thing, freq; Number(thing, how many), Equivalence(thing1, thing2)"""
sentences += ['The bus drove slowly', 'She ran away sneakily by tiptoeing her way out.', 'She is happy because she passed her test.']
#sentences = ['His son, a person, might have created succession struggles', 'Sneferu was succeeded by his son, Khufu, who built the Great Pyramid of Giza']

#for s in sentences:
#    const_tree = list(parser.raw_parse(s))[0][0]
#    print(const_tree)

def adjNPs(const_tree):
    l = [const_tree]
    while len(l) > 0:
        tree = l.pop()

def findAdv(const_tree, vp):
    for phr in const_tree: #if on same level
        if phr.label() == 'ADVP' and len(phr) == 1:
            const_tree.remove(phr)
            return const_tree, phr
    if vp:
        for phr in vp:
            #TODO should be more robust but works for now
            if phr.label() == 'ADVP' and len(phr) == 1:
                vp.remove(phr)
                return const_tree, phr
    return None, None
    
def findBy(const_tree, vbphr):
    for phr in const_tree: #if by is before subject
        if phr.label() == 'PP' and leftmost(phr)[0] == 'by':
            const_tree.remove(phr)
            return const_tree, phr
    #if by is within VP, also remove confusing adv
    if vbphr:
        for phr in vbphr:
            #TODO may have to go deeper
            if phr.label() == 'ADVP' and len(phr) == 1:
                vbphr.remove(phr)
    if vbphr:
        for phr in vbphr:
            if phr.label() == 'PP' and leftmost(phr)[0] == 'by':          
                vbphr.remove(phr)
                return const_tree, phr
    return None, None

def is_how(const_tree):
#returns is_how, obj, how
    cpy = const_tree.copy(deep=True)
    badadv = ['almost', 'already', 'also', 'basically', 'further', 'finally', 'generally', 'greatly','however', 'initially', 'just', 'later', 'longer', 'meanwhile', 'often', 'only', 'now', 'then', 'typically']
    #try by
    vbphr = getVP(const_tree, len(const_tree))
    (thing, bydoing) = findBy(const_tree, vbphr)
    if thing != None:
        return thing, bydoing
    else:
    #try adv
        (thing, how) = findAdv(cpy, getVP(cpy, len(cpy)))
        if thing == None or leftmost(how)[0].lower() in badadv:
            return None
        else:
            return cpy, how

#generate how question
def how(const_tree):
    res = is_how(const_tree)
    if res:
      q = getBinQ(res[0])
      if q != None:
        q = "How " +  q[:1].lower() + q[1:]
        return q   
    return None

def reason_cause(const_tree):
#something, cause
    for phr in const_tree: #if by is before subject
        if phr.label() == 'SBAR' and leftmost(phr)[0] == 'because':
            const_tree.remove(phr)
            return const_tree, phr
    #if by is within VP
    vp = getVP(const_tree, len(const_tree))
    if vp:
        for phr in vp:
            if phr.label() == 'SBAR' and leftmost(phr)[0] == 'because':
                reason = phr
                vp.remove(reason)
                return const_tree, reason
    return None, None

def why(const_tree):
    (happening,_) = reason_cause(const_tree)
    if happening:
        q = getBinQ(happening)
        q = "Why " + q[:1].lower() + q[1:]
        return q
    return None
def test():
    for s in sentences:
        try: 
            const_tree = list(parser.raw_parse(s))
        except:
            continue
        if const_tree[0][0]:
            const_tree = const_tree[0][0]
            q1 = why(const_tree)
            q2 = how(const_tree)
            if (q1) and len(q1) < 200:
                print(q1)
            if(q2) and len(q2) < 200:
                print(q2)
            #q = getBinQ(const_tree)
            #if q and len(q) < 200:
            #    print(q)
test()