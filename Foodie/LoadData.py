import pickle
from termcolor import colored, cprint

MAX_FEATURES = 70
FILE_PATH = f'./data_output/BoW/bow_menu_{MAX_FEATURES}_features.pkl'

with open(FILE_PATH, 'rb') as f:
    bow_vectors, vectorizer, stemm_features_names_dict = pickle.load(f)

cprint(stemm_features_names_dict, 'yellow')
cprint(bow_vectors, 'cyan')
cprint(vectorizer.get_feature_names(), 'blue')
