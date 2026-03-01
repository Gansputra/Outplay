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
        last_log = ["The air grows heavy as you face your opponent...", "Waiting for your move."]
        
        while combat_active and self.player.hp > 0 and self.enemy.hp > 0:
            clear_screen()
            from .utils import get_progress_bar, get_player_ascii, get_enemy_ascii, box_text
            
            # --- SYMMETRIC UI HEADER ---
            print_header("CHRONICLE OF CONFLICT", color="MAGENTA")
            
            # ASCII Portraits
            p_ascii = get_player_ascii()
            e_ascii = get_enemy_ascii(self.enemy.name)
            
            # Center padding
            vs_logo = "      VS      "
            
            print(f"\n      {CLR['GREEN']}{self.player.name.center(15)}{CLR['RESET']} {vs_logo} {CLR['RED']}{self.enemy.name.center(15)}{CLR['RESET']}")
            for i in range(len(p_ascii)):
                p_line = p_ascii[i].center(22)
                e_line = e_ascii[i].center(22)
                print(f"{p_line}{' ' * 10}{e_line}")
                
            # Status Bars
            p_hp_bar = get_progress_bar(self.player.hp, self.player.max_hp, length=15, color_mapping="HP")
            e_hp_bar = get_progress_bar(self.enemy.hp, self.enemy.max_hp, length=15, color_mapping="HP")
            p_focus_bar = get_progress_bar(self.player.focus, self.player.max_focus, length=15, color_mapping="FOCUS")
            
            print(f"\n HP: {p_hp_bar}      HP: {e_hp_bar}")
            print(f" FC: {p_focus_bar}      STAT: {CLR['YELLOW']}Aggression {self.enemy.aggression}{CLR['RESET']}")
            
            # Memory Context
            print(f"\n{CLR['BOLD']}History:{CLR['RESET']} {CLR['CYAN']}{self.memory.get_history_summary()}{CLR['RESET']}")
            
            # --- COMBAT LOG ---
            box_text(last_log, width=60, title="COMBAT LOG", color="YELLOW")
            
            # --- ACTIONS ---
            print("\n1. Observe  (Insight↑ Risk↓)   2. Pressure (Stress Enemy)")
            print("3. Bait     (Risk↑↑ Counter)   4. Attack   (Focus Cost)")
            
            choice = safe_input("\nChoose your tactic: ")
            
            if choice == "1":
                last_log = self._execute_turn("OBSERVE")
            elif choice == "2":
                last_log = self._execute_turn("PRESSURE")
            elif choice == "3":
                last_log = self._execute_turn("BAIT")
            elif choice == "4":
                last_log = self._execute_turn("ATTACK")
            elif choice is None:
                return "EXIT"
            else:
                last_log = ["Invalid tactic. They are closing in...", "Try again."]
                input()

            if self.enemy.hp <= 0:
                print(f"\n{CLR['BOLD']}[!] {self.enemy.name} has been suppressed.{CLR['RESET']}")
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
        turn_log = []
        
        # Calculate modifiers
        mem_modifier = self.memory.get_effectiveness_modifier(player_action)
        enemy_modifier = self.enemy.get_adaptation_penalty(player_action, self.player_history)
        
        # Combined effectiveness
        modifier = min(mem_modifier, enemy_modifier)
        
        # Apply Fatigue System
        fatigue_effects = self.memory.get_fatigue_triggers(player_action)
        if fatigue_effects:
            if "focus" in fatigue_effects:
                turn_log.append(f"{CLR['RED']}Mental Strain: -{abs(fatigue_effects['focus'])} Focus{CLR['RESET']}")
            if "risk" in fatigue_effects:
                turn_log.append(f"{CLR['YELLOW']}Over-extension: +{fatigue_effects['risk']}% Risk{CLR['RESET']}")
            self.player.apply_decision_effect(fatigue_effects, silent=True)
        
        self.player_history.append(player_action)
        self.memory.record_decision(player_action)
        
        enemy_action = self.enemy.choose_response(self.player_history)
        
        if modifier < 1.0:
            if enemy_modifier < mem_modifier:
                turn_log.append(f"{CLR['MAGENTA']}{self.enemy.name} has adapted to your style!{CLR['RESET']}")
            else:
                turn_log.append(f"{CLR['BLUE']}You are losing concentration...{CLR['RESET']}")
            
        turn_log.append(f"You : {player_action}")
        turn_log.append(f"{self.enemy.name} : {enemy_action}")

        # RESOLUTION LOGIC
        if player_action == "OBSERVE":
            insight_gain = int(2 * modifier)
            self.player.apply_decision_effect({"insight": insight_gain, "risk": -5}, silent=True)
            
            if enemy_action == "ATTACK":
                risk_multiplier = 1.0 + (self.player.risk / 100.0)
                dmg = int(5 * risk_multiplier)
                self.player.apply_decision_effect({"hp": -dmg, "insight": 1}, silent=True)
                turn_log.append(f"{CLR['RED']}Result: Caught off-guard! Take {dmg} dmg.{CLR['RESET']}")
            else:
                turn_log.append(f"{CLR['GREEN']}Result: Insights gained (+{insight_gain}).{CLR['RESET']}")

        elif player_action == "PRESSURE":
            dmg = int(random.randint(3, 7) * modifier)
            self.enemy.hp -= dmg
            self.player.apply_decision_effect({"risk": 2, "focus": -1}, silent=True)
            if enemy_action == "DEFEND":
                turn_log.append(f"Result: Forced their guard! ({dmg} dmg)")
            else:
                turn_log.append(f"Result: Keeping them stressed ({dmg} dmg)")

        elif player_action == "BAIT":
            self.player.apply_decision_effect({"risk": 15}, silent=True)
            if enemy_action == "ATTACK":
                counter_dmg = int((15 + (self.player.insight // 2)) * modifier)
                self.enemy.hp -= counter_dmg
                self.player.apply_decision_effect({"risk": -10, "focus": 2}, silent=True)
                turn_log.append(f"{CLR['BOLD']}Result: PERFECT COUNTER! ({counter_dmg} dmg){CLR['RESET']}")
            else:
                turn_log.append(f"Result: They didn't bite. Risk increased.")

        elif player_action == "ATTACK":
            if self.player.focus >= 2:
                base_dmg = int((8 + (self.player.insight // 3)) * modifier)
                if enemy_action == "DEFEND":
                    base_dmg //= 2
                    turn_log.append(f"Result: Attack partially blocked.")
                
                self.enemy.hp -= base_dmg
                self.player.apply_decision_effect({"focus": -2, "risk": 5}, silent=True)
                turn_log.append(f"Result: Struck for {base_dmg} dmg.")
            else:
                turn_log.append(f"{CLR['YELLOW']}Result: Too exhausted to attack.{CLR['RESET']}")
                self.player.apply_decision_effect({"focus": 1}, silent=True)

        return turn_log
