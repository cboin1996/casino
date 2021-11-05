from casino.models.cards.card import Card, Color
import logging
from enum import Enum

logger = logging.getLogger(__name__)

class Player:
    """Simple player class for Easy21
    """
    def __init__(self, name):
        logger.info(f"Initializing new Player!")
        self.name = name
    
    def reset(self, card: Card):
        """Reset with a black card, and a score
        """
        logger.info(f"Resetting Player '{self.name}' with card {card}!")
        self.cards = [card]
        self.score = card.number
        self.last_action = Action.NONE
        self.turn_count = 0
    
    def hit(self, card: Card) -> None:
        """Add a card to the players hand and update their score

        Args:
            card (Card): the card to add
        """
        self.turn_count += 1
        logger.info(f"Turn [{self.turn_count}: {self.name} hits receiving card {card}!")
        self.cards.append(card)
        self.score = self.get_card_score(card)
        self.last_action = Action.HIT
        logger.info(f"Turn [{self.turn_count}: {self.name} has score updated to {self.score}!")
    
    def stick(self) -> None:
        """Stay with current hand, and update the last action of the player.
        """
        self.turn_count += 1
        logger.info(f"Player {self.name} has chosen to stick with score {self.score}!")
        self.last_action = Action.STICK
    
    def get_card_score(self, card: Card) -> int:
        """Get the score of a card

        Args:
            card (Card): the card objet

        Returns:
            int: the score of the card (+ if black, - if negative)
        """
        if card.color == Color.RED:
            return -card.number
        else:
            return card.number
    
    def isbust(self) -> bool:
        """Get whether the player has bust. Rules for easy21 define bust as having scores < 1 or > 21.

        Returns:
            bool: true if the player has gone bust
        """
        if self.score < 1 or self.score > 21:
            logger.info(f"Player {self.name} has gone bust with score {self.score}!")
            return True
        else:
            return False
            
class Action(Enum):
    """Enum for actions related to easy21:
    \nSTICK = 0
    \nHIT   = 1
    \nNONE  = 2 

    Args:
        Enum (enum): inherited enum class
    """
    STICK = 0,
    HIT = 1,    
    NONE = 2,

