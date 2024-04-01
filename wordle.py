import string

def load_dictionary(file_path):
    with open(file_path, 'r') as file:
        return [word.strip().lower() for word in file.readlines()]

def initialize_possible_letters():
    return [list(string.ascii_lowercase) for _ in range(5)]

def log_possible_letters(possible_letters):
    for i, letters in enumerate(possible_letters):
        print(f"[Position {i}] => {letters}")

def update_possible_letters(possible_letters, input_string):
    excluded_letters = input_string[input_string.find('(')+1:input_string.find(')')]
    input_string = input_string[input_string.find(')')+1:]
    
    for letter in excluded_letters:
        for i in range(5):
            possible_letters[i] = [l for l in possible_letters[i] if l != letter]

    for i, char in enumerate(input_string):
        if char.islower():
            possible_letters[i] = [letter for letter in possible_letters[i] if letter != char]
        elif char.isupper():
            possible_letters[i] = [char.lower()]
    log_possible_letters(possible_letters)
    return True
    

def filter_words(words, possible_letters):
    filtered_words = []
    for word in words:
        if all(word[i] in possible_letters[i] for i in range(5)):
            filtered_words.append(word)
    return filtered_words

def main():
    dictionary_file = "dictionary.txt"
    words = load_dictionary(dictionary_file)
    possible_letters = initialize_possible_letters()
    log_possible_letters(possible_letters)

    while True:
        input_string = input("Enter input string (press Enter to exit): ")
        if not input_string:
            break
        
        if update_possible_letters(possible_letters, input_string):
            filtered_words = filter_words(words, possible_letters)
            print("Possible words:")
            for word in filtered_words:
                print(word)

if __name__ == "__main__":
    main()
