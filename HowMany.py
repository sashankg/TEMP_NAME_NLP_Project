import nltk
import spacy
import sys
from BinQ import getVP, getBinQ, leftmost, getDoForm, getNP
from LocTime import searchPhrase, searchAndRem

def is_valid(nertags):
	numtags = ["NUMBER", "CARDINAL"]
	num_numtags = 0
	for n in nertags:
		if (n[1] in numtags):
			num_numtags += 1
	if ((num_numtags > 1) or (num_numtags == 0)):
		return False
	return True

def is_howmany(const_tree, nertags):
	numtags = ["NUMBER", "CARDINAL"]
	np = getNP(const_tree, len(const_tree))
	vp = getVP(const_tree, len(const_tree))
	const_tree1 = const_tree.copy(deep=True)
	(const_tree2, preps) = searchAndRem(const_tree1, 'PP')
	preps_lst = []
	if preps:
		preps_lst = ' '.join(preps[0].leaves()).split()
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
		if (len(preps_lst) > 0):
			for n in nertags:
				if (n[1] in numtags and n[0] in preps_lst):
					np_string = ' '.join(' '.join(np.leaves()).split())
					np_string_lower = np_string[0].lower() + np_string[1:]
					vp_string = ' '.join(' '.join(vp.leaves()).split())
					no_prep = vp_string.replace(' '.join(preps_lst), "")
					rest_preps = ' '.join(preps_lst).replace(n[0], "").replace(preps_lst[0], "")
					verb = ' '.join(' '.join(vp[0].leaves()).split())
					no_prep_verb = no_prep.replace(verb, "")
					try:
						(prep_tree, det) = searchAndRem(preps, 'DT')
						rest_preps2 = ' '.join(' '.join(prep_tree[0].leaves()).split())
						final_preps = rest_preps2.replace(' '.join(' '.join(det[0].leaves()).split()), "").replace(n[0], "").replace(preps_lst[0], "")
						ques = 'How many' + final_preps + ' ' + verb + ' ' + np_string_lower + no_prep_verb + " " + preps_lst[0] + "?"
					except:
						ques = 'How many' + rest_preps + ' ' + verb + ' ' + np_string_lower + no_prep_verb + " " + preps_lst[0] + "?"
					return ques, n[0]
		np_list = ' '.join(np.leaves()).split()
		for n in nertags:
			if (n[1] in numtags and n[0] in np_list):
				q_body = ' '.join(' '.join(const_tree.leaves()).split())
				q_body1 = q_body.replace(n[0], "")
				q_body1_lower = q_body1[0].lower() + q_body1[1:]
				q_body2 = q_body1_lower
				try:
					(np_tree, det) = searchAndRem(np, 'DT')
					rest_np = ' '.join(' '.join(np_tree.leaves()).split())
					vp_str = ' '.join(' '.join(vp.leaves()).split())
					q_body2 = rest_np.replace(' '.join(' '.join(det[0].leaves()).split()), "").replace(n[0], "") + ' ' + vp_str
				except:
					pass
				ques = 'How many ' + q_body2 + "?"
				return ques, n[0]
		return None, None
	return None, None

def howmany(const_tree, nertags):
	if is_valid(nertags):
		(p, a) = is_howmany(const_tree, nertags)
		if a:
			return p
	return None