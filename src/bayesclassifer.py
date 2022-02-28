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
        with open("jsons/yelp_small_dataset.json", "r") as f:
            reader = pd.read_json(f, orient="records", lines=True, dtype=self.r_dtypes, chunksize=1000)

            for chunk in reader:
                reduced_chunk = chunk.drop(columns=['review_id', 'user_id'])
                self.b_pandas.append(reduced_chunk)

        self.b_pandas = pd.concat(self.b_pandas, ignore_index=True)
        for item in self.b_pandas.iterrows():
            if item[1]["stars"] >= 4:
                add_text_to_frequency_dict(self.pos_freqs, item[1]["text"])
            elif item[1]["stars"] <= 2:
                add_text_to_frequency_dict(self.neg_freqs, item[1]["text"])

    def save(self, filename):
        data = {"positive": self.pos_freqs, "negative": self.neg_freqs}
        with open("jsons/freqs.json", 'w') as file_write:
            json.dump(data, file_write, indent=4, sort_keys=True)

    def get_likelihood_of_word(self, word, is_positive):
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
        tokens = tokenize(text)
        sum = 0
        for token in tokens:
            sum += math.log(self.get_likelihood_of_word(token, is_positive))

        return sum

    def get_prediction(self, text):
        if self.get_log_likelihood_of_text(text, True) >= self.get_log_likelihood_of_text(text, False):
            return "positive"
        else:
            return "negative"


def tokenize(text: str):
    """

    :param text:
    :return:
    """
    tokens = [re.sub(r'[^A-Za-z]+', '', s).lower().strip() for s in text.split()]
    return tokens


def add_text_to_frequency_dict(freq_dict, text):
    tokens = tokenize(text)
    for token in tokens:
        if token not in freq_dict.keys():
            freq_dict[token] = 1
        else:
            freq_dict[token] += 1


def get_total_words(freq_dict: dict):
    return sum(freq_dict.values())


a = BayesClassifier()
a.train()
print(a.get_prediction("amazing"))
print(a.neg_freqs)




