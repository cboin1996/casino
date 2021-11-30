from casino.agents.monte import MonteCarlo
from casino.agents.qlearn import QLearningAgent, SarsaAgent
from casino.environments.easy21.easy21 import Easy21
from casino.environments.env import Games
from casino.agents.agent import Agent
from casino.agents.human import HumanAgent
from casino.util.env import varia
from casino.io import disk

from abc import ABC, abstractmethod
import argparse
import enum
import logging
import os
import numpy as np

from casino.plotting import plotlib

logger = logging.getLogger(__name__)

class AbstractRunner(ABC):
    def __init__(self, name, base_dir: str, launch_time: str):
        self.name = name
        self.base_dir = base_dir
        self.launch_time = launch_time
        self.output_dir = os.path.join(self.base_dir, varia.DATA_DIR, self.launch_time)

        self.is_initialized = False
        self.terminate = False
    
    @abstractmethod
    def initialize(self) -> bool:
        """Override this method with logic for initializing for training

        Returns:
            bool: true if initialization was a success
        """
        pass

    @abstractmethod
    def run(self) -> bool:
        """Override this method with logic performing a single game

        Returns:
            bool: true if the game is over
        """
        pass
    
    @abstractmethod
    def train(self) -> bool:
        """Override this method for logic for training a model 

        Args:
            args ([type]): command line arguments

        Returns:
            bool: true if training completes successfully
        """
        pass
    
    @abstractmethod
    def evaluate(self, session_dir: str) -> bool:
        """Override this method with logic for evaluating a training session/updating results

        Args:
            session_dir (str): the path to the result directory

        Returns:
            bool: True if the evaluation terminates successfully.
        """
        pass
    
    @abstractmethod
    def quit(self) -> None:
        """Override this method with any logic to run while quitting.
        """
        pass
    
    def setup(self):
        self.is_initialized = self.initialize()

    def play(self):
        if self.is_initialized:
            self.playing = True
            logger.info(f"Running!")
            while not self.terminate:
                self.terminate = self.run()
        else:
            logger.error(f"Could not run due to an initialization error!")
        
        self.shutdown()
    
    def train_session(self):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        self.train()
        self.plot_results(self.output_dir)
        self.save_metadata()
        self.shutdown()

    
    def perform_evaluation(self, session_dir):
        self.evaluate(session_dir)
        self.plot_results(self.output_dir)
        self.shutdown()
    
    def shutdown(self):
        logger.info("Shutting down")
        self.quit()
        logger.info("Shutdown completed")

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
            
    def set_agent(self, n_actions: int, args: argparse.ArgumentParser) -> bool:
        """Sets the agent to use for playing the game

        Args:
            agent (str): the str description of the agent
            game_id (int): the id of the game
            n_actions (int): number of discrete actions for the agent to explore

        Raises:
            ValueError: raised if the agent is undefined
        """
        try:
            if not self.playing:
                self.agent_type = Agent[args.agent.upper()]
                if self.agent_type == Agent.HUMAN:
                    self.agent = HumanAgent(n_actions, args)
                elif self.agent_type == Agent.MONTE:
                    self.agent = MonteCarlo(n_actions, args)
                elif self.agent_type == Agent.SARSA:
                    self.agent = SarsaAgent(n_actions, args)
                elif self.agent_type == Agent.QLEARN:
                    self.agent = QLearningAgent(n_actions, args)
                else:
                    return False
            return True
        except KeyError:
            logger.error("Invalid agent type!", exc_info=True)
            return False
    
    def plot_results(self, output_dir):
        """Run the appropriate plotter for the game environment and agent

        Args:
            output_dir (str): the output directory for plots
        """
        fname = os.path.join(output_dir, varia.VAL_FUNC_PLOT_NAME)
        if self.game_type == Games.EASY21:
            plotlib.plot_two_dim_value_func(self.agent.policy_func, Games.EASY21.name, 
                                            "Dealer showing","Player Sum", "A", self.agent.n_actions*5,
                                            fname)
    
    def save_metadata(self):
        meta = {}
        meta[varia.META_GAME_KEY] = self.game_type.value
        meta[varia.META_AGENT_KEY] = self.agent_type.value
        disk.write_json(os.path.join(self.output_dir, varia.META_FNAME), meta)