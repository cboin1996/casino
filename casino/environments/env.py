from abc import ABC, abstractmethod
from typing import Tuple
from enum import Enum
class Env(ABC):
    """Abstract RL environment class

    Args:
        ABC (abc.ABC): the abstract class interface
    """

    @abstractmethod
    def reset(self) -> None:
        """Override this method implementing logic for resetting the environment
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
    WINNER = 0,
    LOSER = 1,
    DRAW = 2

