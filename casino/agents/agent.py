from abc import ABC, abstractmethod
import enum
from collections import defaultdict
import logging
import os
import numpy as np

from casino.io import disk
from casino.util.env import varia

from casino.environments.env import Env
from casino.plotting import plotlib
"""Module file for anything related to the abstract concept of an agent
"""
logger = logging.getLogger(__name__)
class AbstractAgent(ABC):
    def __init__(self, n_actions: int, name: str, policy_code: int, eps_constant: int) -> None:
        """Constructor

        Args:
            game_id (int): the id of the game the agent will be interacting with
            n_actions (int): the size of the action space for the game
            name (str): the name of the agent implementation
            policy_code (int): a code represneting the type of policy function
        """
        super().__init__()
        self.n_actions = n_actions
        self.name = name
        self.n_state_visits = {} # counter for tracking the number of visits to a state
        self.n_state_action_visits = {} # counter for tracking the number of times an action has been selected for a state
        self.eps_constant = eps_constant
        self.policy_type = Policies(policy_code)
        self.policy_func = {}

        self.q_func = defaultdict(lambda: np.zeros(self.n_actions)) # Q function
        self.policy_func = {} # optimal policy func

        self.cumulative_episodic_rewards = []

    def load(self, policy_func, q_func):
        self.policy_func = policy_func
        self.q_func = q_func

    @abstractmethod
    def update_policy(self):
        """Override this method with logic for performing a training update using the states, actions and rewards
        """

    @abstractmethod
    def train_episode(self, env: Env, episode: int):
        """Override this method with logic for performing a single training episode
        """

    
    @abstractmethod
    def save(self, output_dir) -> bool:
        """Override this method with logic for saving the data accumulated during training specific to the agent

        Args:
            output_dir: the output directory to which training data will be saved

        Returns:
            bool: true if the save was succussful
        """

    def get_optimal_action(self, state: list) -> int:
        return np.amax(self.q_func[state])

    def get_policy(self, state: int):
        """Get the policy for the agent, and update the visit counters

        Args:
            state (int): the state for which the policy will use to select the action
        """
        action = self.policy(state)
        return action

    def policy(self, state: int) -> int:
        """Override this method with logic for calculating the agent's policy

        Args:
            state (int): the state for inferring the policy on
        """
        action = None
        if self.policy_type == Policies.EPSILON_GREEDY:
            action = self.get_epsilon_greedy_policy(state)
        
        return action

    def get_epsilon_greedy_policy(self, state):
        probabilities = np.zeros(self.n_actions)
        optimal_action_idx = np.argmax(self.q_func[state])
        alt_action = np.random.choice(np.setdiff1d(np.arange(self.n_actions), optimal_action_idx)) 
        epsilon = self.get_epsilon(state)
        probabilities[optimal_action_idx] = 1 - epsilon + (epsilon/self.n_actions)
        probabilities[alt_action] = epsilon / self.n_actions

        action = np.random.choice(np.arange(self.n_actions), p = probabilities)
        return action

    def get_epsilon(self, state):
        return self.eps_constant / (self.eps_constant + self.get_state_visit_count(state))
    
    def get_alpha(self, state, action):
        """Return the time variant alpha 'step size' parameter, based on the number of times the given action has been chosen
        for the state

        Args:
            state (any): the state
            action (any): the action

        Returns:
            float: the alpha value
        """
        return 1/self.get_state_action_visit_count(state, action)

    def get_state_visit_count(self, state):
        if state not in self.n_state_visits:
            self.n_state_visits[state] = 1
        else:
            self.n_state_visits[state] += 1
        
        return self.n_state_visits[state]
    
    def get_state_action_visit_count(self, state, action):
        if (state, action) not in self.n_state_action_visits:
            self.n_state_action_visits[(state, action)] = 1
        else:
            self.n_state_action_visits[(state, action)] += 1
        
        return self.n_state_action_visits[(state, action)]

    def save_training_data(self, output_dir, cumulative_rewards):
        logger.info("Saving training data.")
        self.save(output_dir)
        disk.write_dict_as_json(os.path.join(output_dir, varia.Q_FNAME), dict(self.q_func), str, list)
        disk.write_dict_as_json(os.path.join(output_dir, varia.POLICY_FNAME), self.policy_func, str, int)
        disk.write_numpy_as_csv(os.path.join(output_dir, varia.CUMULATIVE_EP_REWARD_FNAME), cumulative_rewards, ['Cumulative episodic reward'])

class Agent(enum.Enum):
    """Enum the game mode.. defines the type of agent to use for the game.

    Types:
        HUMAN = a human playable environment
        monte = play using monte carlo trained model
        TD    = play using td learning trained model
    """
    HUMAN = 0,
    MONTE = 1,
    SARSA = 2,
    QLEARN =3

class Policies(enum.Enum):
    EPSILON_GREEDY = 0