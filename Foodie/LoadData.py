import pickle
from termcolor import colored, cprint
from FeatureExtraction.BagOfWords import BagOfWords

MAX_FEATURES = 50
FILE_PATH = f'./data_output/BoW/bow_breakfast_{MAX_FEATURES}_features.pkl'
# FILE_PATH = f'./data_output/BoW/bow_lunch_{MAX_FEATURES}_features.pkl'

bow: BagOfWords = None
with open(FILE_PATH, 'rb') as f:
    bow = pickle.load(f)

cprint(bow.getFeaturesStemmedWordsDict(), 'yellow')
cprint(bow.getFeatures(), 'blue')
cprint(bow.getVectors(), 'cyan')
cprint(f'{len(bow.getVectors())}*{len(bow.getVectors()[0])}', 'cyan')

bow.vectorizeRawData(
    [' mexican groundbeef picadillo side dishes:  red rice / refried beans',
     ' red porkrind tacos (tacos de chicharrón); scrambled eggs with turkey ham;1/2 portion of porkrind and 1/2 portion of scrambled eggs'])
