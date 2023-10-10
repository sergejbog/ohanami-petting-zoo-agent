from enum import Enum


class CardColors(Enum):
    BLUE = 1
    GREEN = 2
    GRAY = 3
    PINK = 4


CARD_COLOR_MAP = {
    CardColors.BLUE: [116, 50, 16, 58, 64, 68, 38, 104, 110, 10, 2, 88, 92, 44, 74, 34, 62, 82, 4, 22, 52, 106, 118, 8, 100, 26, 32, 40, 46, 86, 94, 80, 76, 20],
    CardColors.GREEN: [120, 102, 48, 9, 75, 15, 12, 6, 3, 108, 111, 114, 51, 60, 69, 66, 72, 87, 18, 36, 45, 30, 24, 54, 96, 93, 117, 90, 81, 78, 99, 57, 39, 33, 27],
    CardColors.GRAY: [56, 28, 91, 42, 49, 35, 14, 119, 77, 98, 21, 63, 70, 105, 84, 112, 7],
    CardColors.PINK: [95, 47, 19, 13, 5, 79, 103, 113, 89, 85, 29, 61, 1, 67, 55, 65, 115, 109, 107, 97, 59, 101, 11, 17, 83, 23, 25, 37, 71, 73, 41, 43, 53, 31]
}


class OhanamiCard:
    def __init__(self, number):
        """ Initialize the class of OhanamiCard

        Args:
            number (int): The number on the card
        """
        self.number = number
        self.color = self.get_color_from_number(number)
        self.str = self.get_str()

    def get_card_number(self):
        """ Get the card number starting from 0 to 119, instead of 1 to 120"""
        return self.number - 1

    def get_str(self):
        """ Get the string representation of card

        Return:
            (str): The string of card's color and number
        """
        return self.color.name + '-' + str(self.number)

    @staticmethod
    def get_color_from_number(number):
        """ Get the card color based on the card number

        Args:
            number (int): The number on the card

        Returns:
            color (str): The color corresponding to the card number
        """
        for color, numbers in CARD_COLOR_MAP.items():
            if number in numbers:
                return color
        return None

    def __str__(self):
        return self.str

    def __lt__(self, other):
        if isinstance(other, OhanamiCard):
            return self.number < other.number
        return NotImplemented

    def __le__(self, other):
        if isinstance(other, OhanamiCard):
            return self.number <= other.number
        return NotImplemented

    def __eq__(self, other):
        if isinstance(other, OhanamiCard):
            return self.number == other.number
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, OhanamiCard):
            return self.number != other.number
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, OhanamiCard):
            return self.number > other.number
        return NotImplemented

    def __ge__(self, other):
        if isinstance(other, OhanamiCard):
            return self.number >= other.number
        return NotImplemented
