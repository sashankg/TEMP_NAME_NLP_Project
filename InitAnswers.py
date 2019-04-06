import nltk
from nltk.parse import CoreNLPParser
from nltk.tree import Tree
from WhyHow import is_how, reason_cause
from Who import is_who
from LocTime import is_where, is_time 
from BinQ import getBinQ
import What
import spacy
from spacy.lemmatizer import Lemmatizer
from spacy.lang.en import LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES, English

parser = CoreNLPParser(url='http://localhost:9000')
lem = Lemmatizer(LEMMA_INDEX, LEMMA_EXC, LEMMA_RULES)

def main(questions, matches):
	spacy_nlp = spacy.load('en')
	for i in range(len(matches)):
		keyword = questions[i].split(" ")[0]
		parser.tagtype = 'pos'
		[(w, keywordpos)] = parser.tag([keyword])
		sent = matches[i]
		try:
			const_tree1 = list(parser.raw_parse(sent))[0][0]
			const_tree2 = const_tree1.copy(deep=True)
			const_tree3 = const_tree1.copy(deep=True)
			const_tree4 = const_tree1.copy(deep=True)
			const_tree5 = const_tree1.copy(deep=True)
			const_tree6 = const_tree1.copy(deep=True)
		except:
			continue
		try:
			nertags = parser.tag(sent.split())
		except:
			nertags = []
			s1 = spacy_nlp(sent) 
			for w in s1:
				nertags.append((str(w), w.ent_type_))
		if (keyword == "Where"): 
			(t1, whereA) = is_where(const_tree1, nertags, True)
			print(whereA)
		elif (keyword == "When"):
			(t2, whenA) = is_time(const_tree2, nertags, True)
			print(whenA)
		elif (keyword == "Who"):
			whoA = is_who(const_tree3)
			print(whoA)
		elif (keyword == "How"):
			(t5, howA) = is_how(const_tree5)
			print(howA)
		elif (keyword == "Why"):
			(t4, whyA) = reason_cause(const_tree4)
		elif (keywordpos == "MD" or lem(u''+keyword, u'VERB')[0] == "do" or lem(u''+keyword, u'VERB')[0] == "is" or lem(u''+keyword, u'VERB')[0] == "be"):
			binA = getBinQ(const_tree6)
			print("Yes")
		else:
			print("NONE")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])