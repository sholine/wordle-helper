import string
import sys

def compute_word_score(word):
    # Définition des fréquences des lettres en français
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

    # Calcul du score en utilisant les fréquences des lettres et en évitant la répétition de lettres
    score = 0
    used_letters = set()
    for letter in word:
        score += letters_frequency.get(letter, 0)
        used_letters.add(letter)

    # Bonus pour la variété de lettres (je pondère en multipliant par 3)
    score += len(used_letters) * 3

    return score

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [word.strip().lower() for word in file.readlines()]

def initialize_possible_letters():
    possible_letters = {
        'word': [list(string.ascii_lowercase) for _ in range(5)],
        'must_have': []
    }
    return possible_letters

def log_possible_letters(possible_letters):
    for key, value in possible_letters.items():
        if key == 'word':
            print(f"[{key}]")
            for i, letters in enumerate(value):
                print(f"  [Position {i}] => {letters}")
        elif key == 'must_have':
            print(f"[{key}] => {''.join(value)}")

def update_possible_letters(possible_letters, input_string):
    excluded_letters = input_string[input_string.find('(')+1:input_string.find(')')]
    input_string = input_string[input_string.find(')')+1:]
    
    for letter in excluded_letters:
        for i in range(5):
            possible_letters['word'][i] = [l for l in possible_letters['word'][i] if l != letter]

    for i, char in enumerate(input_string):
        if char.islower():
            possible_letters['word'][i] = [letter for letter in possible_letters['word'][i] if letter != char]
            possible_letters['must_have'].append(char)
        elif char.isupper():
            possible_letters['word'][i] = [char.lower()]

    if "-v" in sys.argv or "--verbose" in sys.argv:
        log_possible_letters(possible_letters)

    return True

# Filtre les mots du dictionnaire en fonction des contraintes de lettres connues
def filter_words(words, possible_letters):
    filtered_words = []
    for word in words:
        if all(word[i] in possible_letters['word'][i] for i in range(5)) and all(letter in word for letter in possible_letters['must_have']):
            filtered_words.append(word)
    return filtered_words

# Trie les mots en fonction de leur score
def order_filtered_words(words):
    mots_tries = sorted(words, key=compute_word_score, reverse=True)
    return mots_tries

def main():
    dictionary_file = "french_5.txt"
    words = load_dictionary(dictionary_file)
    possible_letters = initialize_possible_letters()

    while True:
        input_string = input("Enter input string (press Enter to exit): ")
        if not input_string:
            break
        
        if update_possible_letters(possible_letters, input_string):
            filtered_words = order_filtered_words(filter_words(words, possible_letters))
            print("Possible words:")
            for word in filtered_words:
                print(word)

if __name__ == "__main__":
    main()
