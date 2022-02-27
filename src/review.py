import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
API_KEY = os.getenv('API_KEY')


class Review:
    """
    Represents a Yelp review.
    """
    def __init__(self, li):
        divs = li.find_all("div")
        for div in divs:
            if "aria-label" in div.attrs and "star rating" in div.attrs["aria-label"]:
                self.rating = int(div.attrs["aria-label"][0])
        print(li.find("p", {"class": "comment__09f24__gu0rG css-1sufhje"}).text)
        self.text = li.find("p").text


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
        if li.find("p", {"class": "comment__09f24__gu0rG css-1sufhje"}):
            reviews.append(Review(li))

    return reviews


def get_all_yelp_reviews(search_term: str):
    """
    Returns the yelp reviews on every page for a search term

    :param search_term: What user would like to search for
    :return: List of Review objects for every page
    """
    all_reviews = []
    counter = 0
    while True:
        reviews = get_yelp_reviews(search_businesses(search_term)[0]["url"] + f"&start={counter}")
        if len(reviews) == 0:
            return all_reviews
        print(len(reviews))
        all_reviews.append(reviews)
        counter += 10
