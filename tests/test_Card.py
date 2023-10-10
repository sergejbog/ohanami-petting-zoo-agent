import unittest
from unittest import TestCase
from rl_card_env.game.Card import OhanamiCard, CARD_COLOR_MAP


class TestOhanamiCard(TestCase):
    def test_card_numbers(self):
        all_numbers = []
        for color, numbers in CARD_COLOR_MAP.items():
            all_numbers.extend(numbers)

        # Check if there are no duplicates
        self.assertEqual(len(all_numbers), len(set(all_numbers)))

        # Check if all numbers from 1 to 120 are included
        self.assertEqual(set(all_numbers), set(range(1, 121)))


if __name__ == '__main__':
    unittest.main()
