import string
import re
import os

from collections import Counter

from possible_letters import PossibleLetters

# Compute word scoring using French letters frequency and letters reuse

class WordFilter:
    def __init__(self, file_path: string):
        with open(file_path, 'r') as file:
            self.all_words = [word.strip().lower() for word in file.readlines()]
        self.filtered_words = []
        self.most_discriminant_words = []
    
    def filter_words(self, possible_letters: PossibleLetters):
        self.filtered_words = self.all_words

        # First filtering on possible remaining letters
        regex = possible_letters.generate_regex_from_letters()
        compiled_regex = re.compile(regex)
        self.filtered_words = filter(lambda word: compiled_regex.match(word), self.filtered_words)
        #print("First filter : ", len(filtered_words))

        # Second filtering: words MUST contains some letters
        must_have = possible_letters.must_have
        self.filtered_words = filter(lambda word: all(letter in word for letter in must_have), self.filtered_words)
        #print("Second filter : ", len(filtered_words))

        return self.filtered_words

    def _compute_word_score(self, word):
        # French letters frequencies
        letters_frequency = {
            'e': 14.715,
            'a': 7.636,
            's': 7.245,
            'i': 6.311,
            'n': 6.311,
            't': 5.697,
            'r': 5.68,
            'u': 5.68,
            'l': 5.451,
            'o': 5.102,
            'd': 3.669,
            'c': 3.384,
            'm': 2.968,
            'p': 2.921,
            'v': 1.628,
            'g': 1.268,
            'f': 1.066,
            'b': 0.901,
            'q': 0.866,
            'h': 0.737,
            'x': 0.597,
            'j': 0.173,
            'y': 0.166,
            'z': 0.083,
            'w': 0.045,
            'k': 0.022,
        }

        score = 0
        used_letters = set()
        for letter in word:
            score += letters_frequency.get(letter, 0)
            used_letters.add(letter)

        # Bonus if number of used letters is low (3 is my magic sauce...)
        score += len(used_letters) * 3

        # Malus if the word contains too many 'e' (because the 'e' is crushing other letters in terms of frequency)
        if word.count('e') >= 3: score -= 15
        elif word.count('e') >= 2: score -= 10

        return score

    def order_filtered_words(self):
        self.filtered_words = sorted(self.filtered_words, key=self._compute_word_score, reverse=True)

    def __str__(self):
        output = ""
        # Retrieve the terminal width to adapt the number of words to display
        terminal_width = os.get_terminal_size().columns

        if len(self.filtered_words) > 0:
          output += "\033[1;32mPossible words:\033[0m"
          output += f" {len(self.filtered_words)}\n"
          line_width = 0
          for word in self.filtered_words:
              if line_width + len(word) + 1 > terminal_width:
                  output += "\n"
                  line_width = 0
              output += word + " "
              line_width += len(word) + 1
          output += "\n\n"

        if len(self.most_discriminant_words) > 0 and len(self.filtered_words) > 2:
          output += "\033[1;32mMost discriminant words:\033[0m"
          output += f" {len(self.most_discriminant_words)}\n"
          line_width = 0
          for word in self.most_discriminant_words:
              if line_width + len(word) + 1 > terminal_width:
                  output += "\n"
                  line_width = 0
              output += word + " "
              line_width += len(word) + 1
          output += "\n"

        return output

    def get_most_discriminant_words(self, possible_letters: PossibleLetters):
        lettersCounter = Counter("".join(self.filtered_words))
        lettersCounter = sorted(lettersCounter.items(), key=lambda x: x[1], reverse=True)
    
        # lettersCounter filtering to remove already tested letters
        temp_lettersCounter = []
        for letter, number in lettersCounter:
            if letter not in possible_letters.tested_letters:
              temp_lettersCounter.append((letter, number))
        lettersCounter = temp_lettersCounter

        # Building list of word candidates. Starting from the longest size (5) and if nothing found, try with less (4), etc.
        res = []
        for i in range(5, 0, -1):
          if len(lettersCounter) >= i:
            currentLetters = lettersCounter[:i]

            regex = '^'
            regex += ''.join(f'(?=.*{lettre[0]})' for lettre in currentLetters)
            regex += '[a-zA-Z]*$'

            compiled_regex = re.compile(regex)
            res = [word for word in self.all_words if compiled_regex.match(word)]

          if len(res) > 0:
            break
        
        self.most_discriminant_words = res
