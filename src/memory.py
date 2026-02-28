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
        """
        if not self.decisions:
            return 1.0

        repetition_count = list(self.decisions).count(current_action)
        modifier = 1.0
        
        if repetition_count >= 4:
            modifier -= 0.5
            print(f"[Memory] STALE tactic! Your {current_action} is completely transparent (-50% effectiveness)")
        elif repetition_count == 3:
            modifier -= 0.3
            print(f"[Memory] Predictable! Your {current_action} is becoming expected (-30% effectiveness)")
        elif repetition_count == 2:
            modifier -= 0.1
            print(f"[Memory] Repetitive. Your {current_action} is losing its edge (-10% effectiveness)")
            
        return max(0.3, modifier)

    def get_fatigue_triggers(self, current_action):
        """
        Calculates stat penalties based on overuse of specific mechanics.
        """
        penalties = {}
        history_list = list(self.decisions)
        
        # Observe Overuse -> Focus drain (Mental exhaustion from over-analysis)
        if current_action == "OBSERVE":
            observe_count = history_list.count("OBSERVE")
            if observe_count >= 2:
                penalties["focus"] = -(observe_count) 
        
        # Attack Overuse -> Risk increase (Physical recklessness/tunnel vision)
        if current_action == "ATTACK":
            attack_count = history_list.count("ATTACK")
            if attack_count >= 2:
                penalties["risk"] = attack_count * 5
                
        return penalties

    def get_history_summary(self):
        """Returns a string representation of recent decisions."""
        return " -> ".join(self.decisions)
