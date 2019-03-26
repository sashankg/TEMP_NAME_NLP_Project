import spacy 
from spacy import displacy
from collections import Counter
import en_core_web_sm

def detQuestionTypes(named_entities, types_mapped):
	q_categories = {"who": [], "what": [], "where": [], "when": [], "how": []}
	for (word, label) in named_entities:
		for c in types_mapped:
			if (label in (types_mapped[c])):
				q_categories[c].append(word)
	print(q_categories)

def main():
	nlp = en_core_web_sm.load()
	doc = nlp('European authorities fined Google a record $5.1 billion on Wednesday for abusing its power in the mobile phone market and ordered the company to alter its practices')
	named_entities = [(X.text, X.label_) for X in doc.ents]
	entity_types_mapped = {"who": set(["NORP", "ORG", "PERSON"]), "when": set(["DATE"]), "where": set(["FAC", "GPE"])}
	detQuestionTypes(named_entities, entity_types_mapped)
	print(named_entities)


if __name__ == '__main__':
	main()