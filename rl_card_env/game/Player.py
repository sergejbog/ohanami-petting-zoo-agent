from rl_card_env.game.Card import OhanamiCard, CardColors
from rl_card_env.game.utils.action_event import ActionEvent
from typing import List
from rl_card_env.game.utils.garden_position import POSITION


class OhanamiPlayer:

    def __init__(self, player_id, num_players):
        """ Initialize a player.

        Args:
            player_id (int): The id of the player
            num_players (int): The number of players in the game
        """
        self.player_id = player_id
        self.hand: List[OhanamiCard] = []
        self.gardens = [[], [], []]
        self.points = 0
        self.num_of_pink_cards = 0

        # For tracking cards that the player knows are in other players' hands
        self.known_hands = [[] for _ in range(num_players - 1)]

        # For tracking cards that the player knows
        self.remaining_cards = [OhanamiCard(i) for i in range(1, 120)]

        # For tracking actions in a turn to not reveal them to other players before everyone has chosen
        self.selected_actions: List[ActionEvent] = []

    def add_to_hand(self, card: OhanamiCard):
        """ Add a card to the hand of the player

        Args:
            card (OhanamiCard): The card to be added
        """
        self.hand.append(card)

    def remove_from_hand(self, card: OhanamiCard):
        """ Remove a card from the hand of the player

        Args:
            card (OhanamiCard): The card to be removed
        """
        self.hand.remove(card)

    def add_to_garden(self, card: OhanamiCard, garden_index, position: POSITION):
        """ Add a card to the garden of the player and increase the points of the player
            The card is added to the beginning of the garden if the position is POSITION.SMALLEST, otherwise it is added to the end of the garden

        Args:
            card (OhanamiCard): The card to be added
            garden_index (int): The index of the garden
            position (POSITION): The position of the card in the garden
        """
        if position == POSITION.SMALLEST:
            self.gardens[garden_index].insert(0, card)
        else:
            self.gardens[garden_index].append(card)

        if card.color == CardColors.PINK:
            self.num_of_pink_cards += 1

    def add_points(self, points: int):
        """ Add points to the player based on the card

        Args:
            points (int): The points to be added
        """
        self.points += points

    def add_action(self, action: ActionEvent):
        """ Add an action to the player's selected actions

        Args:
            action (ActionEvent): The action to be added
        """
        self.selected_actions.append(action)

    def remove_remaining_cards(self, card: OhanamiCard):
        """ Add a card to the player's known cards

        Args:
            card (OhanamiCard): The card to be added
        """
        self.remaining_cards.remove(card)

    def get_cards_from_gardens(self):
        """ Get all cards in the player's gardens """
        cards = [[], [], []]
        for i, garden in enumerate(self.gardens):
            cards[i] = [card for card in garden]
        return cards

    def update_known_hands_after_pass(self):
        """Update the known hands after passing cards to the left."""
        self.known_hands.insert(0, self.known_hands.pop())  # Rotate the list to the left

    def receive_hand(self, hand):
        """Receive a new hand of cards and update known hands."""
        missing_cards = set(self.known_hands[0]) - set(hand)  # Determine cards that were either placed or discarded
        for card in missing_cards:
            if card not in self.remaining_cards:  # If a card was already placed in a garden or discarded before, then it was placed in the garden
                self.known_hands[0].remove(card)  # Remove card from expected cards in known hand
        self.hand = hand  # Update player's hand
