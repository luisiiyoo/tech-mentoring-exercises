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


class BagOfWords:
    def __init__(self, col_names_features: List[str], max_features: int):
        self.col_names_features = col_names_features
        self.max_features = max_features
        self.__clean_text_data: List[str] = []
        self.__stemm_words_dict: Dict[str, Set] = defaultdict(set)
        self.__features_stemm_words_dict: Dict[str, Set] = dict()
        self.__bow_features: List[str] = []
        self.__bow_vectors: List[List[int]] = []
        self.__vectorizer = None

    def __getTokensWord(self, word: str, language="english") -> List[str]:
        return word_tokenize(word, language)

    def __removeStopWords(self, tokens: List[str], language="english") -> List[str]:
        return [word for word in tokens if word not in stopwords.words(language)]

    def __getBaseWords(self, tokens: List[str]) -> List[str]:
        stemmer = PorterStemmer()
        spell = Speller(lang='en')
        return [spell(stemmer.stem(word))
                for word in tokens]

    def __addSpaceBetweenNumberAndChars(self, word: str) -> str:
        # Add space between number and chars i.e. 3pcs ... 3 pcs
        return re.sub(r'(\d+(\.\d+)?)', r' \1 ', word)

    def __removeNonAlphabeticChars(self, word: str) -> str:
        return re.sub('[^A-Za-z]', ' ', word)

    def __changeAbbreviationsForCompleteWord(self, word: str) -> str:
        return re.sub('pc', 'piece', word)

    def __stemmRawTextList(self, text_list: List[str], feed_stemm_dict: bool = False) -> List[str]:
        clean_text_list: List[str] = []
        for text in text_list:
            # Preprocessing
            text = text.strip().lower()
            text = self.__addSpaceBetweenNumberAndChars(text)
            text = self.__changeAbbreviationsForCompleteWord(text)
            text = self.__removeNonAlphabeticChars(text)
            # Stemming
            tokens = self.__getTokensWord(text)
            clean_tokens = self.__removeStopWords(tokens)
            stemm_clean_tokens = self.__getBaseWords(clean_tokens)

            if feed_stemm_dict:
                for token, stemmed_token in zip(clean_tokens, stemm_clean_tokens):
                    self.__stemm_words_dict[stemmed_token].add(token)

            final_text = " ".join(stemm_clean_tokens)
            clean_text_list.append(final_text)
        return clean_text_list

    def build(self, df: pandas.DataFrame, filter_col_name: str):
        # Get clean stemmed data
        for col_name in self.col_names_features:
            filtered_data = df.loc[df[filter_col_name], col_name]
            diet_texts = filtered_data.astype(str).values.tolist()
            self.__clean_text_data += self.__stemmRawTextList(
                diet_texts, feed_stemm_dict=True)
        # Get Bag of Words
        self.__vectorizer = CountVectorizer(max_features=self.max_features)
        self.__bow_vectors = self.__vectorizer.fit_transform(
            self.__clean_text_data).toarray()
        self.__bow_features = self.__vectorizer.get_feature_names()

        # Keep only the features names in the dict
        for feature in self.__bow_features:
            self.__features_stemm_words_dict[feature] = self.__stemm_words_dict[feature]
        self.printResults()

    def saveResults(self, output_file: str) -> None:
        print(f'\nSaving variables on {output_file}')
        with open(output_file, 'wb') as f:
            pickle.dump([self.__bow_vectors, self.__vectorizer,
                         self.__features_stemm_words_dict], f)

    def vectorizeRawData(self, raw_texts: List[str]):
        cprint(f"\nBoW Features:\n{self.__bow_features}", 'blue')
        clean_texts = self.__stemmRawTextList(raw_texts)
        vectors = self.__vectorizer.transform(clean_texts).toarray()
        for idx, texts in enumerate(zip(raw_texts, clean_texts)):
            raw_text, clean_text = texts
            vector = vectors[idx]
            cprint(f'Raw Text: "{raw_text}"', 'magenta')
            cprint(f'Clean Text: "{clean_text}"', 'cyan')
            print(f'{vector}\n')
        return vectors

    def printResults(self) -> None:
        cprint(
            f'{self.__clean_text_data}\n Len: {len(self.__clean_text_data)}\n', 'green')
        cprint(
            f'{self.__features_stemm_words_dict}\n Len: {len(self.__features_stemm_words_dict)}\n', 'yellow')
        cprint(self.__bow_features, 'blue')
        cprint(self.__bow_vectors, 'blue')
        cprint(
            f'Size: {len(self.__bow_vectors)} * {len(self.__bow_vectors[0])}', 'blue')


# %% Main
FILE_PATH = './data_output/MENU/MENU_Breakfast(2019-12-30_2020-03-20).csv'
COL_NAMES_DATA = ['Regular', 'Light', 'Vegan', 'Vegetarian']
MAX_FEATURES = 30
OUTPUT_FILE_PATH = f'./data_output/BoW/bow_menu_{MAX_FEATURES}_features.pkl'
FILTER_COL_NAME = 'ServiceDay'

df = pandas.read_csv(FILE_PATH, index_col=0)
print(df.head())
print(df.columns)
print()

bow = BagOfWords(COL_NAMES_DATA, MAX_FEATURES)
bow.build(df, FILTER_COL_NAME)
bow.vectorizeRawData(
    [' trivorced chilaquiles; egg tortilla; 1/2 portion of chilaquiles and 1/2 egg tortilla'])
