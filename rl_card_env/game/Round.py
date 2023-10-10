from typing import List

from rl_card_env.game.Dealer import OhanamiDealer
from rl_card_env.game.Player import OhanamiPlayer
from rl_card_env.game.Card import OhanamiCard
from rl_card_env.game.utils.garden_position import POSITION
from rl_card_env.game.utils.action_event import *
from rl_card_env.game.Judger import OhanamiJudger


class OhanamiRound:

    def __init__(self, dealer: OhanamiDealer, players: List[OhanamiPlayer],  num_players):
        """ Initialize the round class

        Args:
            dealer (object): OhanamiDealer object
            players (List[object]): List[OhanamiPlayer] object
            num_players (int): the number of players in game

        """
        self.dealer = dealer
        self.players = players
        self.current_player_id = 0
        self.num_players = num_players
        self.played_cards = []  # For tracking cards played in this round
        self.current_player_num_actions = 0
        self.players_finished_actions_count = 0

    def start_round(self):
        for player in self.players:
            self.dealer.deal_cards(player, 10)

    def discard_card(self, card):
        """ Discard a card

        Args:
            card (OhanamiCard): The card to be discarded
        """
        self.dealer.discards.append(card)
        self.players[self.current_player_id].remove_from_hand(card)

        self._increment_actions_and_check()

    def add_to_garden(self, card: OhanamiCard, garden_index, position: POSITION, round_counter: int):
        """ Add a card to the garden of the player and increase the points of the player

        Args:
            card (object): OhanamiCard object
            garden_index (int): The index of the garden
            position (POSITION): The position of the card in the garden
            round_counter (int): The round counter
        """
        self.players[self.current_player_id].add_to_garden(card, garden_index, position)
        self.players[self.current_player_id].remove_from_hand(card)
        self.players[self.current_player_id].add_points(OhanamiJudger.get_points(card, round_counter, self.players[self.current_player_id].num_of_pink_cards))

        self._increment_actions_and_check()

    def is_round_over(self) -> bool:
        """ Check if the round is over by checking if all players have played their cards. """
        return all([len(player.hand) == 0 for player in self.players])

    def _pass_cards(self):
        """ Pass the cards to the player above in the array. """
        # The last player's cards are saved temporarily
        last_player_cards = self.players[-1].hand.copy()

        # Iterate from the end to the start and shift cards
        for i in range(self.num_players - 1, 0, -1):
            self.players[i].hand = self.players[i - 1].hand.copy()

        # The first player gets the last player's cards
        self.players[0].hand = last_player_cards

    def _increment_actions_and_check(self):
        """ Increment the action count and check if it's time to proceed to the next round. """
        self.current_player_num_actions += 1
        if self.current_player_num_actions == 2:
            self.current_player_num_actions = 0
            self.players_finished_actions_count += 1
            self.proceed_round()

    def proceed_round(self):
        if self.players_finished_actions_count == self.num_players:
            self.players_finished_actions_count = 0
            self._pass_cards()
        self.current_player_id = (self.current_player_id + 1) % self.num_players

    def get_legal_actions(self) -> list:
        """ Get the legal actions for the current player """
        current_player = self.players[self.current_player_id]
        legal_actions = []

        # Check each card in the player's hand
        for card in current_player.hand:
            # Check if the card can be added to the top or bottom of each garden
            for garden_idx, garden in enumerate(current_player.gardens):
                if not garden or card > garden[-1]:  # can add to the bottom
                    if garden_idx == 0:
                        legal_actions.append(ChooseCard1Garden1LargestAction(card=card))
                    elif garden_idx == 1:
                        legal_actions.append(ChooseCard1Garden2LargestAction(card=card))
                    else:
                        legal_actions.append(ChooseCard1Garden3LargestAction(card=card))

                if not garden or card < garden[0]:  # can add to the top
                    if garden_idx == 0:
                        legal_actions.append(ChooseCard1Garden1SmallestAction(card=card))
                    elif garden_idx == 1:
                        legal_actions.append(ChooseCard1Garden2SmallestAction(card=card))
                    else:
                        legal_actions.append(ChooseCard1Garden3SmallestAction(card=card))

            # Always can discard a card
            legal_actions.append(ChooseCard1DiscardAction(card=card))

        return legal_actions


