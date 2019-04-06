import nltk
import spacy
import sys
from BinQ import getVP, getNP, getBinQ, leftmost

def is_who(const_tree):
	cpy = const_tree.copy(deep=True)
	vbphr = getVP(const_tree, len(const_tree))
	nphr = getNP(const_tree, len(const_tree))
	if not (vbphr and nphr):
		return None
	poss_who = ''
	for n in nphr:
		poss_who += ' ' + ' '.join(n.leaves())
	spacy_nlp = spacy.load('en')
	noun = spacy_nlp(poss_who) 
	who = None
	for c in noun.ents:
		if (c.label_ == ("PERSON" or "NORP" or "ORG" or "GPE")):
			who = c
	return str(who)

def who(const_tree):
	res = is_who(const_tree)
	q = ''
	if res:
		vbphr = getVP(const_tree, len(const_tree))
		if vbphr:
			vp = ''
			for v in vbphr:
				vp += ' ' + ' '.join(v.leaves())
			q =  "Who" + vp + "?"
			return q
	return None
