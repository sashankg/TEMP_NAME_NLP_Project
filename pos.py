import nltk

text = "My name is Bob and I really like candy."

tokens = nltk.word_tokenize(text)
tags = nltk.pos_tag(tokens)

print(tags)
