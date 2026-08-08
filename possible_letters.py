import string
import sys

from collections import Counter

class PossibleLetters:
    def __init__(self, words_size):
        self.words_size = words_size
        self.word = [list(string.ascii_lowercase) for _ in range(words_size)]
        self.must_have = {}  # letter -> minimum number of occurrences required
        self.letter_max_count = {}  # letter -> exact number of occurrences allowed (when known)
        self.tested_letters = []

    def __str__(self):
        output = "\033[1;33m[Word]\033[0m\n"
        for i, letters in enumerate(self.word):
            output += f"  [Position {i}] => {letters}\n"
        output += f"\033[1;33m[Must Have]\033[0m => {self.must_have}\n"
        output += f"\033[1;33m[Letter Max Count]\033[0m => {self.letter_max_count}\n"
        output += f"\033[1;33m[Tested Letters]\033[0m => {self.tested_letters}\n"
        return output

    def _apply_heuristics(self):
        # 1st heuristic: if a letter is missing exactly one more occurrence (in "Must have")
        # and there is only 1 other possible position left for it, then we know where it goes!
        for letter, min_count in list(self.must_have.items()):
          if min_count != 1:
              continue
          index_unique_occurrence = None
          for i, letters in enumerate(self.word):
              if letter in letters and len(letters) > 1:
                  if index_unique_occurrence is None:
                      index_unique_occurrence = i
                  else:
                      index_unique_occurrence = None
                      break
          if index_unique_occurrence is not None:
              self.word[index_unique_occurrence] = [letter]
              del self.must_have[letter]

    def update_possible_letters(self, input_string: str):
        """Update all letters remaining possibilities regarding the user's input string

        Args:
            input_string (str): space-separated tokens, one per letter position:
              '-'  : no information for this position
              'X'  (single uppercase letter): letter is at the correct place (green)
              'x'  (single lowercase letter): letter is present but at the wrong place (yellow)
              'x-' (lowercase letter followed by '-'): this occurrence of the letter is not
                    at this position. If the letter has no green/yellow occurrence elsewhere
                    in the same guess, it means the letter is entirely absent from the word.
                    Otherwise, it means the word contains exactly as many occurrences of that
                    letter as there are green/yellow occurrences in this same guess (this is
                    how duplicate letters are handled).
        """
        tokens = input_string.split()

        # First pass: count green/yellow (confirmed) occurrences of each letter in this guess
        confirmed_count = Counter()
        for token in tokens:
            if len(token) == 1 and token.isalpha():
                confirmed_count[token.lower()] += 1

        for i, token in enumerate(tokens):
            if i >= len(self.word) or token == '-':
                continue

            letter = token[0].lower()
            if letter not in self.tested_letters:
                self.tested_letters.append(letter)

            if len(token) == 2 and token[1] == '-':
                # Gray: this specific occurrence is not at this position
                if letter in self.word[i]:
                    self.word[i].remove(letter)
                if confirmed_count[letter] == 0:
                    # No other occurrence of this letter elsewhere in the guess: absent from the word
                    for possibilities in self.word:
                        if len(possibilities) > 1 and letter in possibilities:
                            possibilities.remove(letter)
                else:
                    # The word contains exactly this many occurrences of the letter
                    self.letter_max_count[letter] = confirmed_count[letter]
            elif token.islower():
                # Yellow: present in the word, but not at this position
                if letter in self.word[i]:
                    self.word[i].remove(letter)
                self.must_have[letter] = max(self.must_have.get(letter, 0), confirmed_count[letter])
            elif token.isupper():
                # Green: correct position
                self.word[i] = [letter]
                self.must_have[letter] = max(self.must_have.get(letter, 0), confirmed_count[letter])

        self._apply_heuristics()

        if "-v" in sys.argv or "--verbose" in sys.argv:
            print(self)

    def generate_regex_from_letters(self):
        regex = '^'
        for possibilities in self.word:
            if len(possibilities) == 1:
                regex += possibilities[0] # Add the only possible letter at this place
            else:
                regex += '[' + ''.join(possibilities) + ']'  # Add all possible letters at this place
        regex += '$'
        if "-v" in sys.argv or "--verbose" in sys.argv:
            print("Regex : [", regex, "]")
        return regex
