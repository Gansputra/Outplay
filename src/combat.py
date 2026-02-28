from .utils import clear_screen, safe_input, print_header, CLR
from .memory import MemorySystem
import random

class CombatManager:
    def __init__(self, player, enemy, player_history):
        self.player = player
        self.enemy = enemy
        self.player_history = player_history
        self.memory = MemorySystem(size=5)

    def start_encounter(self):
        """Main combat loop."""
        combat_active = True
        
        while combat_active and self.player.hp > 0 and self.enemy.hp > 0:
            clear_screen()
            self.player.display_status()
            self.enemy.display_status()
            
            print(f"{CLR['BOLD']}Recent Choices:{CLR['RESET']} {CLR['CYAN']}{self.memory.get_history_summary()}{CLR['RESET']}")
            print_header("COMBAT ACTIONS")
            print("1. Observe  (Gain Insight, Lower Risk)")
            print("2. Pressure (Stress Enemy, Minor Damage)")
            print("3. Bait     (High Risk, Counter Chance)")
            print("4. Attack   (Direct Damage, Needs Focus)")
            
            choice = safe_input("\nChoose your tactic: ")
            
            if choice == "1":
                self._execute_turn("OBSERVE")
            elif choice == "2":
                self._execute_turn("PRESSURE")
            elif choice == "3":
                self._execute_turn("BAIT")
            elif choice == "4":
                self._execute_turn("ATTACK")
            elif choice is None:
                return "EXIT"
            else:
                print("Invalid tactic. They are closing in...")
                input()

            if self.enemy.hp <= 0:
                print(f"\n[!] {self.enemy.name} has been suppressed.")
                input()
                return "VICTORY"
            elif self.player.hp <= 0:
                return self._determine_defeat_type()

        return "VICTORY" if self.enemy.hp <= 0 else "DEFEAT"

    def _determine_defeat_type(self):
        """Logic to decide the nature of the player's defeat."""
        last_action = self.player_history[-1] if self.player_history else "NONE"
        
        if self.player.risk > 50:
            return "PHYSICAL_TRAUMA"  # Hit 0 HP with high risk
        elif self.player.focus <= 2:
            return "MENTAL_COLLAPSE"  # Hit 0 HP while mentally exhausted
        elif last_action == "OBSERVE":
            return "ESCAPED_COWARDLY" # Lost while being passive
        else:
            return "DEFEAT"

    def _execute_turn(self, player_action):
        # Calculate modifiers
        mem_modifier = self.memory.get_effectiveness_modifier(player_action)
        enemy_modifier = self.enemy.get_adaptation_penalty(player_action, self.player_history)
        
        # Combined effectiveness
        modifier = min(mem_modifier, enemy_modifier)
        
        # Apply Fatigue System
        fatigue_effects = self.memory.get_fatigue_triggers(player_action)
        if fatigue_effects:
            print_header("FATIGUE WARNING")
            if "focus" in fatigue_effects:
                print(f"-> Mental Strain: Over-analyzing is draining your focus! ({fatigue_effects['focus']} Focus)")
            if "risk" in fatigue_effects:
                print(f"-> Over-extension: Aggressive tunneling increases your exposure! (+{fatigue_effects['risk']}% Risk)")
            self.player.apply_decision_effect(fatigue_effects)
        
        self.player_history.append(player_action)
        self.memory.record_decision(player_action)
        
        enemy_action = self.enemy.choose_response(self.player_history)
        
        print_header("TURN RESOLUTION")
        if modifier < 1.0:
            print(f"{CLR['YELLOW']}[!] COMBINED EFFECTIVENESS: {int(modifier*100)}%{CLR['RESET']}")
            if enemy_modifier < mem_modifier:
                print(f"{CLR['MAGENTA']}-> {self.enemy.name} has adapted to your style!{CLR['RESET']}")
            else:
                print(f"{CLR['BLUE']}-> You are losing concentration from repetitive actions.{CLR['RESET']}")
            
        print(f"\nYou chose to {player_action}.")
        print(f"{self.enemy.name} is preparing to {enemy_action}.\n")

        # RESOLUTION LOGIC
        if player_action == "OBSERVE":
            insight_gain = int(2 * modifier)
            self.player.apply_decision_effect({"insight": insight_gain, "risk": -5})
            
            if enemy_action == "ATTACK":
                # High risk leads to more damage received
                risk_multiplier = 1.0 + (self.player.risk / 100.0)
                dmg = int(5 * risk_multiplier)
                self.player.apply_decision_effect({"hp": -dmg, "insight": 1})
                print(f"-> Exposure Penalty: Your high risk ({self.player.risk}%) increased damage taken!")
                print(f"-> You caught a glimpse of their style while taking a hit (-{dmg} HP).")
            else:
                print(f"-> You studied the surroundings undisturbed (+{insight_gain} Insight).")

        elif player_action == "PRESSURE":
            dmg = int(random.randint(3, 7) * modifier)
            self.enemy.hp -= dmg
            self.player.apply_decision_effect({"risk": 2, "focus": -1})
            if enemy_action == "DEFEND":
                print(f"-> Your pressure forced them into an awkward guard! (Direct -{dmg} HP)")
            else:
                print(f"-> You stayed in their face, keeping them stressed (-{dmg} HP).")

        elif player_action == "BAIT":
            self.player.apply_decision_effect({"risk": 15})
            if enemy_action == "ATTACK":
                counter_dmg = int((15 + (self.player.insight // 2)) * modifier)
                self.enemy.hp -= counter_dmg
                self.player.apply_decision_effect({"risk": -10, "focus": 2})
                print(f"-> PERFECT COUNTER! You lured them in and struck back for {counter_dmg} damage!")
            else:
                print("-> You left yourself open, but they didn't bite. Your heart is racing...")

        elif player_action == "ATTACK":
            if self.player.focus >= 2:
                base_dmg = int((8 + (self.player.insight // 3)) * modifier)
                if enemy_action == "DEFEND":
                    base_dmg //= 2
                    print("-> They blocked part of the impact.")
                
                self.enemy.hp -= base_dmg
                self.player.apply_decision_effect({"focus": -2, "risk": 5})
                print(f"-> You landed a strike for {base_dmg} damage.")
            else:
                print("-> You are too exhausted to mount an effective attack!")
                self.player.apply_decision_effect({"focus": 1})

        input("\nPress Enter to continue...")
