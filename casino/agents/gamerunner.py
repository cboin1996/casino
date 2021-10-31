import enum

from casino.environments.easy21.easy21 import Easy21
class GameRunner:
    """High level class for playing games as a human or as an AI.
    """
    def __init__(self, game_id: int, mode: str):
        """Initialize the game runner

        Args:
            game_id (int): the expected game to play (see Games enum class)
            mode (str): the mode. human, monte, or td are supported for playing as
            human, monte carlo learning or td learning.
        """
        self.game_type = Games(game_id)
        self.mode = mode

    def setup(self):
        if self.game_type == Games.EASY21:
            self.game_env = Easy21()

    def run(self):
        if self.mode == "human":
            self.play_as_human()
        elif self.mode == "monte":
            self.play_as_monte()
        elif self.mode == "td":
            self.play_as_td()
        else:
            raise ValueError(f"Unknown mode was passed to gamerunner: [{self.mode}]")
    
    def play_as_human(self):
        """Play a game as a human, through command prompt
        """
        quit_str = "q"
        while not quit_str:
            self.game_env.step()

    def play_as_monte(self):
        pass

    def play_as_td(self):
        pass


class Games(enum.Enum):
    EASY21 = 0