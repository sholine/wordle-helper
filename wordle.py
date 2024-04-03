import string
import sys
import yaml

def load_occurrences(file_path="occurences.yaml"):
    try:
        with open(file_path, 'r') as file:
            occurrences_data = yaml.safe_load(file)
            return occurrences_data
    except FileNotFoundError:
        print(f"File '{file_path}' not found. Using default occurrences.")
        return {
            letter: 1 for letter in string.ascii_lowercase
        }

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

def filter_words(words, possible_letters, occurrences):
    def sort_key(word):
        return sum(occurrences[letter] for letter in word if letter in occurrences)
    
    filtered_words = [word for word in words if all(word[i] in possible_letters['word'][i] for i in range(5))]
    filtered_words.sort(key=sort_key, reverse=True)
    return filtered_words

def main():
    dictionary_file = "french_5.txt"
    occurrences = load_occurrences()
    words = load_dictionary(dictionary_file)
    possible_letters = initialize_possible_letters()

    while True:
        input_string = input("Enter input string (press Enter to exit): ")
        if not input_string:
            break
        
        if update_possible_letters(possible_letters, input_string):
            filtered_words = filter_words(words, possible_letters, occurrences)
            print("Possible words:")
            for word in filtered_words:
                print(word)

if __name__ == "__main__":
    main()
