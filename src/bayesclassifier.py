import re
import numpy as np
import pandas as pd
import math
import json


class BayesClassifier:
    def __init__(self):
        self.pos_freqs = {}
        self.neg_freqs = {}
        self.b_pandas = []
        self.r_dtypes = {"stars": np.float16,
                         "useful": np.int32,
                         "funny": np.int32,
                         "cool": np.int32
                         }

    def train(self):
        """
        Adds tokenized text to their respective frequency dictionary

        :return: void
        """
        with open("jsons/yelp_academic_dataset_review.json", "r") as f:
            reader = pd.read_json(f, orient="records", lines=True, dtype=self.r_dtypes,
                                  chunksize=1000000, nrows=1000000)
            for chunk in reader:
                reduced_chunk = chunk.drop(columns=['review_id', 'user_id'])
            self.b_pandas.append(reduced_chunk)

        self.b_pandas = pd.concat(self.b_pandas, ignore_index=True)
        for item in self.b_pandas.iterrows():
            if item[1]["stars"] >= 4:
                add_text_to_frequency_dict(self.pos_freqs, item[1]["text"])
            elif item[1]["stars"] <= 2:
                add_text_to_frequency_dict(self.neg_freqs, item[1]["text"])

    def save(self):
        """
        Writes each frequency dictionary onto a single json file

        :return: void
        """
        data = {"positive": self.pos_freqs, "negative": self.neg_freqs}
        with open("jsons/freqs.json", 'w') as file_write:
            json.dump(data, file_write, indent=4, sort_keys=True)

    def load(self):
        """
        Reads from json file and loads data about positive and negative frequencies to self.pos_freqs and self.neg_freqs

        :return: void
        """
        with open("jsons/freqs.json", 'r') as file_read:
            json_load = json.load(file_read)
            self.pos_freqs = json_load["positive"]
            self.neg_freqs = json_load["negative"]

    def get_likelihood_of_word(self, word: str, is_positive: bool):
        """
        Returns the probability of a word's appearance in a frequency dictionary

        :param word: str
        :param is_positive: bool
        :return: float
        """
        if is_positive:
            if word in self.pos_freqs.keys():
                return (self.pos_freqs[word] + 1) / get_total_words(self.pos_freqs)
            else:
                return 1 / get_total_words(self.pos_freqs)
        else:
            if word in self.neg_freqs.keys():
                return (self.neg_freqs[word] + 1) / get_total_words(self.neg_freqs)
            else:
                return 1 / get_total_words(self.neg_freqs)

    def get_log_likelihood_of_text(self, text, is_positive):
        """

        :param text:
        :param is_positive:
        :return:
        """
        tokens = tokenize(text)
        log_likelihood = 0
        for token in tokens:
            log_likelihood += math.log(self.get_likelihood_of_word(token, is_positive))
        return log_likelihood

    def get_prediction(self, text):
        return self.get_log_likelihood_of_text(text, True) - self.get_log_likelihood_of_text(text, False)

        #if self.get_log_likelihood_of_text(text, True) >= self.get_log_likelihood_of_text(text, False):
        #    return "positive"
        #else:
        #    return "negative"


def tokenize(text: str):
    """

    :param text:
    :return:
    """
    tokens = [re.sub(r'[^A-Za-z]+', '', s).lower().strip() for s in text.split()]
    return tokens


def add_text_to_frequency_dict(freq_dict, text):
    """

    :param freq_dict:
    :param text:
    :return:
    """
    tokens = tokenize(text)
    for token in tokens:
        if token not in freq_dict.keys():
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1


def get_total_words(freq_dict: dict):
    """

    :param freq_dict:
    :return: int: Total number of words in a frequency dictionary
    """
    return sum(freq_dict.values())

a = BayesClassifier()
a.load()
print(a.get_prediction("not good"))