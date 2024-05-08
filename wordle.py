from possible_letters import PossibleLetters
from word_filter import WordFilter

def main():
  word_filter = WordFilter("french_5_wordle.txt")
  possible_letters = PossibleLetters(5)

  while True:
    input_string = input("Enter input string (press Enter to exit): ")
    if not input_string:
      break
    
    possible_letters.update_possible_letters(input_string)
    word_filter.filter_words(possible_letters)
    word_filter.order_filtered_words()
    print(word_filter)

if __name__ == "__main__":
  main()
