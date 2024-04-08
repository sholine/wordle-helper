import string
import sys
import re

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
    
    def update_possible_letters(self, input_string: string):
        """Update all letters remaining possibilities regarding the user's input string

        Args:
            input_string (string): Should have this format: (<unused_letters>)<wordle_letters>
              '-' if the letter was unused
              lowercase: if the letter is at the wrong place (orange letter)
              uppercase: if the letter is at the right place (green letter)
        """
        excluded_letters = input_string[input_string.find('(') + 1 : input_string.find(')')]
        input_string = input_string[input_string.find(')') + 1 :]
        
        for letter in excluded_letters:
            for possibilities in self.word:
                if (len(possibilities) > 1 and letter in possibilities):
                  possibilities.remove(letter)

        for i, char in enumerate(input_string):
            if char.islower():
                self.word[i].remove(char)
                self.must_have.append(char)
            elif char.isupper():
                self.word[i] = [char.lower()]

        if "-v" in sys.argv or "--verbose" in sys.argv:
            self.print()
    
    def generate_regex_from_letters(self):
        regex = '^'
        for possibilities in self.word:
            if len(possibilities) == 1:
                regex += possibilities[0]  # Ajoute la lettre seule à l'expression régulière
            else:
                regex += '[' + ''.join(possibilities) + ']'  # Ajoute les lettres entre crochets à l'expression régulière
        regex += '$'
        if "-v" in sys.argv or "--verbose" in sys.argv:
            print("Regex : [", regex, "]")
        return regex
