import nltk
#from nltk.parse import CoreNLPParser
from nltk.tree import Tree
#from spacy.lemmatizer import Lemmatizer
#from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English
import sys
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English

lem = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)
#TODO: some capitalization errors welp
def leftmost(phr):
#first word in tree to lower case unless proper noun
    tmp = phr
    while isinstance(tmp[0], Tree):
        tmp = tmp[0]
    return tmp
def insert_lemma(phr, lemma):
#insert lemmatized verb into phrase
    tmp = phr
    while isinstance(tmp[0], Tree):
        tmp = tmp[0]
    tmp[0] = lemma
    return

def lemVerb(phr, lemmatizer):
#lemmatize the head verb of phr
    verb = leftmost(phr)
    vblem = lemmatizer(u''+verb[0], u'VERB')[0]
    return vblem

def fixcap(phr):
#uncapitalize phr if not proper noun or I
    tmp = leftmost(phr)
    if tmp.label() != 'NNP' and tmp.label() != 'NNPS' and tmp[0] != 'I':
        tmp[0] = tmp[0].lower()
    return phr

def getDoForm(verb):
#get correct tense of 'do' based on verb tense
    ret = ''
    if verb.label().endswith('Z'):
        ret += 'Does'
    elif verb.label().endswith('P'):
        ret += 'Do'
    elif verb.label().endswith('D'):
        ret += 'Did'  
    return ret

def getVP(const_tree, tree_len):
    i = 1
    while i < tree_len and const_tree[i].label() != 'VP':
        i += 1
    if (i >= tree_len):
        return None
    return const_tree[i]

def getNP(const_tree, tree_len):
    i = 0
    while i < tree_len and const_tree[i].label() != 'NP':
        i += 1
    if (i >= tree_len):
        return None
    return const_tree[i]

def getBinQ(const_tree):
    tree_len = len(const_tree)
    subject = fixcap(const_tree[0]) 
    if (subject.label() != 'NP' or tree_len < 2):
        return None
    verbphr = getVP(const_tree, tree_len)
    if verbphr == None:
        return None
    #verb = verbphr[0][0] #verbphr[0] = [verb, tag]
    #vblem = lem(u''+verb, u'VERB')[0]
    verb = leftmost(verbphr)
    vblem = lemVerb(verbphr, lem)
    if verbphr[0].label() == 'MD' or vblem == u'be':
        ques = ''
        for n in verbphr[1:]:
            ques += ' ' + ' '.join(n.leaves())
        beg = ''
        label = ''
        for n in subject:
            beg += ' ' + ' '.join(n.leaves())
        ques = verb[0].capitalize() + beg + ques + '?'
        return (ques)
    else:
        insert_lemma(verbphr, vblem)
        '''TODO correct form of do based on tense/plurality of verb
            VBG, VBN verb, LRB and RRB remove
        '''
        doform = getDoForm(verb)
        ques = ''
        for n in verbphr:
            ques += ' ' + ' '.join(n.leaves())
        beg = ''
        for n in subject:
            beg += ' ' + ' '.join(n.leaves())
        ques = doform + beg + ques + '?'
        return (ques)

