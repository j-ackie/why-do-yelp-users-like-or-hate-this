import math
import statistics
from bayesclassifier import BayesClassifier


def positive_measures_of_central_tendency():
    classifier = BayesClassifier()
    classifier.load()
    with open("words/positive-words.txt", 'r') as file_read:
        positive_words = file_read.readlines()

    positive_log_likelihood = []
    min_positive_log_likelihood = math.inf
    max_positive_log_likelihood = -math.inf
    for word in positive_words:
        word = word.rstrip("\n")

        log_likelihood = classifier.get_prediction(word)

        positive_log_likelihood.append(log_likelihood)

        if log_likelihood < min_positive_log_likelihood:
            min_positive_log_likelihood = log_likelihood

        if log_likelihood > max_positive_log_likelihood:
            max_positive_log_likelihood = log_likelihood

    print("-------------------------------------------")
    print("Positive words measures of central tendency")
    print("-------------------------------------------")

    length = len(positive_words)
    average_positive_log_likelihood = sum(positive_log_likelihood) / length
    print("Average:", average_positive_log_likelihood)

    positive_log_likelihood.sort()
    if len(positive_words) % 2 == 0:
        print("Median:", (positive_log_likelihood[length // 2] + positive_log_likelihood[length // 2 - 1]) / 2)
    else:
        print("Median:", positive_log_likelihood[length // 2])

    for i in range(3, 0, -1):
        rounded_positive_log_likelihood = []
        for log in positive_log_likelihood:
            rounded_positive_log_likelihood.append(round(log, i))
        print(f"Mode ({i} decimal digits):", statistics.mode(rounded_positive_log_likelihood))

    print("Min:", min_positive_log_likelihood)
    print("Max:", max_positive_log_likelihood)


def negative_measures_of_central_tendency():
    classifier = BayesClassifier()
    classifier.load()
    with open("words/negative-words.txt", 'r') as file_read:
        negative_words = file_read.readlines()

    negative_log_likelihood = []
    min_negative_log_likelihood = math.inf
    max_negative_log_likelihood = -math.inf
    for word in negative_words:
        word = word.rstrip("\n")

        log_likelihood = classifier.get_prediction(word)

        negative_log_likelihood.append(log_likelihood)

        if log_likelihood < min_negative_log_likelihood:
            min_negative_log_likelihood = log_likelihood

        if log_likelihood > max_negative_log_likelihood:
            max_negative_log_likelihood = log_likelihood

    print("-------------------------------------------")
    print("Negative words measures of central tendency")
    print("-------------------------------------------")

    length = len(negative_words)
    average_negative_log_likelihood = sum(negative_log_likelihood) / length
    print("Average:", average_negative_log_likelihood)

    negative_log_likelihood.sort()
    if len(negative_words) % 2 == 0:
        print("Median:", (negative_log_likelihood[length // 2] + negative_log_likelihood[length // 2 - 1]) / 2)
    else:
        print("Median:", negative_log_likelihood[length // 2])

    for i in range(3, 0, -1):
        rounded_negative_log_likelihood = []
        for log in negative_log_likelihood:
            rounded_negative_log_likelihood.append(round(log, i))
        print(f"Mode ({i} decimal digits):", statistics.mode(rounded_negative_log_likelihood))

    print("Min:", min_negative_log_likelihood)
    print("Max:", max_negative_log_likelihood)


if __name__ == "__main__":
    positive_measures_of_central_tendency()
    negative_measures_of_central_tendency()
