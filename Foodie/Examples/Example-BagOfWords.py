import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from autocorrect import Speller
import pandas
import re
from typing import List, Dict, Set
from collections import defaultdict
from termcolor import colored, cprint
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import pickle

nltk.download('punkt')
nltk.download('stopwords')

FILE_PATH = './data_output/MENU/MENU_Breakfast(2019-12-30_2020-03-20).csv'
COL_NAMES_DATA = ['Regular', 'Light', 'Vegan', 'Vegetarian']
MAX_FEATURES = 30
OUTPUT_FILE_PATH = f'./data_output/BoW/bow_menu_{MAX_FEATURES}_features.pkl'

df = pandas.read_csv(FILE_PATH, index_col=0)
print(df.head())
print(df.columns)
print()

stemmer = PorterStemmer()
spell = Speller(lang='en')

data: List[str] = []
stemm_words_dict = defaultdict(set)

for col_name in COL_NAMES_DATA:
    # get data by diet
    diet_menus = df.loc[(df['ServiceDay'] == True), col_name].str.lower(
    ).str.strip().astype(str).values.tolist()

    # add space between number and chars i.e. 3pcs ... 3 pcs
    diet_menus = [re.sub(r'(\d+(\.\d+)?)', r' \1 ', doc)
                  for doc in diet_menus]
    # chance pc to piece
    diet_menus = [re.sub('pc', 'piece', doc) for doc in diet_menus]
    # Remove no alphabetic characters
    diet_menus = [re.sub('[^A-Za-z]', ' ', doc) for doc in diet_menus]

    for menu in diet_menus:
        # tokenize the menu
        tokenized_menu = word_tokenize(menu)
        # Remove stop words
        clean_tokenized_menu = [word for word in tokenized_menu if (
            word not in stopwords.words('english'))]

        # Stemming (Finding the base word)
        stemm_clean_tokenized_menu = [spell(stemmer.stem(word))
                                      for word in clean_tokenized_menu]

        # The Menu is mixed English and Spanish
        for word, stemmed_word in zip(clean_tokenized_menu, stemm_clean_tokenized_menu):
            stemm_words_dict[stemmed_word].add(word)

        # Generate final word
        final_menu = " ".join(stemm_clean_tokenized_menu)
        # Add the menu to the list of data
        data.append(final_menu)

# %% Get Bag of Wordss
vectorizer = CountVectorizer(max_features=MAX_FEATURES)
bow_vectors = vectorizer.fit_transform(data).toarray()  # numpy.array()
bow_features_names = vectorizer.get_feature_names()

# %% Keep the features names in the dict
stemm_features_names_dict: Dict[str, Set] = dict()
for feature_name in bow_features_names:
    stemm_features_names_dict[feature_name] = stemm_words_dict[feature_name]

cprint(f'{data}\n Len: {len(data)}\n', 'green')
cprint(f'{stemm_features_names_dict}\n Len: {len(stemm_features_names_dict)}\n', 'yellow')

cprint(bow_features_names, 'blue')
cprint(bow_vectors, 'blue')
cprint(f'Size: {len(bow_vectors)} * {len(bow_vectors[0])}', 'blue')


# %% Test new input data
example = 'spice foreleg burrito piece scramble egg turkey chorizo burrito portion scramble egg'
test = vectorizer.transform(
    [example]).toarray()
cprint(f'\nText_sample: "{example}"', 'red')
cprint(f'{test}', 'green')
cprint(bow_features_names, 'blue')

# %% Save Data
print(f'\nSaving variables on {OUTPUT_FILE_PATH}')
with open(OUTPUT_FILE_PATH, 'wb') as f:
    pickle.dump([bow_vectors, vectorizer, stemm_features_names_dict], f)
