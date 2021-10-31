from casino.environments.env import Env
from casino.environments.easy21.player import Player, Action

from casino.models.cards.card import Card
from casino.models.cards.color import Color
from casino.models.cards.infinitedeck import InfiniteDeck


from enum import Enum
from typing import List

import logging

from casino.environments.easy21.player import Player

logger = logging.getLogger(__name__)

class Easy21(Env):
    """Environment class for Easy21.
    """
    def __init__(self):
        """Initializes the game, with a black card sampled from the deck for both the player and dealer
        """
        logger.info("Initializing Easy21!")
        self.player = Player("player")
        self.dealer = Player("dealer")

        self.reset()

    def reset(self) -> None:
        logger.info("Resetting game environment!")
        self.deck = InfiniteDeck(1, 10, 0.33)
        self.player.reset(self.deck.draw(Color.BLACK))
        self.dealer.reset(self.deck.draw(Color.BLACK))
        self.turn_count = 0
        self.terminal = False

    def step(self, action: int) -> tuple:
        """Advance the game a 'step' or turn

        Args:
            action (int): the action to take. See Action enum.

        Returns:
            tuple: the state, reward, terminal observation
        """
        action = Action(action)
        if action == Action.HIT:
            self.player.hit(self.deck.draw())

        elif action == Action.STICK:
            self.player.stick()
            self.play_dealer() # dealer begins
            reward = self.get_reward()
        else:
            logger.error("Invalid action passed!")

        return self.get_state(), reward, self.isterminal() 

    def play_dealer(self) -> None:
        """Runs the dealer for the game, drawing cards and 
           playing according the the rule that the dealer sticks at a score of >=17.
        """
        logger.info("Dealer is beginning its turn.")
        while self.dealer.score < 17 and not self.dealer.isbust():
            self.dealer.hit(self.deck.draw())
    
    def get_reward(self):
        """Get the reward for the game, and set the terminal flag to indicate the game is over.
        """
        self.terminal = True
        if self.player.isbust():
            logger.info("Player has busted, returning reward of -1.")
            return -1
        if self.dealer.isbust():
            logger.info("Dealer has busted, returning reward of -1.")
            return 1

        msg = f"Player(s={self.player.score}) has %s score than dealer(s={self.dealer.score}), returning reward of 1."
        if self.player.score < self.dealer.score:
            logger.info(msg.format("lower"))
            return -1
        elif self.player.score > self.dealer.score:
            logger.info(msg.format("higher"))
            return 1
        else:
            logger.info("A draw has occured! Player(s={self.player.score}), dealer(s={self.dealer.score})! Returning reward of 0")
            return 0
    
    def get_state(self):
        """Get the state for the easy21 game environment. 
            For this implementation, the state is defined as a tuple
            containing the dealers first card, and the players score.
        """
        return self.dealer.cards[0], self.player.score

    def isterminal(self) -> bool:
        return self.terminal

        
