from abc import ABC, abstractmethod
from typing import Tuple
from enum import Enum
class Env(ABC):
    """Abstract RL environment class

    Args:
        ABC (abc.ABC): the abstract class interface
    """
    def __init__(self, name: str, num_actions: int):
        """Constructor, with a name for the environment

        Args:
            name (str): the name of the environment
        """
        self.name = name
        self.n_actions = num_actions

    @abstractmethod
    def reset(self) -> list:
        """Override this method implementing logic for resetting the environment
        Return: the state upon reset
        """
        pass

    @abstractmethod
    def step(self, action) -> Tuple:
        """Override this method including logic for advancing the environment

        Args:
            action (optional): the action for the environment to take on this step
            return (tuple): tuple of: state, reward, terminal
        """
        pass

    @abstractmethod
    def isterminal(self) -> bool:
        """Override method defining logic for the environment is terminal
        Returns:
            bool: whether the environment is in a terminal state or not
        """

class Result(Enum):
    """The result for a game
    """
    WINNER = 0
    LOSER = 1
    DRAW = 2

class Games(Enum):
    """Enum for the types of games
    """
    EASY21 = 0