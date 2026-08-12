import os
import re
import subprocess
import sys
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANSI_ESCAPE = re.compile(r'\x1b\[[0-9;]*m')


def run_wordle(guesses, timeout=15):
    input_text = "\n".join(guesses) + "\n\n"
    result = subprocess.run(
        [sys.executable, 'wordle.py'],
        cwd=REPO_ROOT,
        input=input_text,
        capture_output=True,
        text=True,
        timeout=timeout,
    )
    result.stdout = ANSI_ESCAPE.sub('', result.stdout)
    return result


class TestWordleFunctional(unittest.TestCase):
    """End-to-end tests driving the real wordle.py REPL against the actual
    french_5_wordle.txt dictionary, as a user would from the terminal."""

    def test_exits_cleanly_on_empty_input(self):
        result = run_wordle([])
        self.assertEqual(result.returncode, 0)

    def test_first_guess_shows_expected_candidate_count(self):
        result = run_wordle(['s- a- i- n- E'])
        self.assertIn('Possible words: 509', result.stdout)

    def test_regression_duplicate_letter_keeps_correct_word(self):
        # Target has a single 'r'; guessing it twice (one confirmed, one
        # grayed-out excess) must not eliminate the correct word.
        result = run_wordle(['r a- r- e s-'])
        self.assertIn('tigre', result.stdout.split())

    def test_regression_moque_stays_a_candidate(self):
        # Exact scenario reported by the user: after 3 guesses narrowing
        # every letter but the first one, 'moque' used to disappear because
        # of a stale must_have entry re-triggering the placement heuristic.
        result = run_wordle(['s- a- i- n- E', 'l- O u r- d-', 't- O Q U E'])
        self.assertIn('moque', result.stdout.split())

    def test_no_information_token_is_accepted(self):
        result = run_wordle(['- - - - -'])
        self.assertEqual(result.returncode, 0)
        self.assertIn('Possible words:', result.stdout)


if __name__ == '__main__':
    unittest.main()
