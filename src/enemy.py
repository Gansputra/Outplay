import random
from .utils import print_header

class Enemy:
    def __init__(self, name="Shadow", aggression=5, patience=5, adapt_rate=2):
        """
        Initializes an Enemy with specific behavioral traits.
        
        Args:
            name (str): Name of the enemy.
            aggression (int): Propensity to attack (1-10).
            patience (int): Propensity to wait/defend (1-10).
            adapt_rate (int): How quickly it learns from player patterns (1-10).
        """
        self.name = name
        self.aggression = aggression
        self.patience = patience
        self.adapt_rate = adapt_rate
        self.hp = 50
        self.max_hp = 50

    def choose_response(self, player_history):
        """
        Determines the enemy's next action based on its traits and the player's history.
        
        Args:
            player_history (list): List of previous actions taken by the player.
            
        Returns:
            str: The chosen action ('ATTACK', 'DEFEND', 'WAIT', 'COUNTER').
        """
        # Baseline probability based on aggression and patience
        attack_weight = self.aggression
        defend_weight = self.patience
        wait_weight = 10 - self.aggression
        
        # Simple Adaptation Logic
        if player_history:
            # Check for patterns (e.g., player attacks frequently)
            recent_actions = player_history[-3:]
            attack_count = recent_actions.count('ATTACK')
            
            # If player is aggressive, high adapt_rate increases chance to DEFEND or COUNTER
            if attack_count >= 2:
                defend_weight += self.adapt_rate * 2
            
            # If player is defensive, high aggression increases chance to ATTACK
            defend_count = recent_actions.count('DEFEND')
            if defend_count >= 2:
                attack_weight += self.adapt_rate * 1.5

        # Normalize and choose
        actions = ['ATTACK', 'DEFEND', 'WAIT', 'COUNTER']
        # Rough counter weight based on adaptation
        counter_weight = self.adapt_rate if len(player_history) > 2 else 0
        
        weights = [attack_weight, defend_weight, wait_weight, counter_weight]
        
        chosen_action = random.choices(actions, weights=weights, k=1)[0]
        return chosen_action

    def display_status(self):
        print(f"[{self.name}] HP: {self.hp}/{self.max_hp} | Aggression: {self.aggression}")
