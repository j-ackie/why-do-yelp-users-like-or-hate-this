from src.review import search_businesses
import unittest


class TestReviewFunctions(unittest.TestCase):
    def test_search_businesses(self):
        # Expect empty list because zero results
        self.assertEqual(search_businesses("qwertyuiop"), [])

        # Check that top result's name is Cheeky Sandwiches
        self.assertEqual(search_businesses("Sandwich")[0]["name"], "Cheeky Sandwiches")


if __name__ == "__main__":
    unittest.main()