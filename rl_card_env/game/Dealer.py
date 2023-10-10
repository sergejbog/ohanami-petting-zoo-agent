
from rl_card_env.game.utils.utils import init_deck
from rl_card_env.game.Player import OhanamiPlayer


class OhanamiDealer:
    """ Initialize an Ohanami dealer class
    """
    def __init__(self, np_random):
        self.np_random = np_random
        self.deck = init_deck()
        self.discards = []
        self.shuffle()

    def shuffle(self):
        """ Shuffle the deck
        """
        self.np_random.shuffle(self.deck)

    def deal_cards(self, player: OhanamiPlayer, num):
        """ Deal some cards from deck to one player

        Args:
            player (OhanamiPlayer): The object of OhanamiPlayer
            num (int): The number of cards to be dealt
        """
        for _ in range(num):
            player.add_to_hand(self.deck.pop())

    def discard_card(self, card):
        """ Discard a card

        Args:
            card (OhanamiCard): The card to be discarded
        """
        self.discards.append(card)
