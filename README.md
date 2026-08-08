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
1. Follow the prompts to provide hints as a space-separated list of tokens, one per letter position, using this format:
	1. `-` if you have no information for this position,
	1. **lowercase** letter for a letter at the wrong place (orange), e.g. `x`,
	1. **uppercase** letter for a letter at the correct place (green), e.g. `X`,
	1. **lowercase** letter followed by `-` for a letter that is grayed out at this position, e.g. `x-`. If this letter doesn't appear anywhere else (green/orange) in the same guess, it means the letter is absent from the word. Otherwise, it means the word contains exactly as many occurrences of that letter as there are green/orange occurrences in the same guess — this is how repeated letters (e.g. a word with two "r") are handled correctly.

## Examples

![Example 1](images/example1.jpg) `s- a- i n- E`
![Example 2](images/example2.jpg) `c- o- u- r t-`
![Example 3](images/example3.jpg) `v- i r e E`

Repeated letter example: guessing `RARES` against a word containing a single `r` (at an unknown position) gives `r a- r- e- s-` — the first `r` is orange (present, wrong place), the second `r` is grayed out because the word only has one `r`.
