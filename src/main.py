import requests
import os
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv('API_KEY')


class Review:
    def __init__(self, review: dict):
        self.rating = review["rating"]
        self.url = review["url"]
        self.text = review["text"]


def search_businesses(search_term: str):
    """
    Returns search results for input
    Helper function for get_yelp_reviews

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

    return result.json()["businesses"]

# Add bool for if they want to query for specific restaurant or not
def get_yelp_reviews(search_term: str):
    """
    Returns the yelp reviews for a search term

    https://www.yelp.com/developers/documentation/v3/business

    :param search_term:
    :return:
    """
    business_id = search_businesses(search_term)[0]["id"]
    url = f"https://api.yelp.com/v3/businesses/{business_id}/reviews"
    headers = {"Authorization": "Bearer {}".format(API_KEY)}

    try:
        result = requests.get(url, headers=headers)
        result.raise_for_status()
    except requests.RequestException:
        return None

    reviews = []
    result = result.json()["reviews"]
    for review in result:
        reviews.append(Review(review))

    return reviews


if __name__ == "__main__":
    print(get_yelp_reviews("Ramen")[2].text)