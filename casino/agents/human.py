import argparse
from casino.agents.agent import AbstractAgent
from casino.environments.env import Games
from casino.io import parser
import logging

logger = logging.getLogger(__name__)
class HumanAgent(AbstractAgent):
    def __init__(self) -> None:
        super().__init__(None, "Human", None, None)
    
    def get_action_easy21(self, state) -> list:
        return parser.get_input("Hit[1] or stick[0]!", set([0,1]), "q", int)
    
    def get_policy(self, state):
        if (self.game_id == Games.EASY21):
            return self.get_action_easy21(state)
        
    def update_policy(self, states: list, actions: list, rewards: list):
        return super().update_policy(states, actions, rewards)
    
    def save(self, output_dir) -> bool:
        return super().save(output_dir)