from .utils import print_header, CLR

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
        self.perks = []

    def display_status(self):
        """Displays the player's current status and statistics."""
        print_header(f"STATUS: {self.name}", color="GREEN")
        print(f"{CLR['BOLD']}HP      :{CLR['RESET']} {CLR['GREEN']}{self.hp}/{self.max_hp}{CLR['RESET']}")
        print(f"{CLR['BOLD']}Focus   :{CLR['RESET']} {CLR['BLUE']}{self.focus}/{self.max_focus}{CLR['RESET']}")
        print(f"{CLR['BOLD']}Insight :{CLR['RESET']} {CLR['YELLOW']}{self.insight}{CLR['RESET']}")
        print(f"{CLR['BOLD']}Risk    :{CLR['RESET']} {CLR['RED']}{self.risk}%{CLR['RESET']}")
        if self.permanent_scars:
            print(f"{CLR['MAGENTA']}Scars   : {', '.join(self.permanent_scars)}{CLR['RESET']}")
        print("-" * 50)

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

    def apply_decision_effect(self, effects: dict, silent=False):
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
                if not silent:
                    change = f"+{value}" if value > 0 else f"{value}"
                    print(f"[Stat Update] {stat.upper()}: {change}")
            else:
                if not silent:
                    print(f"[Warning] Unknown stat: {stat}")

    def recover(self, hp_amount=0, focus_amount=0):
        """Restores HP and Focus, capped at max values."""
        if hp_amount > 0:
            self.hp = min(self.max_hp, self.hp + hp_amount)
            print(f"[Rest] Recovered {hp_amount} HP.")
        if focus_amount > 0:
            self.focus = min(self.max_focus, self.focus + focus_amount)
            print(f"[Rest] Recovered {focus_amount} Focus.")
