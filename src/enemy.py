import random
from .utils import print_header, CLR

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
        """
        # Baseline weights
        weights = {
            'ATTACK': self.aggression,
            'DEFEND': self.patience,
            'WAIT': max(1, 10 - self.aggression),
            'COUNTER': 0
        }
        
        if not player_history:
            return random.choices(list(weights.keys()), weights=list(weights.values()))[0]

        # Analyze player patterns
        recent_5 = player_history[-5:]
        most_frequent = max(set(recent_5), key=recent_5.count)
        freq_count = recent_5.count(most_frequent)

        # Strategic Adaptation based on player's most used tactic
        if most_frequent == "ATTACK":
            weights['DEFEND'] += self.adapt_rate * freq_count
            weights['COUNTER'] += self.adapt_rate * (freq_count - 1)
        elif most_frequent == "PRESSURE":
            weights['ATTACK'] += self.adapt_rate * 1.5
        elif most_frequent == "BAIT":
            weights['WAIT'] += self.adapt_rate * 2
            weights['DEFEND'] += self.adapt_rate
        elif most_frequent == "OBSERVE":
            weights['ATTACK'] += self.adapt_rate * 1.2
            
        # Add slight randomness/unpredictability
        chosen_action = random.choices(list(weights.keys()), weights=list(weights.values()))[0]
        return chosen_action

    def get_adaptation_penalty(self, player_action, player_history):
        """
        Returns a penalty modifier (0.0 to 1.0) based on how much the enemy 
        has adapted to this specific player action.
        """
        if not player_history:
            return 1.0
            
        recent_5 = player_history[-5:]
        occurrence = recent_5.count(player_action)
        
        # Every time the same action is in the history, effectiveness drops
        # based on the enemy's adapt_rate
        penalty = (occurrence * self.adapt_rate) / 20.0 # Max 0.5 penalty at 5/5 frequency and 2 adapt_rate
        
        modifier = max(0.4, 1.0 - penalty)
        
        if modifier < 1.0:
            print(f"[{self.name}] I've seen your {player_action} before. It won't work as well now.")
            
        return modifier

    def display_status(self):
        hp_perc = (self.hp / self.max_hp) * 100
        hp_color = CLR['GREEN'] if hp_perc > 50 else (CLR['YELLOW'] if hp_perc > 25 else CLR['RED'])
        print(f"[{CLR['RED']}{self.name}{CLR['RESET']}] HP: {hp_color}{self.hp}/{self.max_hp}{CLR['RESET']} | Aggression: {CLR['YELLOW']}{self.aggression}{CLR['RESET']}")
