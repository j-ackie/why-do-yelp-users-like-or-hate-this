from src.main import tokenize


def test_tokenize():
    assert tokenize(" A B C") == ['a', 'b', 'c']
    assert tokenize("abc") == ['abc']
    assert tokenize("@@@@ A B C D ##") == ['', 'a', 'b', 'c', 'd', '']


if __name__ == "__main__":
    test_tokenize()
    print("All tests passed.")