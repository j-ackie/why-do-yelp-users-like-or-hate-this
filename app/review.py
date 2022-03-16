import requests
import os
import json
from config import API_KEY
from bs4 import BeautifulSoup
from app.bayesclassifier import BayesClassifier, tokenize


class Review:
    """
    Represents a Yelp review.
    """
    def __init__(self, li, p):
        divs = li.find_all("div")
        for div in divs:
            if "aria-label" in div.attrs and "star rating" in div.attrs["aria-label"]:
                self.rating = int(div.attrs["aria-label"][0])
                break
        self.text = p.text


def search_businesses(search_term: str):
    """
    Returns search results for input.
    Helper function for get_yelp_reviews.

    https://www.yelp.com/developers/documentation/v3/business_search

    :param search_term: (str) What user would like to search for
    :return: (dict) Dictionary containing all the businesses pertaining to search term
    """
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "Bearer {}".format(API_KEY)}
    params = {"term": search_term,
              "location": "New York City"}
    try:
        result = requests.get(url, headers=headers, params=params)
        result.raise_for_status()
    except requests.RequestException:
        print("Search business error")
        return None

    return result.json()["businesses"]


def get_yelp_reviews(url: str):
    """
    Returns the yelp reviews on a single page for a search term.
    Helper function for get_all_yelp_reviews.

    :param url: (str) Yelp url of search term
    :return: (list) List of Review objects for a single page
    """
    try:
        result = requests.get(url)
        result.raise_for_status()
    except requests.RequestException:
        print("ERROR")
        return None

    soup = BeautifulSoup(result.content, "html.parser")

    reviews = []

    list_items = soup.find_all("li", {"class": "margin-b5__09f24__pTvws border-color--default__09f24__NPAKY"})
    for li in list_items:
        p = li.find("p", {"class": "comment__09f24__gu0rG css-qgunke"})
        if p:
            reviews.append(Review(li, p))

    return reviews


def get_all_yelp_reviews(search_term: str, max_depth: int):
    """
    Returns the yelp reviews on every page for a search term.

    :param search_term: (str) What the user would like to search for
    :param max_depth: (int) Maximum number of pages
    :return: (list) List of Review objects for every page
    """
    all_reviews = []
    counter = 0
    while True:
        if counter / 10 > max_depth:
            return all_reviews
        reviews = get_yelp_reviews(search_businesses(search_term)[0]["url"] + f"&start={counter}")
        if len(reviews) == 0:
            return all_reviews
        all_reviews.append(reviews)
        counter += 10


def add_to_freqs(search_term: str, max_depth: int):
    """
    Adds the tokens of every review within the max depth to the frequency dictionaries.

    :param search_term: (str) What the user would like to search for
    :param max_depth: (int) Maximum number of pages
    :return: (dict) Dictionary containing both positive and negative frequency dictionaries.
    """ 
    a = BayesClassifier()
    a.load()

    with open("app/resources/words/common-words.txt", 'r') as file_read:
        common_words = file_read.readlines()

    stripped_common_words = []
    for word in common_words:
        stripped_common_words.append(word.rstrip("\n"))

    pos_freqs = {}
    neg_freqs = {}
    all_review_pages = get_all_yelp_reviews(search_term, max_depth)
    for review_page in all_review_pages:
        for review in review_page:
            tokens = tokenize(review.text)
            for token in tokens:
                if a.get_prediction(token) > 0.5 and review.rating >= 4 and token not in stripped_common_words:
                    if token not in pos_freqs.keys():
                        pos_freqs[token] = 1
                    else:
                        pos_freqs[token] += 1
                elif a.get_prediction(token) < -0.75 and review.rating <= 2 and token not in stripped_common_words:
                    if token not in neg_freqs.keys():
                        neg_freqs[token] = 1
                    else:
                        neg_freqs[token] += 1

    return {"positive": pos_freqs, "negative": neg_freqs}


def save_freqs(search_term: str, max_depth: int, alias: str):
    """
    Saves the frequency dictionaries in a JSON.

    :param search_term: (str) What the user would like to search for
    :param max_depth: (int) Maximum number of pages
    :param alias: (str) Alias of business given from call of Yelp Fusion API
    :return: (void)
    """
    freqs = add_to_freqs(search_term, max_depth)
    with open("app/resources/businesses-jsons/" + alias + ".json", 'w') as file_write:
        json.dump(freqs, file_write, indent=4)


def load_freqs(search_term: str, max_depth=5):
    """
    Loads the frequency dictionaries from a JSON.

    :param search_term: (str) What the user would like to search for
    :return: (dict) Dictionary containing both positive and negative frequency dictionaries
    """
    search = search_businesses(search_term)
    if len(search) == 0:
        return None
    top_result = search[0]
    alias = top_result["alias"]
    name = top_result["name"]
    business_url = top_result["url"]
    if not os.path.isfile("app/resources/businesses-jsons/" + alias + ".json"):
        save_freqs(search_term, max_depth, alias)
    with open("app/resources/businesses-jsons/" + alias + ".json", 'r') as file_read:
        freqs = json.load(file_read)
        pos_freqs = sorted(freqs["positive"].items(), key=lambda x: x[1], reverse=True)
        neg_freqs = sorted(freqs["negative"].items(), key=lambda x: x[1], reverse=True)
        return name, business_url, {"positive": pos_freqs, "negative": neg_freqs}
