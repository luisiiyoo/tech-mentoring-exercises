from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from autocorrect import Speller
import pandas
import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')

FILE_PATH = './data_output/MENU/MENU_Breakfast(2019-12-30_2020-03-20).csv'

# %% Import the data
df = pandas.read_csv(FILE_PATH, index_col=0)
# print(df.head())
# print(df.columns)
print()

# %% Cleaning and removing no alphabetic characters
regular_menu = df.loc[(df['ServiceDay'] == True),
                      'Regular'].str.lower().str.strip().astype(str).values.tolist()

# add space between number and chars i.e. 3pcs ... 3 pcs
regular_menu = [re.sub(r'(\d+(\.\d+)?)', r' \1 ', doc) for doc in regular_menu]
# chance pc to piece
regular_menu = [re.sub('pc', 'piece', doc) for doc in regular_menu]
# Remove no alphabetic characters
regular_menu = [re.sub('[^A-Za-z]', ' ', doc) for doc in regular_menu]

example = regular_menu[0]
tokenized_example = word_tokenize(example)

print(f'Original text: "{regular_menu[0]}"', "\n")
print('Tokenized text:', tokenized_example,  '\n')


# %% Remove stop words
tokenized_example = [word for word in tokenized_example if (
    word not in stopwords.words('english'))]
print('Clean text:', tokenized_example, '\n')

# %% Stemming (Finding the base word)
stemmer = PorterStemmer()
spell = Speller(lang='en')
tokenized_example = [spell(stemmer.stem(word)) for word in tokenized_example]
print('Stemmed text:', tokenized_example, '\n')

# %% Generate Final word
final_example = " ".join(tokenized_example)
print('Final text:', final_example, '\n')
