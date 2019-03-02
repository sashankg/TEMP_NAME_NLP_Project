import nltk
from stanfordcorenlp import StanfordCoreNLP
import sys
import os

#for simple sentences: subj + pred, NP + VP + .
#figure out when sentence form is ^
path = sys.argv[1] #path to stanford corenlp

nlp = StanfordCoreNLP(r'' + path)
sentences = ["The cat is eating the cake.", "She likes the chocolate cake.", "I should sleep.", "She ran faster than me."]
questions = []
#TODO: capitalization 
for sent in sentences:
    const_tree = nltk.Tree.fromstring(nlp.parse(sent))[0]
    subject = const_tree[0]
    verbphr = const_tree[1]
    verb  = verbphr[0][0] #verbphr[0] = [verb, tag]
    lem = nltk.stem.WordNetLemmatizer()
    if verbphr[0].label() == 'MD' or lem.lemmatize(verb, pos='v') == u'be':
        print('invert')
        ques = ''
        for n in verbphr[1:]:
            ques += ' ' + ' '.join(n.leaves())
        beg = ''
        for n in subject:
            beg += ' ' + ' '.join(n.leaves())
        ques = verb + beg + ques + '?'
        print(ques)
    else:
        print('add do')
        verbphr[0][0] = (lem.lemmatize(verb, pos='v'))
        '''TODO correct form of do based on tense/plurality of verb
            VBG, VBN verb
        '''
        doform = ''
        if verbphr[0].label().endswith('Z'):
            doform += 'Does'
        elif verbphr[0].label().endswith('P'):
            doform += 'Do'
        elif verbphr[0].label().endswith('D'):
            doform += 'Did'
        ques = ''
        for n in verbphr:
            ques += ' ' + ' '.join(n.leaves())
        beg = ''
        for n in subject:
            beg += ' ' + ' '.join(n.leaves())
        ques = doform + beg + ques + '?'
        print(ques)

nlp.close()
