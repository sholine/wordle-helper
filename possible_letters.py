import string
import sys

class PossibleLetters:
    def __init__(self, words_size):
        self.words_size = words_size
        self.word = [list(string.ascii_lowercase) for _ in range(words_size)]
        self.must_have = []
        self.tested_letters = []

    def __str__(self):
        output = "\033[1;33m[Word]\033[0m\n"
        for i, letters in enumerate(self.word):
            output += f"  [Position {i}] => {letters}\n"
        output += f"\033[1;33m[Must Have]\033[0m => {self.must_have}\n"
        output += f"\033[1;33m[Tested Letters]\033[0m => {self.tested_letters}\n"
        return output

    def _apply_heuristics(self):
        # Première heuristique : si une lettre est mal placée (dans "Must have" et qu'il n'y a qu'une seule possibilité où elle peut se trouver, alors on sait où elle va aller)
        for letter in self.must_have:
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
              if letter.lower() in self.must_have:
                  self.must_have.remove(letter.lower())

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
            if letter not in self.tested_letters:
                self.tested_letters.append(letter)
            for possibilities in self.word:
                if (len(possibilities) > 1 and letter in possibilities):
                  possibilities.remove(letter)

        for i, char in enumerate(input_string):
            if char.lower() != '-' and char.lower() not in self.tested_letters:
                self.tested_letters.append(char.lower())
            if char.islower():
                if char in self.word[i]:
                  self.word[i].remove(char)
                if char not in self.must_have:
                  self.must_have.append(char)
            elif char.isupper():
                self.word[i] = [char.lower()]
                if char.lower() in self.must_have:
                  self.must_have.remove(char.lower())

        self._apply_heuristics()

        if "-v" in sys.argv or "--verbose" in sys.argv:
            print(self)
    
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
