import argparse
from casino.agents.agent import AbstractAgent

import numpy as np
import logging
logger = logging.getLogger(__name__)

class MonteCarlo(AbstractAgent):
    """Monte carlo agent. 
    See Sutton and Barto pg. 101 (2018) Reinforcement Learning for pseudocode
    """
    def __init__(self, n_actions: int, args: argparse.ArgumentParser):
        """Default constructor
        """
        super().__init__(n_actions, "MonteCarlo", args.policy, args.eps_const)
        self.gamma = args.gamma
        self.states = []
        self.actions = []
        self.rewards = []

    def update_policy(self):
        rewards = np.array(self.rewards)
        for i in range(len(self.states)):
            state = self.states[i]
            action = self.actions[i]

            discounts = np.array([self.gamma ** n for n in range(len(rewards[i:]))])
            returns = sum(rewards[i:] * discounts)
            self.q_func[state][action] += self.get_alpha(state, action) * (returns - self.q_func[state][action])
            self.policy_func = dict((state, np.argmax(q_value)) for state, q_value in self.q_func.items())

    def save(self, output_dir) -> bool:
        logger.info("Saving.")
        return super().save(output_dir)

    def train_episode(self, env, episode: int):
        self.states, self.actions, self.rewards = self.generate_episode(env)
        self.cumulative_episodic_rewards.append(sum(self.rewards))
        self.update_policy()

    def generate_episode(self, env) -> tuple:
        """Episode generation method

        Returns:
            list: the trajectory for the episode containg tuples of (state, action, reward)
        """
        state = env.reset()
        states = []
        actions = []
        rewards = []
        terminal = False
        while not terminal:
            action = self.policy(state)
            next_state, reward, terminal = env.step(action)
            state = next_state
            states.append(state)
            actions.append(action)
            rewards.append(reward)        
        return states, actions, rewards