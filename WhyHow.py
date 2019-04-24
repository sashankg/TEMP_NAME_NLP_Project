import nltk
import spacy
import sys
from BinQ import getVP, getBinQ, leftmost
#frequency
#number

def vb_past(label):
  return label in ['VBD', 'VBN']

"""TODO: how often/frequency thing, freq; Number(thing, how many), Equivalence(thing1, thing2)"""
#sentences += ['The bus drove slowly', 'She ran away sneakily by tiptoeing her way out.', 'She is happy because she passed her test.']
#sentences = ['His son, a person, might have created succession struggles', 'Sneferu was succeeded by his son, Khufu, who built the Great Pyramid of Giza']

#for s in sentences:
#    const_tree = list(parser.raw_parse(s))[0][0]
#    print(const_tree)

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
    for phrase in const_tree:
        if phrase.label() == 'PP' and leftmost(phrase)[0] in ['by','By']:
            for phr in phrase:
                if phr.label() == 'NP': #if NP before VP, then is location by  
                    if leftmost(phr).label() == 'VBG':     
                        const_tree.remove(phrase)
                        return const_tree, phrase
                    else:
                        return None, None
                if phr.label() == 'VP':
                    const_tree.remove(phrase)
                    return const_tree, phrase
                if phr.label() == 'S' and phr[0].label() == 'VP':
                    const_tree.remove(phrase)
                    return const_tree, phrase
    #if by is within VP, also remove confusing adv
    if vbphr:
        for phr in vbphr:
            #TODO may have to go deeper
            if phr.label() == 'ADVP' and len(phr) == 1:
                vbphr.remove(phr)
    if vbphr:
        for phrase in vbphr:
            if phrase.label() == 'PP' and leftmost(phrase)[0] == 'by':
                for phr in phrase:
                    if phr.label() == 'NP': #if NP before VP, then is location by
                        if leftmost(phr).label() == 'VBG':
                            vbphr.remove(phrase)
                            return const_tree, phrase
                        else:
                            return None, None
                    if phr.label() == 'VP':
                        vbphr.remove(phrase)
                        return const_tree, phrase
                    if phr.label() == 'S' and phr[0].label() == 'VP':
                        vbphr.remove(phrase)
                        return const_tree, phrase
    return None, None

def is_how(const_tree):
#returns is_how, obj, how
    cpy = const_tree.copy(deep=True)
    badadv = ['all', 'almost', 'already', 'also', 'basically', 'further', 'finally', 'generally', 'greatly', 'however', 'initially', 'just', 'later', 'longer', 'meanwhile', 'often', 'only', 'perhaps', 'now', 'then', 'typically']
    #try by
    vbphr = getVP(const_tree, len(const_tree))
    (thing, bydoing) = findBy(const_tree, vbphr)
    if thing != None:
        return thing, " ".join(bydoing.leaves())
    else:
    #try adv
        (thing, how) = findAdv(cpy, getVP(cpy, len(cpy)))
        if thing == None or leftmost(how)[0].lower() in badadv:
            return None, None
        else:
            return cpy, " ".join(how.leaves())

#generate how question
def how(const_tree):
    res = is_how(const_tree)
    if len(const_tree) > 0 and hasattr(const_tree[0], 'label') and const_tree[0].label() == ',':
        const_tree.remove(const_tree[0])
    if not (res == (None, None)):
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
                return const_tree, " ".join(reason.leaves())
    return None, None

def why(const_tree):
    (happening,_) = reason_cause(const_tree)
    if happening:
        q = getBinQ(happening)
        if q:
            q = "Why " + q[:1].lower() + q[1:]
            return q
    return None
