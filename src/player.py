from .utils import print_header

class Player:
    def __init__(self, name="Traveler", hp=100, insight=10, focus=10, risk=0):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.insight = insight
        self.focus = focus
        self.max_focus = focus
        self.risk = risk

    def display_status(self):
        """Displays the player's current status and statistics."""
        print_header(f"STATUS: {self.name}")
        print(f"HP      : {self.hp}/{self.max_hp}")
        print(f"Focus   : {self.focus}/{self.max_focus}")
        print(f"Insight : {self.insight}")
        print(f"Risk    : {self.risk}%")
        print("-" * 40)

    def apply_decision_effect(self, effects: dict):
        """
        Applies changes to the player's stats based on a decision.
        Example effects: {"hp": -10, "insight": 5, "risk": 2}
        """
        for stat, value in effects.items():
            if hasattr(self, stat):
                setattr(self, stat, getattr(self, stat) + value)
                
                # Boundary checks
                if stat == "hp":
                    self.hp = max(0, min(self.hp, self.max_hp))
                elif stat == "focus":
                    self.focus = max(0, min(self.focus, self.max_focus))
                elif stat == "risk":
                    self.risk = max(0, self.risk)
                
                # Feedback to user
                change = f"+{value}" if value > 0 else f"{value}"
                print(f"[Stat Update] {stat.upper()}: {change}")
            else:
                print(f"[Warning] Unknown stat: {stat}")
