# French Wordle Guesser

This Python program is a helper to facilate (who said cheat?) the [LouanBen French Wordle](https://wordle.louan.me/) using information provided by the user.
It's definitely more of a style exercise than a real tool!
By the way, the word dictionnary used in this tool has been also taken from the [LouanBen Github repository](https://github.com/LouanBen/wordle-fr).

## Features

- The program loads a list of French words from a dictionnary file (text file with 1 word per line).
- It allows the user to provide hints in the form of a string to refine their search.
- The program filters the list of words based on the hints provided by the user.
- It then displays the possible words that match the given criteria.

## Usage

1. Make sure you have Python installed on your system.
1. Clone this repository or download the source file.
1. Run the program using the command `python wordle.py`.
1. Follow the prompts to provide hints using this format: `(list_of_missing_letters)--x-X` using:
	1. `-` for missing letter,
	1. lowercase letter for a letter at a wrong place (orange)
	1. uppercase letter for a letter at the correct place (green).

## Examples

![Example 1](images/example1.jpg) `(san)--i-E`
![Example 2](images/example2.jpg) `(cout)---r-`
![Example 3](images/example3.jpg) `(v)-ireE`
