import string
import sys
import re
import os

from possible_letters import PossibleLetters

# Compute word scoring using French letters frequency and letters reuse
def compute_word_score(word):
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

def load_dictionary(file_path):
  with open(file_path, 'r') as file:
    return [word.strip().lower() for word in file.readlines()]

def update_possible_letters(possible_letters: PossibleLetters, input_string):
  excluded_letters = input_string[input_string.find('(')+1:input_string.find(')')]
  input_string = input_string[input_string.find(')')+1:]
  
  for letter in excluded_letters:
    for i in range(5):
      if (len(possible_letters.word[i]) > 1 and letter in possible_letters.word[i]):
        possible_letters.word[i].remove(letter)

  for i, char in enumerate(input_string):
    if char.islower():
      possible_letters.word[i].remove(char)
      possible_letters.must_have.append(char)
    elif char.isupper():
      possible_letters.word[i] = [char.lower()]

  if "-v" in sys.argv or "--verbose" in sys.argv:
    possible_letters.print()

  return True

def generate_regex_from_letters(word):
  regex = '^'
  for position in word:
    if len(position) == 1:
      regex += position[0]  # Ajoute la lettre seule à l'expression régulière
    else:
      regex += '[' + ''.join(position) + ']'  # Ajoute les lettres entre crochets à l'expression régulière
  regex += '$'
  return regex

# Filtre les mots du dictionnaire en fonction des contraintes de lettres connues
def filter_words(words, possible_letters: PossibleLetters):
  regex = generate_regex_from_letters(possible_letters.word)
  #print("Regex : ["+regex+"]")
  first_filtering = list(filter(lambda word: re.match(regex, word), words))
  #print("First filter : ",len(first_filtering))
  second_filtering = []
  for word in first_filtering:
    if all(letter in word for letter in possible_letters.must_have):
      second_filtering.append(word)
  #print("Second filter : ",len(second_filtering))
  return second_filtering

# Trie les mots en fonction de leur score
def order_filtered_words(words):
  mots_tries = sorted(words, key=compute_word_score, reverse=True)
  return mots_tries

def print_proposals(filtered_words):
  # Récupérer la largeur du terminal
  terminal_width = os.get_terminal_size().columns

  line_width = 0
  for word in filtered_words:
    if line_width + len(word) + 1 > terminal_width:
      print("")
      line_width = 0
    print(word, end=" ")
    line_width += len(word) + 1
  print("")

def main():
  dictionary_file = "french_5_wordle.txt"
  words = load_dictionary(dictionary_file)
  possible_letters = PossibleLetters(5)

  while True:
    input_string = input("Enter input string (press Enter to exit): ")
    if not input_string:
      break
    
    if update_possible_letters(possible_letters, input_string):
      filtered_words = order_filtered_words(filter_words(words, possible_letters))
      print("Possible words:")
      print_proposals(filtered_words)

if __name__ == "__main__":
  main()
