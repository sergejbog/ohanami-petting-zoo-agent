import unittest
from unittest.mock import MagicMock
from rl_card_env.game.utils.action_event import *
from rl_card_env.game.Game import OhanamiGame
from rl_card_env.game.Player import OhanamiPlayer
from rl_card_env.game.Round import OhanamiRound
from rl_card_env.game.Dealer import OhanamiDealer
# Other necessary imports go here


class TestOhanamiGame(unittest.TestCase):

    def setUp(self):
        """Setup a basic game instance for each test."""
        self.game = OhanamiGame(num_players=2)

    def test_init_game(self):
        """Test the init_game method thoroughly."""
        state, current_player_id = self.game.init_game()

        # 1. Check that dealer is initialized
        self.assertIsInstance(self.game.dealer, OhanamiDealer)

        # 2. Check if all players are initialized
        self.assertEqual(len(self.game.players), 2)
        for i, player in enumerate(self.game.players):
            self.assertIsInstance(player, OhanamiPlayer)
            self.assertEqual(player.player_id, i)

        # 3. Ensure that the round is initialized and started correctly
        self.assertIsInstance(self.game.round, OhanamiRound)

        # 4. Check if round_counter is initialized to 0
        self.assertEqual(self.game.round_counter, 0)

        # 5. Validate the structure and contents of the returned state
        self.assertIn('hand', state)
        self.assertIn('discarded_num', state)
        self.assertIn('round_counter', state)
        self.assertIn('gardens', state)
        self.assertIn('points', state)

        self.assertEqual(state['round_counter'], 0)
        self.assertEqual(len(state['gardens']), self.game.num_players)
        self.assertEqual(len(state['points']), self.game.num_players)

        # 6. Validate the current_player_id
        self.assertEqual(current_player_id, self.game.round.current_player_id)

    def test_is_over(self):
        """Test the is_over method."""
        self.game.round_counter = 0
        self.assertFalse(self.game.is_over())

        self.game.round_counter = 3
        self.assertTrue(self.game.is_over())

    def test_state_initialization(self):
        """Test get_state method after game initialization."""
        self.game.init_game()
        state = self.game.get_state(player_id=0)

        # Validate keys
        self.assertIn('hand', state)
        self.assertIn('discarded_num', state)
        self.assertIn('round_counter', state)
        self.assertIn('gardens', state)
        self.assertIn('points', state)

        # Check initial conditions
        self.assertEqual(state['discarded_num'], 0)
        self.assertEqual(state['round_counter'], 0)
        for garden in state['gardens']:
            self.assertTrue(isinstance(garden, list))
        self.assertEqual(len(state['points']), 2)

    def test_get_state(self):
        self.game.init_game()
        """Test the get_state method."""
        state = self.game.get_state(player_id=0)

        # Add some simple checks. You can expand on this.
        self.assertIn('hand', state)
        self.assertIn('discarded_num', state)

    def test_get_num_players(self):
        """Test the get_num_players method."""
        self.assertEqual(self.game.get_num_players(), 2)

    # You can add more unit tests for other methods too!


if __name__ == '__main__':
    unittest.main()
