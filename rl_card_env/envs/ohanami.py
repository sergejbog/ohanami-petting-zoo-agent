import numpy as np
from rlcard.envs import Env
from ..game import Game
from collections import OrderedDict
from rl_card_env.game.utils.utils import print_cards

DEFAULT_GAME_CONFIG = {
    'num_players': 2,
}


class OhanamiEnv(Env):
    """ Ohanami Environment
    """

    def __init__(self, config):
        self.name = 'ohanami'
        self.default_game_config = DEFAULT_GAME_CONFIG
        self.game = Game(num_players=DEFAULT_GAME_CONFIG['num_players'])
        super().__init__(config)
        self.state_shape = [(120 * self.game.num_players) + 1 + 2 + self.game.num_players for _ in range(self.game.num_players)]
        self.action_shape = [None for _ in range(self.game.num_players)]

    def get_payoffs(self):
        """ Get the payoff of a game

        Returns:
           payoffs (list): list of payoffs
        """
        if self.game.is_over():
            return self.game.get_payoffs()
        else:
            return [0 for _ in range(self.game.num_players)]

    @staticmethod
    def _round_to_thermometer_encoding(round_number):
        if round_number == 0:
            return [0, 0]
        elif round_number == 1:
            return [0, 1]
        elif round_number == 2:
            return [1, 1]
        else:
            raise ValueError("Invalid round number")

    def _extract_state(self, state):
        """ Encode state

        Args:
            state (dict): dict of original state

        Returns:
            numpy array: 5 * 52 array
                         5 : current hand (1 if card in hand else 0)
                             top_discard (1 if card is top discard else 0)
                             dead_cards (1 for discards except for top_discard else 0)
                             opponent known cards (likewise)
                             unknown cards (likewise)  # is this needed ??? 200213
        """
        MAX_NUM_CARDS = 120
        MAX_POINTS = 285
        if self.game.is_over():
            empty_hand_vector = [0] * MAX_NUM_CARDS  # Assuming binary representation for cards
            obs = {
                'hand': empty_hand_vector,
                'gardens': [empty_hand_vector for _ in range(MAX_NUM_CARDS * self.game.num_players)],
                'discarded_num': 0,
                'round_counter': 0,
                'points': [0 for _ in range(self.game.num_players)],
            }
            extracted_state = {'obs': obs, 'legal_actions': self._get_legal_actions(), 'raw_legal_actions': list(self._get_legal_actions().keys()), 'raw_obs': obs}
        else:
            hand_vec = np.zeros(MAX_NUM_CARDS)
            for card in state['hand']:
                hand_vec[card.number - 1] = 1

            gardens_vec = np.zeros(MAX_NUM_CARDS * self.game.num_players)
            for player_num, gardens in enumerate(state['gardens']):
                for garden in gardens:
                    for card in garden:
                        gardens_vec[player_num * MAX_NUM_CARDS + card.number - 1] = 1

            discarded_num = state['discarded_num']

            round_counter_norm = self._round_to_thermometer_encoding(state['round_counter'])
            points_norm = [p / MAX_POINTS for p in state['points']]

            final_vector = np.concatenate([hand_vec,
                                           gardens_vec,
                                           [discarded_num],
                                           round_counter_norm,
                                           points_norm])
            extracted_state = {'obs': final_vector, 'legal_actions': self._get_legal_actions(), 'raw_legal_actions': list(self._get_legal_actions().keys()), 'raw_obs': final_vector}
        return extracted_state

    def _decode_action(self, action_id):
        """ Action id -> the action in the game. Must be implemented in the child class.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        """
        return self.game.decode_action(action_id=action_id)

    def _get_legal_actions(self):
        """ Get all legal actions for current state

        Returns:
            legal_actions (list): a list of legal actions' id
        """
        legal_actions = self.game.get_legal_actions()
        legal_actions_ids = {action_event.action_id: None for action_event in legal_actions}
        return OrderedDict(legal_actions_ids)

    def print_state(self, player_id):
        """ Print out the state
        """

        if self.game.is_over():
            print('===============   Game Over    ===============')
            return
        state = self.game.get_state(player_id)
        print('===============   Round {}    ==============='.format(state['round_counter']))
        print('Current player: {}'.format(self.game.round.current_player_id))
        print('Discarded cards: {}'.format(state['discarded_num']))
        print('Current hand:')
        print_cards(state['hand'])
        print()
        # print("Legal actions:")
        # for action_id in self._get_legal_actions():
        #     print(self._decode_action(action_id))
        print('Current gardens:')
        for i, gardens in enumerate(state['gardens']):
            if i == 0:
                print('Your gardens:')
            else:
                print('Opponent {}:'.format(i))
            for garden in gardens:
                print_cards(garden)
                print()
            print("==========================")
        print('Current points:')
        for i, points in enumerate(state['points']):
            print('Player {}: {}'.format(i, points))
        print('=============================================')
