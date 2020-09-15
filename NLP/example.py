# python -m spacy download en_core_web_sm
# pipenv install en_core_web_sm

import spacy

nlp = spacy.load("en_core_web_md")
tokens = nlp("dog cat banana afskfsd")
tokens = nlp('Lonche    (sandwich) of ham (1Pc)')

ttt = ['Text', 'Vec', 'VecNorm', 'OOV']
print(f'{ttt[0]:^12} | {ttt[1]:^5} | {ttt[2]:^7} | {ttt[3]:^5}')
print('-'*40)
for token in tokens:
    print(f'{token.text:^12} | {token.has_vector:^5} | {token.vector_norm:^7.2f} | {token.has_vector:^5}')
    # print(token.text, token.has_vector, token.vector_norm, token.is_oov)

# for token in tokens:
#     print(token.vector)
