import pandas as pd
import spacy
from spacy.matcher import PhraseMatcher
from collections import defaultdict


def extractMatches(match):
    _, idxStart, idxEnd = match
    return doc[idxStart:idxEnd].lower_


# Load the SpaCy model
nlp = spacy.blank('en')
matcher = PhraseMatcher(nlp.vocab, attr='LOWER')

menu = ["Cheese Steak", "Cheesesteak", "Steak and Cheese", "Italian Combo", "Tiramisu", "Cannoli",
        "Chicken Salad", "Chicken Spinach Salad", "Meatball", "Pizza", "Pizzas", "Spaghetti",
        "Bruchetta", "Eggplant", "Italian Beef", "Purista", "Pasta", "Calzones",  "Calzone",
        "Italian Sausage", "Chicken Cutlet", "Chicken Parm", "Chicken Parmesan", "Gnocchi",
        "Chicken Pesto", "Turkey Sandwich", "Turkey Breast", "Ziti", "Portobello", "Reuben",
        "Mozzarella Caprese",  "Corned Beef", "Garlic Bread", "Pastrami", "Roast Beef",
        "Tuna Salad", "Lasagna", "Artichoke Salad", "Fettuccini Alfredo", "Chicken Parmigiana",
        "Grilled Veggie", "Grilled Veggies", "Grilled Vegetable", "Mac and Cheese", "Macaroni",
        "Prosciutto", "Salami"]

# %% Load in the data from JSON file
DATA_SOURCE = './data/restaurant.json'
data = pd.read_json(DATA_SOURCE)
# print(data.head())

# Create/Converting a list of tokens for each item in the menu
menu_tokens_list = [nlp(item) for item in menu]
matcher.add("MENU", menu_tokens_list)

# %% Matching on the whole dataset all the menu tokens
# item_ratings is a dictionary of lists. If a key doesn't exist in item_ratings,
# the key is added with an empty list as the value.
item_ratings = defaultdict(list)
for idx, review in data.iterrows():
    doc = nlp(review['text'])
    matches = matcher(doc)

    # Create a set of the items found in the review text
    found_items = set(
        list(map(extractMatches, matches)))

    # Update item_ratings with rating for each item in found_items
    for item in found_items:
        item_ratings[item].append(review['stars'])

# %% Rating menu scores
# Calculate the mean ratings for each menu item as a dictionary
mean_ratings = {item: sum(ratings)/len(ratings)
                for item, ratings in item_ratings.items()}

# Find the worst item, and write it as a string in worst_text. This can be multiple lines of code if you want.
sorted_menu_review_scores = sorted(mean_ratings, key=mean_ratings.get)
worst_item = sorted_menu_review_scores[0]
best_item = sorted_menu_review_scores[-1]

print('WORST item : ', worst_item, '\t MeanScore:', mean_ratings[worst_item])
print('BEST item : ', best_item, '\t MeanScore:', mean_ratings[best_item])

# %% Counting reviews
item_review_counts = {item: len(ratings)
                      for item, ratings in item_ratings.items()}

sorted_review_item_counts = sorted(item_review_counts,
                                   key=item_review_counts.get, reverse=True)
print(f'{len(item_review_counts)} items reviewed from {len(menu)}')
for item in sorted_review_item_counts:
    print(
        f"{item:>25}{item_review_counts[item]:>5} ... {mean_ratings[item]:04.2f} stars")

# %% Worst and Best 10 top
sorted_ratings = sorted(mean_ratings, key=mean_ratings.get)

print("\n\nWorst 10-top rated menu items:")
for item in sorted_ratings[:10]:
    print(
        f"\t{item:20} Ave rating: {mean_ratings[item]:.2f} \tcount: {item_review_counts[item]}")

print("\n\nBest 10-top rated menu items:")
for item in sorted_ratings[-10:]:
    print(
        f"\t{item:20} Ave rating: {mean_ratings[item]:.2f} \tcount: {item_review_counts[item]}")
