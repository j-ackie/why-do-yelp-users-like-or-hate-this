import re


def tokenize(text):
    """

    :param text:
    :return:
    """
    tokens = [re.sub(r'[^A-Za-z]+', '', s).lower().strip() for s in  text.split()]
    return tokens

#def calc_like(search_term: str):

