import numpy as np
from rl_card_env.game.Dealer import OhanamiDealer
from rl_card_env.game.Player import OhanamiPlayer
from rl_card_env.game.Round import OhanamiRound
from rl_card_env.game.utils.action_event import *
from typing import List
from rl_card_env.game.utils.garden_position import POSITION

MAX_NUM_PLAYERS = 4
MAX_NUM_ROUNDS = 3


class OhanamiGame:
    def __init__(self, num_players):
        self.round_counter = 0
        self.round: OhanamiRound = None
        self.players: List[OhanamiPlayer] = []
        self.dealer = None
        self.num_players = num_players
        self.np_random = np.random.RandomState()
        self.max_rounds = MAX_NUM_ROUNDS

    def init_game(self):
        """ Initialize all characters in the game and start round 1
        """
        self.dealer = OhanamiDealer(self.np_random)
        self.players = [OhanamiPlayer(i, num_players=self.num_players) for i in range(self.num_players)]

        self.round = OhanamiRound(dealer=self.dealer, players=self.players, num_players=self.num_players)
        self.round.start_round()
        # Count the round. There are 3 rounds in each game.
        self.round_counter = 0

        current_player_id = self.round.current_player_id
        state = self.get_state(player_id=current_player_id)
        return state, current_player_id

    def is_over(self):
        """ Check if the game is over
        """
        return self.round_counter > self.max_rounds - 1

    def get_state(self, player_id: int):
        """ Get player's state
        Return:
            state (dict): The information of the state
        """
        state = {}
        if not self.is_over():
            state['hand'] = [card for card in self.players[player_id].hand]
            state['discarded_num'] = len(self.dealer.discards)
            state['round_counter'] = self.round_counter
            # state['remaining_cards'] = self.players[player_id].remaining_cards
            cards_from_gardens = self.players[player_id].get_cards_from_gardens()
            state['gardens'] = [[garden for garden in cards_from_gardens]]
            state['points'] = [self.players[player_id].points]
            sum_of_all_scores = 0
            for player in self.players:
                if player == self.players[player_id]:
                    continue
                cards_from_gardens = player.get_cards_from_gardens()
                state['gardens'].append([garden for garden in cards_from_gardens])
                state['points'].append(player.points)
                sum_of_all_scores += player.points

            # average_others_score = (sum_of_all_scores - self.players[player_id].points) / (self.num_players - 1)
            # score_differential = self.players[player_id].points - average_others_score
            # state['score_differential'] = score_differential
        return state

    def step(self, action: ActionEvent):
        if isinstance(action, ChooseCard1Garden1LargestAction):
            self.round.add_to_garden(card=action.card, garden_index=0, position=POSITION.LARGEST, round_counter=self.round_counter)
        elif isinstance(action, ChooseCard1Garden1SmallestAction):
            self.round.add_to_garden(card=action.card, garden_index=0, position=POSITION.SMALLEST, round_counter=self.round_counter)
        elif isinstance(action, ChooseCard1Garden2LargestAction):
            self.round.add_to_garden(card=action.card, garden_index=1, position=POSITION.LARGEST, round_counter=self.round_counter)
        elif isinstance(action, ChooseCard1Garden2SmallestAction):
            self.round.add_to_garden(card=action.card, garden_index=1, position=POSITION.SMALLEST, round_counter=self.round_counter)
        elif isinstance(action, ChooseCard1Garden3LargestAction):
            self.round.add_to_garden(card=action.card, garden_index=2, position=POSITION.LARGEST, round_counter=self.round_counter)
        elif isinstance(action, ChooseCard1Garden3SmallestAction):
            self.round.add_to_garden(card=action.card, garden_index=2, position=POSITION.SMALLEST, round_counter=self.round_counter)
        elif isinstance(action, ChooseCard1DiscardAction):
            self.round.discard_card(action.card)

        if self.round.is_round_over():
            self.round_counter += 1
            self.round.start_round()

        next_player_id = self.round.current_player_id

        state = self.get_state(player_id=next_player_id)
        return state, next_player_id

    def get_player_id(self):
        """ Return current player id
        """
        return self.round.current_player_id

    def get_payoffs(self):
        # Sort players by their scores in descending order
        sorted_players = sorted(self.players, key=lambda x: x.points, reverse=True)

        rewards = {}
        skip = 0
        for i in range(self.num_players):
            if skip:
                skip -= 1
                continue

            current_points = sorted_players[i].points

            # Find how many players have the same points (ties)
            j = i + 1
            while j < self.num_players and sorted_players[j].points == current_points:
                j += 1

            num_tied_players = j - i

            # Calculate the average reward for the tied players
            total_rewards_for_tied = sum([(2 * k) / (self.num_players - 1) - 1 for k in range(i, j)])
            avg_reward_for_tied = total_rewards_for_tied / num_tied_players

            for k in range(i, j):
                rewards[sorted_players[k].player_id] = avg_reward_for_tied

            skip = num_tied_players - 1

        return rewards

    def get_legal_actions(self):
        """ Get the legal actions for the current player
        """
        return self.round.get_legal_actions()

    def get_num_players(self):
        """ Return the number of players in the game
        """
        return self.num_players

    @staticmethod
    def get_num_actions():
        """ Return the number of possible actions in the game
        """
        return ActionEvent.get_num_actions()

    @staticmethod
    def decode_action(action_id) -> ActionEvent:
        """ Action id -> the action_event in the game.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        """
        return ActionEvent.decode_action(action_id=action_id)
