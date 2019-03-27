
import spacy 
from spacy import displacy
from collections import Counter
import en_core_web_sm



def main():
	is_action = False
	actor = ''
	recipient = ''
	action = ''
	nlp = en_core_web_sm.load()
	doc = nlp('All dinosaurs lay amniotic eggs with hard shells made mostly of calcium carbonate.')
	named_entities = [(X.text, X.label_) for X in doc.ents]
	pos = [(X.pos_) for X in doc]
	dep_parse = [(X.text, X.dep_, X.head.text, X.head.pos_,) for X in doc]
	for (t, d, h, pos) in dep_parse:
		if (d=='dobj'):
			is_action = True
			recipient = t
			action = h
	for (t, d, h, pos) in dep_parse:
		if (h==action):
			actor = t
			break
	print(dep_parse)
	print("actor: "+actor+"\n")
	print("action: "+action+"\n")
	print("recipient: "+recipient+"\n")

if __name__ == '__main__':
	main()