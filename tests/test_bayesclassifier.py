from src.bayesclassifier import BayesClassifier, tokenize, add_text_to_frequency_dict, get_total_words
import unittest

#class TestBayesClassifier(unittest.TestCase):
#    def


class TestHelperFunctions(unittest.TestCase):
    def test_get_total_words(self):
        self.assertEqual(get_total_words({}), 0)
        self.assertEqual(get_total_words({"word": 4}), 4)
        self.assertEqual(get_total_words({"word": 0}), 0)
        self.assertEqual(get_total_words({"word1": 10, "word2": 8}), 18)
        self.assertEqual(get_total_words({"word1": 10, "word2": 0}), 10)

    def test_add_text_to_frequency_dict(self):
        test_freq_dict = {}
        add_text_to_frequency_dict(test_freq_dict, "word")
        self.assertEqual(test_freq_dict, {"word": 1})

        add_text_to_frequency_dict(test_freq_dict, "word")
        self.assertEqual(test_freq_dict, {"word": 2})

        add_text_to_frequency_dict(test_freq_dict, "otherword")
        self.assertEqual(test_freq_dict, {"word": 2, "otherword": 1})

        add_text_to_frequency_dict(test_freq_dict, "word#$")
        self.assertEqual(test_freq_dict, {"word": 3, "otherword": 1})

        add_text_to_frequency_dict(test_freq_dict, "")
        self.assertEqual(test_freq_dict, {"word": 3, "otherword": 1})

        for i in range(10000):
            add_text_to_frequency_dict(test_freq_dict, "anotherword")
        self.assertEqual(test_freq_dict, {"word": 3, "otherword": 1, "anotherword": 10000})

        test_freq_dict = {}
        add_text_to_frequency_dict(test_freq_dict, "This is a sentence.")
        self.assertEqual(test_freq_dict, {"this": 1, "is": 1, "a": 1, "sentence": 1})

if __name__ == "__main__":
    unittest.main()