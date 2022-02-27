import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup


load_dotenv()
API_KEY = os.getenv('API_KEY')


class Review:
    def __init__(self, review):
        divs = review.find_all("div")
        for div in divs:
            if "aria-label" in div.attrs and "star rating" in div.attrs["aria-label"]:
                self.rating = int(div.attrs["aria-label"][0])
        self.text = review.find("p", {"class": "comment__09f24__gu0rG css-1sufhje"}).text


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
        result = requests.get(url, headers=headers, params=params, timeout=10)
        result.raise_for_status()
    except requests.RequestException:
        return None

    return result.json()["businesses"]

# Add bool for if they want to query for specific restaurant or not
def get_yelp_reviews(url: str):
    """
    Returns the yelp reviews for a search term
    Helper function
    :param url:
    :return:
    """

    print("Loading " + url)
    try:
        result = requests.get(url, timeout=10)
        result.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(result.content, "html.parser")

    reviews = soup.find_all("li", {"class": "margin-b5__09f24__pTvws border-color--default__09f24__NPAKY"})

    cleaned_reviews = []
    for review in reviews:
        cleaned_reviews.append(Review(review))

    return cleaned_reviews


def get_all_yelp_reviews(search_term: str):
    """

    :param search_term:
    :return:
    """
    all_reviews = []
    counter = 0
    while True:
        reviews = get_yelp_reviews(search_businesses(search_term)[0]["url"] + f"&start={counter}")
        if len(reviews) == 0:
            return all_reviews
        all_reviews.append(reviews)
        counter += 10


if __name__ == "__main__":
    print(get_all_yelp_reviews("McDonalds")[0][0].text)