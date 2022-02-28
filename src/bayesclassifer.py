import re
import numpy as np
import pandas as pd
from review import tokenize

b_pandas = []
r_dtypes = {"stars": np.float16,
            "useful": np.int32,
            "funny": np.int32,
            "cool": np.int32,
            }


def tokenize(text: str):
    """

    :param text:
    :return:
    """
    tokens = [re.sub(r'[^A-Za-z]+', '', s).lower().strip() for s in  text.split()]
    return tokens


with open("jsons/yelp_small_dataset.json", "r") as f:
    reader = pd.read_json(f, orient="records", lines=True,
                          dtype=r_dtypes, chunksize=1000)

    for chunk in reader:
        reduced_chunk = chunk.drop(columns=['review_id', 'user_id'])
        b_pandas.append(reduced_chunk)

b_pandas = pd.concat(b_pandas, ignore_index=True)

pos_freqs = {}
neg_freqs = {}

for item in b_pandas.iterrows():
    tokens = tokenize(item[1]["text"])
    if item[1]["stars"] >= 4:
        for token in tokens:
            if token not in pos_freqs.keys():
                pos_freqs[token] = 1
            else:
                pos_freqs[token] += 1
    elif item[1]["stars"] <= 2:
        for token in tokens:
            if token not in neg_freqs.keys():
                neg_freqs[token] = 1
            else:
                neg_freqs[token] += 1

print(pos_freqs, neg_freqs)


