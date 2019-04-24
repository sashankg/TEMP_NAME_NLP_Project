import nltk
import spacy
import sys
from BinQ import getVP, getBinQ, leftmost, getDoForm, getNP
from LocTime import searchPhrase, searchAndRem

def is_howmany(const_tree, nertags):
	numtags = ["NUMBER", "CARDINAL"]
	np = getNP(const_tree, len(const_tree))
	vp = getVP(const_tree, len(const_tree))
	const_tree1 = const_tree.copy(deep=True)
	(const_tree2, preps) = searchAndRem(const_tree1, 'PP')
	if preps:
		preps = ' '.join(preps[0].leaves()).split()
	if vp:
		subnpTree = searchPhrase(vp, 'NP')
		if len(subnpTree) > 0:
			subnp = ' '.join(subnpTree[0].leaves()).split()
			for n in nertags:
				if (n[1] in numtags and subnp[0] == (n[0])):
					restnp = (' '.join(subnp)).replace(subnp[0], "")
					doform = getDoForm(vp[0])[0].lower() + getDoForm(vp[0])[1:]
					q_body = ' '.join(' '.join(const_tree1[0].leaves()).split())
					q_body_lower = q_body[0].lower() + q_body[1:]
					ques = 'How many' + restnp + ' ' + doform + ' ' + q_body_lower + ' have?'
					return ques, subnp[0]
		elif (len(preps) > 0):
			for n in nertags:
				if (n[1] in numtags and n[0] in preps):
					np_string = ' '.join(' '.join(np.leaves()).split())
					np_string_lower = np_string[0].lower() + np_string[1:]
					vp_string = ' '.join(' '.join(vp.leaves()).split())
					no_prep = vp_string.replace(' '.join(preps), "")
					rest_preps = ' '.join(preps).replace(n[0], "").replace(preps[0], "")
					verb = ' '.join(' '.join(vp[0].leaves()).split())
					no_prep_verb = no_prep.replace(verb, "")
					ques = 'How many' + rest_preps + ' ' + verb + ' ' + np_string_lower + no_prep_verb + " " + preps[0] + "?"
					return ques, n[0]
		np_list = ' '.join(np.leaves()).split()
		for n in nertags:
			if (n[1] in numtags and n[0] in np_list):
				q_body = ' '.join(' '.join(const_tree.leaves()).split())
				q_body1 = q_body.replace(n[0], "")
				q_body1_lower = q_body1[0].lower() + q_body1[1:]
				ques = 'How many' + q_body1_lower + "?"
				return ques, n[0]
		return None, None
	return None, None

def howmany(const_tree, nertags):
	(p, a) = is_howmany(const_tree, nertags)
	if a:
		return p
	return None