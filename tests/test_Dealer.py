import unittest
from unittest.mock import MagicMock
from rl_card_env.game.utils.utils import init_deck, OhanamiCard
from rl_card_env.game.Player import OhanamiPlayer
from rl_card_env.game.Dealer import OhanamiDealer
import numpy as np


class TestOhanamiDealer(unittest.TestCase):

    def setUp(self):
        self.np_random_mock = MagicMock()
        self.dealer = OhanamiDealer(self.np_random_mock)
        self.player = OhanamiPlayer(0, 2)

    def test_init(self):
        self.assertEqual(len(self.dealer.deck), len(init_deck()))
        self.assertEqual(self.dealer.discards, [])

    def test_shuffle(self):
        original_deck = self.dealer.deck.copy()

        # Resetting mock so previous calls in setUp don't interfere with this test
        self.dealer.np_random = np.random.RandomState(0)

        self.dealer.shuffle()
        self.np_random_mock.shuffle.assert_called_once_with(self.dealer.deck)

        # Assuming shuffle worked, the deck should be different from the original
        # (Note: this is probabilistic and can technically fail)
        self.assertNotEqual(self.dealer.deck, original_deck)

    def test_deal_cards(self):
        # Mock the deck pop
        self.dealer.deck = [OhanamiCard(i) for i in range(1, 6)]  # Mock deck with 5 cards
        self.dealer.deal_cards(self.player, 3)
        # Check the player's hand size
        self.assertEqual(len(self.player.hand), 3)
        # Check the deck size after dealing
        self.assertEqual(len(self.dealer.deck), 2)

    def test_discard_card(self):
        card = OhanamiCard(15)  # Random card for testing
        self.dealer.discard_card(card)
        self.assertIn(card, self.dealer.discards)

    def tearDown(self):
        del self.dealer
        del self.player


if __name__ == '__main__':
    unittest.main()
