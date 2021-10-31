from casino.models.cards.color import Color

class Card:
    """Simple card class, with integer representing the card rank and a color enum
    """
    def __init__(self, color: Color, number: int) -> None:
        self.color = color
        self.number = number

    def __lt__(self, other):
        if self.number < other.number:
            return True
    
    def __lt__(self, other):
        if self.number <= other.number:
            return True

    def __gt__(self, other):
        if self.number > other.number:
            return True
    def __ge__(self, other):
        if self.number >= other.number:
            return True

    def __eq__(self, other):
        if self.number == other.number and self.color == other.color:
            return True

    def __ne__(self, other):
        if self.number != other.number or self.color != other.color:
            return True
    
    def __str__(self):
        return f"(color : {self.color}, number: {self.number})"