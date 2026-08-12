import os
import tempfile
import unittest

from possible_letters import PossibleLetters
from word_filter import WordFilter


class WordFilterTestCase(unittest.TestCase):
    WORDS = ['tigre', 'arbre', 'moque', 'coque', 'poque', 'toque', 'radis', 'salet']

    def setUp(self):
        fd, self.dict_path = tempfile.mkstemp(suffix='.txt')
        with os.fdopen(fd, 'w') as f:
            f.write('\n'.join(self.WORDS) + '\n')
        self.word_filter = WordFilter(self.dict_path)

    def tearDown(self):
        os.remove(self.dict_path)


class TestFilterWords(WordFilterTestCase):
    def test_filters_by_position_regex(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('- - - - E')  # only 'e' fixed at position 4
        words = list(self.word_filter.filter_words(pl))
        self.assertEqual(set(words), {'tigre', 'arbre', 'moque', 'coque', 'poque', 'toque'})

    def test_filters_out_words_missing_a_required_letter(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('- - - - -')
        pl.must_have = {'x': 1}  # no word in the test dictionary contains 'x'
        words = list(self.word_filter.filter_words(pl))
        self.assertEqual(words, [])

    def test_regression_duplicate_letter_keeps_the_correct_word(self):
        # Same scenario as the TIGRE/RARES bug: target has a single 'r',
        # the correct word must not be eliminated.
        pl = PossibleLetters(5)
        pl.update_possible_letters('r a- r- e s-')
        words = list(self.word_filter.filter_words(pl))
        self.assertIn('tigre', words)

    def test_regression_moque_heuristic_bug(self):
        pl = PossibleLetters(5)
        pl.update_possible_letters('- - - - E')
        pl.update_possible_letters('- O u - -')
        pl.update_possible_letters('- O Q U E')
        words = list(self.word_filter.filter_words(pl))
        self.assertIn('moque', words)


class TestOrderFilteredWords(WordFilterTestCase):
    def test_orders_by_descending_score(self):
        self.word_filter.filtered_words = ['salet', 'radis']
        self.word_filter.order_filtered_words()
        scores = [self.word_filter._compute_word_score(w) for w in self.word_filter.filtered_words]
        self.assertEqual(scores, sorted(scores, reverse=True))

    def test_malus_thresholds_for_repeated_e(self):
        filt = self.word_filter
        letters_frequency = {
            'e': 14.715, 'c': 3.384, 'd': 3.669, 'o': 5.102, 'q': 0.866,
            'u': 5.68, 'x': 0.597,
        }

        def raw_score(word):
            score = sum(letters_frequency[c] for c in word)
            score += len(set(word)) * 3
            return score

        # no malus below 2 occurrences of 'e'
        self.assertAlmostEqual(filt._compute_word_score('coque'), raw_score('coque'))
        # -10 malus at exactly 2 occurrences
        self.assertAlmostEqual(filt._compute_word_score('eecdx'), raw_score('eecdx') - 10)
        # -15 malus at 3 or more occurrences
        self.assertAlmostEqual(filt._compute_word_score('eeecd'), raw_score('eeecd') - 15)


class TestGetMostDiscriminantWords(WordFilterTestCase):
    def test_already_tested_letters_are_not_used_to_pick_candidates(self):
        # If the only letters found in filtered_words have already been tested,
        # they must not be used to build the discriminant-word search.
        pl = PossibleLetters(5)
        pl.tested_letters = ['e']
        self.word_filter.filtered_words = ['eeeee']
        self.word_filter.get_most_discriminant_words(pl)
        self.assertEqual(self.word_filter.most_discriminant_words, [])

    def test_picks_words_covering_the_most_frequent_remaining_letters(self):
        pl = PossibleLetters(5)
        pl.tested_letters = []
        self.word_filter.filtered_words = ['coque']
        self.word_filter.get_most_discriminant_words(pl)
        self.assertIn('coque', self.word_filter.most_discriminant_words)


if __name__ == '__main__':
    unittest.main()
