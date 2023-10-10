from rl_card_env.game.Card import OhanamiCard, CardColors
from termcolor import colored
from typing import List
from colorama import init
init(autoreset=True)


def init_deck():
    """Generate Ohanami deck of 120 cards
    """
    deck = []
    for number in range(1, 121):  # 1 to 120 inclusive
        deck.append(OhanamiCard(number))
    return deck


def print_cards(cards: List[OhanamiCard]):
    """ Print out card in a nice form

    Args:
        cards (List[OhanamiCard]): A list of Ohanami cards
    """
    for i, card in enumerate(cards):

        # Color the numbers based on card color
        if card.color == CardColors.BLUE:
            print(colored(card.number, 'blue'), end='')
        elif card.color == CardColors.GREEN:
            print(colored(card.number, 'green'), end='')
        elif card.color == CardColors.GRAY:
            print(colored(card.number, 'dark_grey'), end='')
        elif card.color == CardColors.PINK:
            print(colored(card.number, 'magenta'), end='')

        if i < len(cards) - 1:
            print(', ', end='')
