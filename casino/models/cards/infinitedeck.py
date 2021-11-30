import numpy as np
import random
from typing import Optional

from casino.models.cards.card import Card
from casino.models.cards.color import Color

class InfiniteDeck:
    """Implementation of an inifinite deck of cards
    Instantiations of this class provide an infinite deck of cards,
    where the lowest and highest card rank are configurable.
    In addition, the color bias may be set, defining the probability
    of the drawed color from the deck upon a sample
    """
    
    def __init__(self, low_bound, high_bound, color_bias):
        """Default constructor

        Args:
            low_bound (int): the lowest card in the deck
            high_bound (int): the highest card in the deck
            color_bias (float): probabilistic ratio of drawing red to black
        """
        self.low_bound = low_bound
        self.high_bound = high_bound
        self.color_bias = color_bias
    
    def draw(self, color=None):
        """Draws a card from the deck
        Args:
            color (Color, optional) : force a color in the draw
        """
        card_number = np.random.randint(1,10, dtype=int)
        if color is None:
            card_color = random.choices([Color.RED, Color.BLACK], [1/3,1])[0]
        else:
            card_color = color
        return Card(card_color, card_number)

        