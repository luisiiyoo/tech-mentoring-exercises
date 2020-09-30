import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from autocorrect import Speller
import pandas
import re
from typing import List, Dict, Set
from collections import defaultdict
from termcolor import colored, cprint
from sklearn.feature_extraction.text import CountVectorizer
import numpy
import pickle
import os


nltk.download('punkt')
nltk.download('stopwords')


class BagOfWords:
    '''
    BagOfWords class to extract features form raw text

    Args:
        col_names_features (List[str]): Data frame columns names to extract from the raw data
        max_features (int): Maximun possible number of features to extract

    Attributes:
        col_names_features (List[str]): Data frame columns names to extract from the raw data
        max_features (int): Maximun possible number of features to extract
        __clean_text_data (List[str]): Corpus of cleaned texts to get the features and vectors
        __stemm_words_dict (Dict[str, Set]): All the steammed words as keys and their original words
        __features_stemm_words_dict (Dict[str, Set]): Steammed words (only the features) as keys and their original words
        __bow_features (List[str]): The N-most frequent words on the corpus
        __bow_vectors (List[List[int]]): Vector for each cleaned text
        __vectorizer (CountVectorizer): CountVectorizer object used to transform cleaned text to vector representation
    '''

    def __init__(self, col_names_features: List[str], max_features: int):
        self.col_names_features = col_names_features
        self.max_features = max_features
        self.__clean_text_data: List[str] = []
        self.__stemm_words_dict: Dict[str, Set] = defaultdict(set)
        self.__features_stemm_words_dict: Dict[str, Set] = dict()
        self.__bow_features: List[str] = []
        self.__bow_vectors: List[List[int]] = []
        self.__vectorizer: CountVectorizer = None

    def getStemmedWordsDict(self) -> Dict[str, Set]:
        '''
        Gets all the steammed words as keys and their original words

        Args:
            None

        Returns:
            stemm_words_dict (Dict[str, Set]): All the steammed words as keys and their original words
        '''
        return self.__stemm_words_dict

    def getFeaturesStemmedWordsDict(self) -> Dict[str, Set]:
        '''
        Gets the steammed features as keys and their original words as a values

        Args:
            None

        Returns:
            features_stemm_words_dict (Dict[str, Set]): Steammed features as keys and their original word
        '''
        return self.__features_stemm_words_dict

    def getFeatures(self) -> List[List[int]]:
        '''
        Gets the the N-most frequent words on the corpus

        Args:
            None

        Returns:
            bow_features (List[str]): The N-most frequent words on the corpus
        '''
        return self.__bow_features

    def getVectors(self) -> List[List[int]]:
        '''
        Gets the vectors obtained after fit and transform the courpus to BoW

        Args:
            None

        Returns:
            bow_vectors (List[List[int]]): Vector for each cleaned text used in the corpus
        '''
        return self.__bow_vectors

    def getVectorizer(self) -> CountVectorizer:
        '''
        Gets the CountVectorizer object used to transform cleaned text to vector representation

        Args:
            None

        Returns:
            vectorizer (CountVectorizer): CountVectorizer object used to transform cleaned text to vector representation
        '''
        return self.__vectorizer

    def __getTokensWord(self, word: str, language="english") -> List[str]:
        '''
        Gets the a list of tokes given a word

        Args:
            word (str): Word to tokenize
            language (str): Language to use

        Returns:
            tokens (List[str]): List of tokens obtained from the word
        '''
        return word_tokenize(word, language)

    def __removeStopWords(self, tokens: List[str], language="english") -> List[str]:
        '''
        Gets the a list of tokens that not includes stop words

        Args:
            tokens (List[str]): List of tokens
            language (str): Language to use

        Returns:
            tokens (List[str]): List of tokens that not includes stop words
        '''
        return [word for word in tokens if word not in stopwords.words(language)]

    def __getBaseWords(self, tokens: List[str], stemm_lang="english", spell_lang="en") -> List[str]:
        '''
        Gets a list of stemmed tokends (base word for each token)

        Args:
            tokens (List[str]): List of tokens
            stemm_lang (str): Language to use on the stemm process
            spell_lang (str): Language to use on the spell check process

        Returns:
            stemmed_tokens (List[str]): List of stemmed tokens
        '''
        stemmer = SnowballStemmer(stemm_lang)
        spell = Speller(lang=spell_lang)
        return [spell(stemmer.stem(word))
                for word in tokens]

    def __addSpaceBetweenNumberAndChars(self, word: str) -> str:
        '''
        Adds space between char and number (and vice cversa) if they are together.
        i.e. Adds space between number and chars 3pcs ... 3 pcs

        Args:
            word (str): word to apply the change

        Returns:
            new_word (str): New word with space between char and number (and vice cversa) if they are together
        '''
        return re.sub(r'(\d+(\.\d+)?)', r' \1 ', word)

    def __removeNonAlphabeticChars(self, word: str) -> str:
        '''
        Gets a new string with only alphabetic characters

        Args:
            word (str): Word to apply the change

        Returns:
            new_word (str): String with only alphabetic characters
        '''
        return re.sub('[^A-Za-z]', ' ', word)

    def __changeAbbreviationsForCompleteWord(self, word: str) -> str:
        '''
        Replaces abbreviations in a text. i.e: 'pc' -> 'piece'

        Args:
            word (str): Word to apply the change

        Returns:
            new_word (str): String with no abbreviations
        '''
        return re.sub('pc', 'piece', word)

    def __stemmRawTextList(self, text_list: List[str], feed_stemm_dict: bool = False) -> List[str]:
        '''
        Transforms a list of raw text into a list of clean steammed text for vectorize 

        Args:
            text_list (List[str]): List of raw text
            feed_stemm_dict (bool): Flag to feed the stemm dictionary

        Returns:
            stemm_text_list (List[str]): List of steammed text for vectorize 
        '''
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

    def build(self, df: pandas.DataFrame, filter_col_name: str) -> None:
        '''
        Extracts the text from a data frame and creates the bow features and vectors from the whole corpus

        Args:
            df (pandas.DataFrame): Data frame to extract the text
            filter_col_name (str): Column name to filter data

        Returns:
            None
        '''
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

    def vectorizeRawData(self, raw_texts: List[str]) -> List[List[int]]:
        '''
        Vectorizes a list of raw text

        Args:
            raw_texts (List[str]): List of raw text

        Returns:
            vectors (List[List[int]]): Vectors for each input list row
        '''
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

    def saveResults(self, full_path_file: str) -> None:
        '''
        Saves the instance in a pkl file

        Args:
            full_path_file (str): Complete path and file name where will be saved the file

        Returns:
            None
        '''
        print(f'\nSaving variables on {full_path_file}')
        output_path, output_file = os.path.split(full_path_file)

        if output_path and not os.path.isdir(output_path):
            try:
                os.makedirs(output_path)  # os.mkdir for one directory only
            except OSError:
                print("Creation of the directory %s failed" % output_path)
            else:
                print("Successfully created the directory %s " % output_path)
        with open(full_path_file, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
