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
        super().__init__("Easy21", 2)
        logger.info("Initializing Easy21!")
        self.player = Player("player")
        self.dealer = Player("dealer")

    def reset(self) -> list:
        logger.debug("Resetting game environment!")
        self.deck = InfiniteDeck(1, 10, 0.33)
        self.player.reset(self.deck.draw(Color.BLACK))
        self.dealer.reset(self.deck.draw(Color.BLACK))
        self.turn_count = 0
        self.terminal = False

        return self.get_state()

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
        else:
            logger.error("Invalid action passed!")

        self.check_for_winner()
        logger.debug(f"Scores: {self.player.name} = {self.player.score} | {self.dealer.name} = {self.dealer.score} ")
        reward = self.get_reward()
        logger.debug(f"-------------------------------------------------------------------------")
        return self.get_state(), reward, self.isterminal() 

    def play_dealer(self) -> None:
        """Runs the dealer for the game, drawing cards and 
           playing according the the rule that the dealer sticks at a score of >=17.
        """
        logger.debug("Dealer is beginning its turn.")
        while self.dealer.score < 17 and not self.dealer.isbust():
            self.dealer.hit(self.deck.draw())

        if self.dealer.score >= 17 and not self.dealer.isbust():
            self.dealer.stick()
    
    def check_for_winner(self):
        """Selects a winner for the game
        """
        if self.player.isbust(print_out=True):
            self.dealer.winner = True
            self.terminal = True
            return
        if self.dealer.isbust(print_out=True):
            self.player.winner = True
            self.terminal = True
            return 

        if self.player.last_action == Action.STICK and self.dealer.last_action == Action.STICK:
            msg = f"Player has %s score than dealer!"
            if self.player.score < self.dealer.score:
                logger.debug(msg % ("lower"))
                self.dealer.winner = True
            elif self.player.score > self.dealer.score:
                logger.debug(msg % ("higher"))
                self.player.winner = True
            elif self.player.score == self.dealer.score:
                logger.debug(f"A draw has occured!")
            self.terminal = True

    def get_reward(self):
        """Get the reward for the game, and set the terminal flag to indicate the game is over if it has completed
        """
        if self.player.winner:
            logger.debug("Returning reward of 1!")
            return 1
        elif self.dealer.winner:
            logger.debug("Returning reward of -1!")
            return -1
        else:
            logger.debug("Returning reward of 0!")
            return 0
    
    def get_state(self):
        """Get the state for the easy21 game environment. 
            For this implementation, the state is defined as a tuple
            containing the dealers first card, and the players score.
            If the environment is terminated a null state is returned (0, 0)
        """
        if self.isterminal():
            return 0,0
        return self.dealer.cards[0].number, self.player.score

    def isterminal(self) -> bool:
        return self.terminal

        
