import enum

from casino.environments.easy21.easy21 import Easy21

import logging

logger = logging.getLogger(__name__)
class GameRunner:
    """High level class for playing games as a human or as an AI.
    """
    def __init__(self, game_id: int, agent: str):
        """Initialize the game runner

        Args:
            game_id (int): the expected game to play (see Games enum class)
            agent (str): the agent. playing as
                human, monte carlo learning or td learning is supported
        """
        self.game_id = game_id
        self.agent_name = agent
        self.initialized = False
        self.playing = False

    def setup(self):
        logger.info("Setting up game environment")
        # Setup the game environment
        is_game_setup = self.set_game(self.game_id)
        is_agent_setup = self.set_agent(self.agent_name)

        # Choose the agent
        if (is_game_setup and is_agent_setup):
            logger.info(f"Game [{self.game_env.name}] has been setup!")
            self.initialized =  True
        else:
            logger.error(f"Game [{self.game_env.name}] could not be setup!")
            self.initialized = False

    def run(self):
        if self.initialized:
            self.playing = True
            logger.info(f"Running!")
        else:
            logger.error(f"Could not run due to an initialization error!")

    def set_game(self, game_id) -> bool:
        """Set the game environment

        Args:
            game_id (int): the id for the game
        """
        try:
            self.game_type = Games(game_id)
            if self.game_type == Games.EASY21:
                self.game_env = Easy21()
            else:
                raise NotImplementedError("Game id [{game_id}] has not been implemented!")
                
            return True
        except ValueError:
            logger.error(f"Game w/ id [{game_id}] is undefined!", exc_info=True)
            return False
            
    def set_agent(self, agent: str) -> bool:
        """Sets the agent to use for playing the game

        Args:
            agent (str): the str description of the agent

        Raises:
            ValueError: raised if the agent is undefined
        """
        try:
            if not self.playing:
                self.agent = Agent[agent.upper()]
                if self.agent == Agent.HUMAN:
                    #self.agent = 
                    pass
                elif self.agent == Agent.MONTE:
                    # TODO: Implement monte carlo agent
                    pass
                elif self.agent == Agent.TD:
                    # TODO: implement TD agent
                    pass
                else:
                    return False
            return True
        except KeyError:
            logger.error("Invalid agent type!", exc_info=True)
            return False
class Games(enum.Enum):
    EASY21 = 0

class Agent(enum.Enum):
    """Enum the game mode.. defines the type of agent to use for the game.

    Types:
        HUMAN = a human playable environment
        monte = play using monte carlo trained model
        TD    = play using td learning trained model
    """
    HUMAN = 0,
    MONTE = 1,
    TD = 2