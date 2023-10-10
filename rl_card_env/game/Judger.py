from rl_card_env.game.Card import OhanamiCard, CardColors

BLUE_CARDS_BASE_POINTS = 3
GREEN_CARDS_BASE_POINTS = 4
GRAY_CARDS_BASE_POINTS = 7


class OhanamiJudger:
    @staticmethod
    def get_points(card: OhanamiCard, round_counter: int, num_of_pink_cards: int):
        """ Get the points of a card based on the round

        Args:
            card (object): OhanamiCard object
            round_counter (int): The round counter
            num_of_pink_cards (int): The number of pink cards in all gardens

        Returns:
            points (int): The points of the card
        """
        if card.color == CardColors.BLUE:
            if round_counter == 0:
                return 3 * BLUE_CARDS_BASE_POINTS
            elif round_counter == 1:
                return 2 * BLUE_CARDS_BASE_POINTS
            return BLUE_CARDS_BASE_POINTS

        if card.color == CardColors.GREEN:
            if round_counter == 0 or round_counter == 1:
                return 2 * GREEN_CARDS_BASE_POINTS
            return GREEN_CARDS_BASE_POINTS

        if card.color == CardColors.GRAY:
            return GRAY_CARDS_BASE_POINTS

        if card.color == CardColors.PINK:
            return num_of_pink_cards
