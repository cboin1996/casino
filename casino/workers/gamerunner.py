from casino.workers.runner import AbstractRunner
from casino.util.env import varia

import os, sys
import logging
import argparse
import enum
import numpy as np

logger = logging.getLogger(__name__)

class GamePlayer(AbstractRunner):
    """High level class for playing games as a human or as an AI.
    """
    def __init__(self, base_dir: str, launch_time: str, args: argparse.ArgumentParser):
        """Initialize the game runner

        Args:
            base_dir (str): the base directory of the program
            launch_time (str): the timestamp for when the program was launched
            args: (argparse.ArgumentParser): the parsed arguments from the CLI
        """
        super().__init__(args.agent, base_dir, launch_time)
        self.game_id = args.game_id
        self.agent_name = args.agent
        self.initialized = False
        self.playing = False
        self.args = args

    def initialize(self) -> bool:
        logger.info("Setting up game environment for training")
        # Setup the game environment
        is_game_setup = self.set_game(self.game_id)
        if is_game_setup:
            logger.info(f"Game [{self.game_env.name}] has been setup!")
        else:
            logger.error(f"Game [{self.game_env.name}] could not be setup!")
            return False
            
        # Choose the agent
        is_agent_setup = self.set_agent(self.game_env.n_actions, self.args)

        if is_agent_setup:
            logger.info(f"Agent [{self.agent.name}] has been setup!")
        else:
            logger.error(f"Agent [{self.agent.name}] could not be setup!")
            return False

    def run(self) -> bool:
        terminal = False
        prev_state = self.game_env.reset()
        state = prev_state

        while not terminal:
            action = self.agent.get_policy(state)
            state, _, terminal = self.game_env.step(action)
        return True
    
    def train(self) -> bool:
        """High level trainer method including saving results to disk

        Returns:
            bool: true if the training was a success
        """
        n_episodes = self.args.n_episodes
        logger.info(f"Launching training session with {n_episodes} episodes!")
        for i in range(n_episodes):
            if (i % 1000 == True):
                logger.info(f"Reached episode [{i}] of [{n_episodes}].")

            self.agent.train_episode(self.game_env, i)
        
        logger.info("Training session complete.")
        self.agent.save_training_data(self.output_dir, self.agent.cumulative_episodic_rewards)

    def evaluate(self, session_dir) -> bool:
        pass # TODO: IMPLEMENT IF NEEDED


    def quit(self) -> None:
        logger.info("Quitting. Saving training results")
        logger.info("Quit completed")