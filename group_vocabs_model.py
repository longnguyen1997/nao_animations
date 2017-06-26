import spacy
import pickle
from read_animations import grouped_tags

# Load medium-sized corpus/model for vocabulary analysis.
nlp = spacy.load("en_vectors_glove_md")
vocabulary = nlp.vocab

def sim(a, b):
    '''
    Computes the vector similarity between
    phrase a and phrase b.
    :return: Similarity weight.
    '''
    return nlp(unicode(a)).similarity(b)

def sim_to_list(w1, other_words, threshold):
    '''
    Checks if a word is similar
    within a certain threshold of all other
    words in a given list.
    :param w1: Word to check against list.
    :param other_words: List to check word against.
    :param threshold: How similar w1 must be to any
                      of the words in other_words.
    :return: True if sim(w1, w_x) >= threshold for any w_x in
             other_words, else False.
    '''
    for w2 in other_words:
        if sim(w2, w1) >= threshold: return True

# Generate the 9 vocabulary lists that will be classified per section.
# Data to be used in training learning model later on.
vocab_data = {}

greeting = set([w for w in vocabulary
                 if sim_to_list(w, ["hello", "goodbye", "greetings", "hey there!", "hi"], 0.75)])
self = set([w for w in vocabulary
            if sim_to_list(w, ["me", "I", "my", "our", "this"], 0.8)])
uncertain = set([w for w in vocabulary
                 if sim_to_list(w, grouped_tags['uncertain'], 0.75)])
disagree = set([w for w in vocabulary
                if sim_to_list(w, ["no", "not", "nah", "never", "definitely not", "no, thanks"], 0.75)])
other = set([w for w in vocabulary
             if sim_to_list(w, ["you", "your", "that", "their"], 0.8)])
tell = set([w for w in vocabulary
             if sim_to_list(w, grouped_tags['tell'], 0.75)])
ask = set([w for w in vocabulary
             if sim_to_list(w, grouped_tags['ask'], 0.6)])
agree = set([w for w in vocabulary
             if sim_to_list(w, grouped_tags['agree'], 0.73)])
good = set([w for w in vocabulary
            if sim_to_list(w, grouped_tags['good'] + ['excited'], 0.73)])

vocab_data['agree'] = agree
vocab_data['greeting'] = greeting
vocab_data['good'] = good
vocab_data['self'] = self
vocab_data['uncertain'] = uncertain
vocab_data['disagree'] = disagree
vocab_data['other'] = other
vocab_data['tell'] = tell
vocab_data['ask'] = ask

with open('pickles/vocab_data.pickle', 'wb') as handle:
    pickle.dump(vocab_data, handle, protocol=pickle.HIGHEST_PROTOCOL)

# ---------------------------------------------- #

from sklearn.neural_network import MLPClassifier

# Load machine learning model.
model = MLPClassifier()

train_x = []; train_labels = []
for k in vocab_data:
    train_x.extend([w.vector for w in vocab_data[k]])
    for i in range(len(vocab_data[k])):
        train_labels.append(k)

model.fit(train_x, train_labels)

with open('pickles/perceptron.pickle', 'wb') as handle:
    pickle.dump(model, handle, protocol=pickle.HIGHEST_PROTOCOL)
