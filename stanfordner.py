import nltk
from stanfordcorenlp import StanfordCoreNLP
import sys

#for simple sentences: subj + pred, NP + VP + .
#figure out when sentence form is ^
path = sys.argv[1] #path to stanford corenlp
nlp = StanfordCoreNLP(r'' + path)
sentence = 'Cleopatra was a member of the Ptolemaic dynasty, a Greek family of Macedonian origin that ruled Egypt after Alexander the Great\'s death during the Hellenistic period'
print(nlp.ner(sentence))
nlp.close()