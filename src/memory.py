from collections import deque

class MemorySystem:
    def __init__(self, size=5):
        """
        Initializes the memory system with a fixed size.
        """
        self.size = size
        self.decisions = deque(maxlen=size)

    def record_decision(self, action):
        """Records a new player decision."""
        self.decisions.append(action)

    def get_effectiveness_modifier(self, current_action):
        """
        Calculates a modifier based on repetitive or varied behavior.
        
        - Repeating the same action too much reduces effectiveness (Predictability penalty).
        - Variety can sometimes provide bonuses or penalties depending on the action type.
        """
        if not self.decisions:
            return 1.0

        # Predictability Check: How many times has this action been performed recently?
        repetition_count = list(self.decisions).count(current_action)
        
        # Base modifier is 100% (1.0)
        modifier = 1.0
        
        if repetition_count >= 3:
            # Significant penalty for being predictable (3 or more times in last 5 turns)
            modifier -= 0.3
            print(f"[Memory] Predictable! Your {current_action} is becoming expected (-30% effectiveness)")
        elif repetition_count == 2:
            # Minor penalty for repeating
            modifier -= 0.1
            print(f"[Memory] Repetitive. Your {current_action} is losing its edge (-10% effectiveness)")
            
        return max(0.4, modifier) # Never go below 40% effectiveness

    def get_history_summary(self):
        """Returns a string representation of recent decisions."""
        return " -> ".join(self.decisions)
