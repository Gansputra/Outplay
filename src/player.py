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
        self.permanent_scars = []

    def display_status(self):
        """Displays the player's current status and statistics."""
        print_header(f"STATUS: {self.name}")
        print(f"HP      : {self.hp}/{self.max_hp}")
        print(f"Focus   : {self.focus}/{self.max_focus}")
        print(f"Insight : {self.insight}")
        print(f"Risk    : {self.risk}%")
        if self.permanent_scars:
            print(f"Scars   : {', '.join(self.permanent_scars)}")
        print("-" * 40)

    def apply_permanent_penalty(self, stat, value, reason):
        """Reduces max stats permanently."""
        if hasattr(self, stat):
            current_val = getattr(self, stat)
            setattr(self, stat, max(1, current_val - value))
            
            # If we reduce max_hp or max_focus, we should also clamp current values
            if stat == "max_hp":
                self.hp = min(self.hp, self.max_hp)
            elif stat == "max_focus":
                self.focus = min(self.focus, self.max_focus)
                
            self.permanent_scars.append(reason)
            print(f"\n[!!!] PERMANENT PENALTY: {stat.upper()} decreased by {value} due to {reason}.")

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
