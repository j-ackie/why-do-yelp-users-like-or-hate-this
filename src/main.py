import requests
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')


class Review:
    def __init__(self, rating, text):
        self.rating = rating
        self.text = text


def search_businesses(search_term: str):
    """
    Returns search results for input

    https://www.yelp.com/developers/documentation/v3/business_search
    :param search_term: What user would like to search for
    :return:
    """
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": "Bearer {}".format(API_KEY)}
    params = {"term": search_term,
              "location": "New York City"}
    try:
        result = requests.get(url, headers=headers, params=params, timeout=5)
        result.raise_for_status()
    except requests.RequestException:
        return None

    return result.json()


def get_yelp_reviews(business_id: str):
    """
    Returns the yelp reviews for a particular business

    https://www.yelp.com/developers/documentation/v3/business

    :param business_id:
    :return:
    """
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    headers = {"Authorization": "Bearer {}".format(API_KEY)}

    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
    except requests.RequestException:
        return None

    return result.json()


if __name__ == "__main__":
    #print(get_yelp_reviews(search_businesses("Ramen")["businesses"][0]["id"]))