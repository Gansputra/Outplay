from .utils import clear_screen, safe_input, print_header
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
            
            print(f"Recent Choices: {self.memory.get_history_summary()}")
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
                combat_active = False
            elif self.player.hp <= 0:
                print("\n[!] You have succumbed to the pressure...")
                input()
                combat_active = False

        return "VICTORY" if self.enemy.hp <= 0 else "DEFEAT"

    def _execute_turn(self, player_action):
        # Calculate modifier based on memory before recording the new choice
        modifier = self.memory.get_effectiveness_modifier(player_action)
        
        self.player_history.append(player_action)
        self.memory.record_decision(player_action)
        
        enemy_action = self.enemy.choose_response(self.player_history)
        
        print_header("TURN RESOLUTION")
        if modifier < 1.0:
            print(f"[!] Warning: Your actions are predictable! Effectiveness: {int(modifier*100)}%")
            
        print(f"You chose to {player_action}.")
        print(f"{self.enemy.name} is preparing to {enemy_action}.\n")

        # RESOLUTION LOGIC
        if player_action == "OBSERVE":
            self.player.apply_decision_effect({"insight": 2, "risk": -5})
            if enemy_action == "ATTACK":
                dmg = 5
                self.player.apply_decision_effect({"hp": -dmg, "insight": 3})
                print(f"-> You caught a glimpse of their style while taking a hit (-{dmg} HP).")
            else:
                print("-> You studied the surroundings undisturbed.")

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
                counter_dmg = 15 + (self.player.insight // 2)
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
