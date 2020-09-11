import pandas as pd
import spacy
from spacy.util import minibatch
import random

DATA_SOURCE = './data/yelp_ratings.csv'


def load_data(csv_file, split=0.9):
    data = pd.read_csv(csv_file)

    # Shuffle data
    train_data = data.sample(frac=1, random_state=7)
    # print(train_data.head())

    texts = train_data['text'].values
    labels = [{"POSITIVE": bool(y), "NEGATIVE": not bool(y)}
              for y in train_data['sentiment'].values]
    split = int(len(train_data) * split)

    train_texts = texts[:split]
    train_labels = [{"cats": labels} for labels in labels[:split]]
    val_texts = texts[split:]
    val_labels = [{"cats": labels} for labels in labels[split:]]

    return train_texts, train_labels, val_texts, val_labels


def train(model, train_data, optimizer):
    losses = {}
    random.seed(1)
    random.shuffle(train_data)

    batches = minibatch(train_data, size=8)
    for batch in batches:
        # train_data is a list of tuples [(text0, label0), (text1, label1), ...]
        # Split batch into texts and labels
        texts, labels = zip(*batch)

        # Update model with texts and labels
        model.update(texts, labels, sgd=optimizer, losses=losses)

    return losses


def predict(nlp, texts):
    # Use the tokenizer to tokenize each input text example
    docs = [nlp.tokenizer(text) for text in texts]

    # Use textcat to get the scores for each doc
    textcat = nlp.get_pipe('textcat')
    scores, _ = textcat.predict(docs)

    # From the scores, find the class with the highest score/probability
    print(scores)
    predicted_class = scores.argmax(axis=1)

    return predicted_class


def evaluate(model, texts, labels):
    """ Returns the accuracy of a TextCategorizer model. 

        Arguments
        ---------
        model: ScaPy model with a TextCategorizer
        texts: Text samples, from load_data function
        labels: True labels, from load_data function

    """
    # Get predictions from textcat model
    predicted_class = predict(model, texts)

    # From labels, get the true class as a list of integers (POSITIVE -> 1, NEGATIVE -> 0)
    true_class = [int(each['cats']['POSITIVE']) for each in labels]

    # A boolean or int array indicating correct predictions
    correct_predictions = predicted_class == true_class

    # The accuracy, number of correct predictions divided by all predictions
    accuracy = correct_predictions.mean()

    return accuracy


# %% Loading data
train_texts, train_labels, val_texts, val_labels = load_data(DATA_SOURCE)

# %% Example train data
print('Texts from training data\n', '--'*30)
print('  ', train_texts[0])
print('\nLabels from training data\n', '--'*30)
print('  ', train_labels[0])

# %% Setup NLP
# Create an empty model
nlp = spacy.blank("en")

# Create the TextCategorizer with exclusive classes and "bow" architecture
textcat = nlp.create_pipe(
    "textcat",
    config={
        "exclusive_classes": True,
        "architecture": "bow"})
# Add the TextCategorizer to the empty model
nlp.add_pipe(textcat)

# Add labels to text classifier
label_names = [*train_labels[0]['cats'].keys()][::-1]  # reverse
print('\nLabels:', label_names)
for label in label_names:
    textcat.add_label(label)

# %% Train Function
# Fix seed for reproducibility
spacy.util.fix_random_seed(1)
random.seed(1)

# This may take a while to run!
optimizer = nlp.begin_training()
train_data = list(zip(train_texts, train_labels))
losses = train(nlp, train_data, optimizer)
print(losses['textcat'])

# %% Predict one
text = "This tea cup was full of holes. Do not recommend."
doc = nlp(text)
print('\n Predicting :')
print(doc)
print(doc.cats)

# %% Predicting validation data
texts = val_texts[34:38]
predictions = predict(nlp, texts)

for p, t in zip(predictions, texts):
    print(f"{textcat.labels[p]}: {t} \n")

# %% Evaluate model
accuracy = evaluate(nlp, val_texts, val_labels)
print(f"Accuracy: {accuracy:.4f}")


# %%
# This may take a while to run!
# n_iters = 5
# for i in range(n_iters):
#     losses = train(nlp, train_data, optimizer)
#     accuracy = evaluate(nlp, val_texts, val_labels)
#     print(f"Loss: {losses['textcat']:.3f} \t Accuracy: {accuracy:.3f}")
