"""
python is Anaconda (32-bit), python64 is Python (64-bit).
Must be run under Windows 10 with these installations.
Subprocess is used to call python from python64 to avoid
environment compatibility issues between spaCy and naoqi.
"""

import en_vectors_glove_md as spacy_model
from pickle import load
from numpy import array
from subprocess import call  # Use later to call gesture_suite.py.
from sklearn.linear_model import SGDClassifier


class LanguageProcessing():

    def __init__(self):
        # Machine learning models.
        self.nlp = spacy_model.load()
        self.model = SGDClassifier()
        # Preprocessing the corpus.
        # self.corpus: Map<String, List<String>>
        self.corpus = load(open('pickles/speech_corpus', 'rb'))
        self.categories = self.corpus.keys()
        self.classifications_by_cat = {self.categories[i]: i
                                       for i in range(len(self.categories))}
        self.classifications_by_num = {i: self.categories[i]
                                       for i in range(len(self.categories))}
        # Training the model.
        training_x = []
        training_y = []
        for k in self.corpus:
            sentences = self.corpus[k]
            training_x += [self.return_nlp(s).vector for s in sentences]
            training_y += [self.classifications_by_cat[k]
                           for i in range(len(sentences))]
        self.model.fit(array(training_x), array(training_y))

    def return_nlp(self, text):
        """
        Wraps given text in unicode and
        returns its spaCy wrapper.
        """
        return self.nlp(unicode(text))

    def string_similarity(self, s1, s2):
        """
        Using spaCy, computes the similarity
        between two strings based on the
        GloVe vectors provided.
        """
        return self.return_nlp(s1).similarity(self.return_nlp(s2))

    def train_with_query(self, query):
        pred = self.model.predict(
            array(self.return_nlp(query).vector))[0]
        # Inform the user of the prediction and
        # ask for confirmation of training. To be removed later.
        print 'QUERY:', query
        print 'CLASSIFIED AS:', self.classifications_by_num[pred]
        decision = raw_input('Is this what you expected? 0 for N, 1 for Y.\n> ')
        if eval(decision) == 1:
            # Update the corpus and train the model.
            self.corpus[self.classifications_by_num[pred]].append(query)
            self.model.partial_fit(array([self.return_nlp(query).vector]),
                                   array([self.classifications_by_num[pred]]))
