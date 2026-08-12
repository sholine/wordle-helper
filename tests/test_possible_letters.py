import string
import unittest

from possible_letters import PossibleLetters


class TestPossibleLettersInitialState(unittest.TestCase):
    def test_starts_with_all_letters_possible_everywhere(self):
        pl = PossibleLetters(5)
        self.assertEqual(len(pl.word), 5)
        for possibilities in pl.word:
            self.assertEqual(possibilities, list(string.ascii_lowercase))

    def test_starts_with_empty_tracking_state(self):
        pl = PossibleLetters(5)
        self.assertEqual(pl.must_have, {})
        self.assertEqual(pl.letter_max_count, {})
        self.assertEqual(pl.tested_letters, [])


class TestGreenLetters(unittest.TestCase):
    def test_green_letter_fixes_the_position(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('T - - - -')
        self.assertEqual(pl.word[0], ['t'])

    def test_green_letter_is_recorded_in_must_have(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('T - - - -')
        self.assertEqual(pl.must_have.get('t'), 1)

    def test_green_letter_is_tracked_as_tested(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('T - - - -')
        self.assertIn('t', pl.tested_letters)


class TestYellowLetters(unittest.TestCase):
    def test_yellow_letter_is_removed_from_its_own_position_only(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('t - - - -')
        self.assertNotIn('t', pl.word[0])
        self.assertIn('t', pl.word[1])

    def test_yellow_letter_is_recorded_in_must_have(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('t - - - -')
        self.assertEqual(pl.must_have.get('t'), 1)


class TestNoInfoToken(unittest.TestCase):
    def test_dash_token_leaves_position_untouched(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('- - - - -')
        for possibilities in pl.word:
            self.assertEqual(possibilities, list(string.ascii_lowercase))
        self.assertEqual(pl.tested_letters, [])


class TestGrayLetters(unittest.TestCase):
    def test_letter_absent_from_the_whole_guess_is_excluded_everywhere(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('s- - - - -')
        for possibilities in pl.word:
            self.assertNotIn('s', possibilities)

    def test_letter_absent_from_the_whole_guess_is_not_capped(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('s- - - - -')
        self.assertEqual(pl.letter_max_count, {})

    def test_duplicate_letter_gray_occurrence_caps_the_exact_count(self):
        # Guess has 'r' twice: one confirmed present (yellow) and one excess (gray).
        # The word must contain exactly 1 'r'.
        pl = PossibleLetters(5)
        pl.update_possible_letters('r a- r- e s-')
        self.assertEqual(pl.letter_max_count.get('r'), 1)

    def test_duplicate_letter_gray_occurrence_only_excludes_its_own_position(self):
        # Regression test: the excess 'r' (position 2) must not be removed from
        # other still-open positions (e.g. position 3, where the real 'r' could be).
        pl = PossibleLetters(5)
        pl.update_possible_letters('r a- r- e s-')
        self.assertNotIn('r', pl.word[2])
        self.assertIn('r', pl.word[3])

    def test_duplicate_letter_still_required_at_least_once(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('r a- r- e s-')
        self.assertEqual(pl.must_have.get('r'), 1)


class TestMultiOccurrenceLetters(unittest.TestCase):
    def test_two_green_occurrences_require_two_in_must_have(self):
        # ARBRE has two 'r's, both guessed at the right place.
        pl = PossibleLetters(5)
        pl.update_possible_letters('A R B R E')
        self.assertEqual(pl.must_have.get('r'), 2)
        self.assertEqual(pl.word, [['a'], ['r'], ['b'], ['r'], ['e']])


class TestHeuristics(unittest.TestCase):
    def test_last_remaining_position_is_deduced(self):
        # 'a' is required once (yellow at position 0, so excluded there).
        # Simulate that every other position except position 2 has already
        # excluded 'a' too (e.g. via other guesses' gray letters), so 'a'
        # must be at position 2.
        pl = PossibleLetters(5)
        pl.update_possible_letters('a - - - -')  # 'a' yellow at position 0: must_have={'a': 1}
        for i in [1, 3, 4]:
            pl.word[i] = [c for c in pl.word[i] if c != 'a']
        pl._apply_heuristics()
        self.assertEqual(pl.word[2], ['a'])

    def test_heuristic_does_not_re_place_an_already_satisfied_letter(self):
        # Regression test for the "moque" bug: a letter fixed directly via a
        # green token (and thus already satisfying must_have) must not be
        # force-placed again into another still-open position.
        pl = PossibleLetters(5)
        pl.update_possible_letters('s- a- i- n- E')   # 'e' fixed at position 4, must_have={'e': 1}
        pl.update_possible_letters('l- O u r- d-')    # 'o' fixed at position 1, 'u' required
        pl.update_possible_letters('t- O Q U E')      # 'q' and 'u' fixed; position 0 is the only one left open

        self.assertEqual(pl.word[0], list('bcefghjkmopquvwxyz'))
        self.assertIn('m', pl.word[0])


class TestRegexGeneration(unittest.TestCase):
    def test_regex_reflects_fixed_and_open_positions(self):
        pl = PossibleLetters(3)
        pl.word = [['a'], ['b', 'c'], ['z']]
        self.assertEqual(pl.generate_regex_from_letters(), '^a[bc]z$')


if __name__ == '__main__':
    unittest.main()
