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


if __name__ == "__main__":
    print(search_businesses("ramen"))