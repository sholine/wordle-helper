import string

class PossibleLetters:
    def __init__(self, words_size):
        self.words_size = words_size
        self.word = [list(string.ascii_lowercase) for _ in range(words_size)]
        self.must_have = []

    def print(self):
        print(f"[Word]")
        for i, letters in enumerate(self.word):
            print(f"  [Position {i}] => {letters}")
        print(f"[Must Have] => {''.join(self.must_have)}")
