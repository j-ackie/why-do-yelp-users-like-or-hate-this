import requests
import os
import json
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from bayesclassifier import BayesClassifier, tokenize

load_dotenv()
API_KEY = os.getenv('API_KEY')


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

    :param search_term: What user would like to search for
    :return: Dictionary containing all the businesses pertaining to search term
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

    :param url: Yelp url of search term
    :return: List of Review objects for a single page
    """

    print("Loading " + url)
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
        p = li.find("p", {"class": "comment__09f24__gu0rG css-1sufhje"})
        if p:
            reviews.append(Review(li, p))

    return reviews


def get_all_yelp_reviews(search_term: str, max_depth: int):
    """
    Returns the yelp reviews on every page for a search term

    :param search_term: What user would like to search for
    :param max_depth:
    :return: List of Review objects for every page
    """
    all_reviews = []
    counter = 0
    while True:
        if counter / 10 > max_depth:
            return all_reviews
        reviews = get_yelp_reviews(search_businesses(search_term)[0]["url"] + f"&start={counter}")
        print(reviews)
        if len(reviews) == 0:
            return all_reviews
        print(len(reviews))
        all_reviews.append(reviews)
        counter += 10


def add_to_freqs(search_term: str, max_depth: int):
    """
    :param search_term:
    :param max_depth:
    :return:
    """
    a = BayesClassifier()
    a.load()

    with open("words/common-words.txt", 'r') as file_read:
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


def save_freqs(search_term: str, max_depth: int):
    """

    :param search_term:
    :param max_depth:
    :return:
    """
    freqs = add_to_freqs(search_term, max_depth)
    with open("jsons/" + search_businesses(search_term)[0]["alias"] + ".json", 'w') as file_write:
        json.dump(freqs, file_write, indent=4)


def load_freqs(search_term: str, max_depth=5):
    """

    :param search_term:
    :return:
    """
    print(search_businesses(search_term))
    name = search_businesses(search_term)[0]["alias"]
    if not os.path.isfile("jsons/" + name + ".json"):
        save_freqs(search_term, max_depth)
    with open("jsons/" + name + ".json", 'r') as file_read:
        freqs = json.load(file_read)
        pos_freqs = sorted(freqs["positive"].items(), key=lambda x: x[1], reverse=True)
        neg_freqs = sorted(freqs["negative"].items(), key=lambda x: x[1], reverse=True)
        return {"positive": pos_freqs, "negative": neg_freqs}
