import spacy
nlp = spacy.load('en')

doc = nlp("Tea is healthy and calming, don't you think?")

print(f"Token \t\tLemma \t\tStopword".format('Token', 'Lemma', 'Stopword'))
print("-"*40)
for token in doc:
    print(f"{str(token)}\t\t{token.lemma_}\t\t{token.is_stop}")
