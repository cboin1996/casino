import argparse
import logging
import numpy as np
import os

from casino.agents.agent import AbstractAgent
from casino.io import disk
from casino.plotting import plotlib
from casino.util.env import varia

logger = logging.getLogger(__name__)
class SarsaAgent(AbstractAgent):
    """Q learning agent using SARSA.
    See Sutton and Barto pg. 130 (2018) Reinforcement Learning for pseudocode


    """
    def __init__(self, n_actions: int, args: argparse.ArgumentParser):
        """Default constructor
        """
        super().__init__(n_actions, "Sarsa", args.policy, args.eps_const)
        self.gamma = args.gamma
        self.opt_q = load_opt_q(args.opt_q_path)
        self.mse = []

    def train_episode(self, env, episode: int):
        state = env.reset()
        action = self.policy(state)

        rewards = []
        terminal = False
        while not terminal:
            next_state, reward, terminal = env.step(action)
            next_action = np.argmax(self.q_func[next_state])
            td_target = reward + self.gamma * self.q_func[next_state][action]
            td_error  = td_target - self.q_func[state][action]

            self.q_func[state][action] = self.q_func[state][action] + super().get_alpha(state, action) * td_error

            state = next_state
            action = next_action
            rewards.append(reward)
          

        self.cumulative_episodic_rewards.append(sum(rewards))
        episodic_mse = compute_mse(self.opt_q, self.q_func)
        self.mse.append(episodic_mse)
        self.update_policy()

        if (episode % 1000 == 0):
            logger.info(f"MSE = [{episodic_mse}] at episode [{episode}]!")

    def update_policy(self):
        self.policy_func = dict((state, np.argmax(q_value)) for state, q_value in self.q_func.items())


    def save(self, output_dir) -> bool:
        logger.info("Saving.")
        plotlib.line_plot(np.arange(1,len(self.mse)+1), self.mse, 
            "SARSA", "Training episode", "Mean square error", os.path.join(output_dir, varia.MSE_PLOT_NAME))
        return super().save(output_dir)

class QLearningAgent(AbstractAgent):
    """Q learning agent
    See Sutton and Barto pg. 131 (2018) Reinforcement Learning for pseudocode
    """
    def __init__(self, n_actions: int, args: argparse.ArgumentParser):
        """Default constructor
        """
        super().__init__(n_actions, "Qlearn", args.policy, args.eps_const)
        self.gamma = args.gamma
        self.opt_q = load_opt_q(args.opt_q_path)
        self.mse = []

    def train_episode(self, env, episode: int):
        state = env.reset()

        rewards = []
        terminal = False
        while not terminal:
            action = self.policy(state)
            next_state, reward, terminal = env.step(action)
            next_action = np.argmax(self.q_func[next_state])
            td_target = reward + self.gamma * self.q_func[next_state][next_action]
            td_error  = td_target - self.q_func[state][action]

            self.q_func[state][action] = self.q_func[state][action] + super().get_alpha(state, action) * td_error

            state = next_state
            rewards.append(reward)
          

        self.cumulative_episodic_rewards.append(sum(rewards))
        episodic_mse = compute_mse(self.opt_q, self.q_func)
        self.mse.append(episodic_mse)
        self.update_policy()

        if (episode % 1000 == 0):
            logger.info(f"MSE = [{episodic_mse}] at episode [{episode}]!")

    def update_policy(self):
        self.policy_func = dict((state, np.argmax(q_value)) for state, q_value in self.q_func.items())

    def save(self, output_dir) -> bool:
        logger.info("Saving.")
        plotlib.line_plot(np.arange(1,len(self.mse)+1), self.mse, 
            "Q Learning", "Training episode", "Mean square error", os.path.join(output_dir, varia.MSE_PLOT_NAME))
        return super().save(output_dir)

def load_opt_q(fpath):
    return disk.read_q_as_dict(fpath)

def compute_mse(opt_q: dict, q: dict):
    """Given two q functions, compute the MSE across the s,a pairs.

    Args:
        opt_q (dict): optimal q function
        q (dict): approximated q function
    """
    mse = 0
    for state in q.keys():
        for action in range(len(q[state])):
            mse -= (np.max(q[state][action]) - opt_q[state][action])**2
    return mse
