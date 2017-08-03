import numpy as np
import sklearn.linear_model as linear
import sklearn.naive_bayes as bayes
import sklearn.neural_network as neural
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score


def k_fold_cv(k, data, classifier=SVC()):
    # type: (int, tuple) -> list
    """
    Performs k-fold cross-validation using a designated
    classifier.

    :param k: Number of bins to generate from data.
    :param data: Tuple of samples and their labelsf as arrays.
    :param classifier: Machine learning classifier to use.
    :return: A list of all accuracy scores gotten from each bin.
    """
    scores = []
    x_folds = np.array_split(data[0], k)
    y_folds = np.array_split(data[1], k)
    for i in range(k):
        training_x = list(x_folds).pop(i)
        training_y = list(y_folds).pop(i)
        test_x = x_folds[i]
        test_y = y_folds[i]
        classifier.fit(training_x, training_y)
        scores.append(accuracy_score(test_y, classifier.predict(test_x)))
    return scores


def model_comparison_classification(k, data):
    # type: (int, tuple) -> dict
    """
    Compares various classification models and
    their performance in analyzing a dataset
    using k-fold cross-validation.

    :param k: How many bins.
    :param data: Data of samples and their labels.
    :return: A dictionary with keys being names
             of classifiers and values being the
             k bins and their accuracy scores.
    """
    models = {clf: None for clf in ['SVM', 'Passive-Agressive',
                                    'Bernoulli', 'Multilayered Perceptron']}
    # Data for k-fold cross-validation on various models.
    cv_results = [k_fold_cv(k, data, c) for c in [SVC(),
                                                  linear.PassiveAggressiveClassifier(),
                                                  bayes.BernoulliNB(),
                                                  neural.MLPClassifier()]]
    models['SVM'] = cv_results[0]
    models['Passive-Agressive'] = cv_results[1]
    models['Bernoulli'] = cv_results[2]
    models['Multilayered Perceptron'] = cv_results[3]

    return models


def plot_model_comparison(data, title, xlab, ylab):
    for k in data:
        plt.plot(data[k], label=k)
    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.legend()
    plt.show()
