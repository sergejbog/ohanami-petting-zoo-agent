from ..Card import OhanamiCard

# ================================================
# Action_ids:
#       0-119     -> place_card_in_garden_1_smallest_id
#       120-239   -> place_card_in_garden_1_largest_id
#       240-359   -> place_card_in_garden_2_smallest_id
#       360-479   -> place_card_in_garden_2_largest_id
#       480-599   -> place_card_in_garden_3_smallest_id
#       600-719   -> place_card_in_garden_3_largest_id
#       720-839   -> discard_card_id
# ================================================

BASE_ACTION = 120

choose_1_card_garden_1_smallest_id = 0
choose_1_card_garden_1_largest_id = 1 * BASE_ACTION
choose_1_card_garden_2_smallest_id = 2 * BASE_ACTION
choose_1_card_garden_2_largest_id = 3 * BASE_ACTION
choose_1_card_garden_3_smallest_id = 4 * BASE_ACTION
choose_1_card_garden_3_largest_id = 5 * BASE_ACTION
choose_1_card_discard_id = 6 * BASE_ACTION


class ActionEvent(object):
    def __init__(self, action_id: int):
        self.action_id = action_id

    def __eq__(self, other):
        result = False
        if isinstance(other, ActionEvent):
            result = self.action_id == other.action_id
        return result

    @staticmethod
    def get_num_actions():
        """ Return the number of possible actions in the game
        """
        return choose_1_card_discard_id + BASE_ACTION

    @staticmethod
    def decode_action(action_id) -> 'ActionEvent':
        """ Action id -> the action_event in the game.

        Args:
            action_id (int): the id of the action

        Returns:
            action (ActionEvent): the action that will be passed to the game engine.
        """
        if choose_1_card_garden_1_smallest_id <= action_id < choose_1_card_garden_1_largest_id:
            card_id = action_id - choose_1_card_garden_1_smallest_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1Garden1SmallestAction(card=card)

        elif choose_1_card_garden_1_largest_id <= action_id < choose_1_card_garden_2_smallest_id:
            card_id = action_id - choose_1_card_garden_1_largest_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1Garden1LargestAction(card=card)

        elif choose_1_card_garden_2_smallest_id <= action_id < choose_1_card_garden_2_largest_id:
            card_id = action_id - choose_1_card_garden_2_smallest_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1Garden2SmallestAction(card=card)

        elif choose_1_card_garden_2_largest_id <= action_id < choose_1_card_garden_3_smallest_id:
            card_id = action_id - choose_1_card_garden_2_largest_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1Garden2LargestAction(card=card)

        elif choose_1_card_garden_3_smallest_id <= action_id < choose_1_card_garden_3_largest_id:
            card_id = action_id - choose_1_card_garden_3_smallest_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1Garden3SmallestAction(card=card)

        elif choose_1_card_garden_3_largest_id <= action_id < choose_1_card_discard_id:
            card_id = action_id - choose_1_card_garden_3_largest_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1Garden3LargestAction(card=card)

        elif choose_1_card_discard_id <= action_id < ActionEvent.get_num_actions():
            card_id = action_id - choose_1_card_discard_id
            card = OhanamiCard(card_id + 1)
            action_event = ChooseCard1DiscardAction(card=card)

        else:
            raise Exception("decode_action: unknown action_id={}".format(action_id))

        return action_event


class ChooseCard1Garden1SmallestAction(ActionEvent):

    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_garden_1_smallest_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_garden_1_smallest {}".format(str(self.card))


class ChooseCard1Garden1LargestAction(ActionEvent):

    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_garden_1_largest_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_garden_1_largest {}".format(str(self.card))


class ChooseCard1Garden2SmallestAction(ActionEvent):

    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_garden_2_smallest_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_garden_2_smallest {}".format(str(self.card))


class ChooseCard1Garden2LargestAction(ActionEvent):
    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_garden_2_largest_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_garden_2_largest {}".format(str(self.card))


class ChooseCard1Garden3SmallestAction(ActionEvent):
    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_garden_3_smallest_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_garden_3_smallest {}".format(str(self.card))


class ChooseCard1Garden3LargestAction(ActionEvent):
    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_garden_3_largest_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_garden_3_largest {}".format(str(self.card))


class ChooseCard1DiscardAction(ActionEvent):
    def __init__(self, card: OhanamiCard):
        card_id = card.get_card_number()
        super().__init__(action_id=choose_1_card_discard_id + card_id)
        self.card = card

    def __str__(self):
        return "choose_card_1_discard {}".format(str(self.card))
