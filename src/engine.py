from .utils import clear_screen, safe_input, print_header, CLR, print_logo, box_text, print_subheader
from .player import Player
from .enemy import Enemy
from .combat import CombatManager
import json
import os

class GameEngine:
    def __init__(self):
        self.is_running = True
        self.player = Player()
        self.player_history = []
        self.fight_count = 0
        self.state = "MENU" # MENU, PLAYING, EXIT
        self.difficulty = "MEDIUM"

    def start(self):
        """Starts the main game loop."""
        while self.is_running:
            if self.state == "MENU":
                self._handle_menu()
            elif self.state == "PLAYING":
                self._handle_gameplay()
            elif self.state == "EXIT":
                self._shutdown()

    def _handle_menu(self):
        clear_screen()
        print_logo()
        
        menu_options = [
            "1. Start Chronicle",
            "2. View Hall of Fame",
            "3. Quit"
        ]
        box_text(menu_options, width=40, title="MAIN MENU", color="CYAN")
        
        choice = safe_input("\nChoose an option: ")
        
        if choice == "1":
            name = safe_input("\nEnter your name, Traveler: ")
            if name:
                self.player.name = name
            
            # Difficulty Selection
            clear_screen()
            diff_options = [
                "1. EASY   (Classic Journey)",
                "2. MEDIUM (The Standard)",
                "3. HARD   (Cruel Reality)"
            ]
            box_text(diff_options, width=40, title="SELECT DIFFICULTY", color="YELLOW")
            diff_choice = safe_input("\nHow difficult is your path? ")
            
            if diff_choice == "1": self.difficulty = "EASY"
            elif diff_choice == "3": self.difficulty = "HARD"
            else: self.difficulty = "MEDIUM"
                
            self.state = "PLAYING"
        elif choice == "2":
            clear_screen()
            print_header("HALL OF FAME")
            print("Feature coming soon! (Wait for next upgrade, King!)")
            input("\nPress Enter to return...")
        elif choice == "3" or choice is None:
            self.state = "EXIT"
        else:
            print(f"{CLR['RED']}Invalid choice.{CLR['RESET']}")
            input("Press Enter to try again.")

    def _handle_gameplay(self):
        floor = 1
        tower_active = True
        
        while tower_active and self.player.hp > 0:
            clear_screen()
            print_header(f"FLOOR {floor}: THE ASCENSION", color="MAGENTA")
            
            # 1. Scaling Difficulty
            difficulty_mult = 1.0 + (floor - 1) * 0.15 # 15% stronger per floor
            
            # 2. Dynamic Enemy Spawning
            enemy_name = "Shadow Stalker" if floor % 5 != 0 else "TOWER GUARDIAN"
            aggro = min(10, 4 + floor) if self.difficulty == "HARD" else min(10, 2 + floor // 2)
            
            enemy = Enemy(
                enemy_name, 
                aggression=aggro, 
                patience=min(10, 2 + floor // 3), 
                adapt_rate=min(10, 2 + floor) if self.difficulty != "EASY" else 2
            )
            enemy.max_hp = int(enemy.max_hp * difficulty_mult)
            enemy.hp = enemy.max_hp
            
            if floor % 5 == 0:
                print(f"\n{CLR['RED']}{CLR['BOLD']}!!! WARNING: BOSS FLOOR !!!{CLR['RESET']}")
                print(f"You feel an overwhelming presence at floor {floor}...")
            else:
                print(f"\n{CLR['CYAN']}Floor {floor}: A new challenger awaits...{CLR['RESET']}")
            
            input("\nPress Enter to engage...")
            
            # 3. Combat
            combat = CombatManager(self.player, enemy, self.player_history)
            result = combat.start_encounter()
            
            if result == "EXIT":
                self.state = "EXIT"
                return
            
            self._process_combat_result(result)
            
            if self.player.hp <= 0:
                tower_active = False
                print_header("TOWER OVERRUN", color="RED")
                print(f"\nYou fell at Floor {floor}. Your legend ends here.")
                input("\nPress Enter to witness your chronicle...")
                self.state = "EXIT"
                return

            self.fight_count = floor # Track progress
            floor += 1
            
            # 4. Rest Stops (Every 2 floors)
            if tower_active and floor % 2 == 0:
                self._handle_rest_stop()

    def _handle_rest_stop(self):
        clear_screen()
        print_header("TOWER SANCTUARY", color="GREEN")
        
        options = [
            "1. Meditate (-Focus Exhaustion)",
            "2. Bandage  (+20 HP)",
            "3. Continue (Higher Resolve)"
        ]
        box_text(options, width=45, title="REST STOP", color="GREEN")
        
        choice = safe_input("\nChoose your respite: ")
        if choice == "1":
            self.player.recover(focus_amount=5)
        elif choice == "2":
            self.player.recover(hp_amount=20)
        else:
            print("\nYou push forward without rest. Risk is the price of glory.")
            
        input("\nPress Enter to climb higher...")

    def _process_combat_result(self, result):
        clear_screen()
        print_header("CHRONICLE UPDATE", color="YELLOW")
        
        lines = []
        if result == "VICTORY":
            lines.append("You emerged victorious. Your resolve strengthens.")
            # Rewards scale slightly
            self.player.apply_decision_effect({"focus": 1, "insight": 2}, silent=True)
        elif result == "PHYSICAL_TRAUMA":
            lines.append("You were beaten down brutally.")
            self.player.apply_permanent_penalty("max_hp", 5, "Shattered Ribs")
        elif result == "MENTAL_COLLAPSE":
            lines.append("Your mind gave way before your body did.")
            self.player.apply_permanent_penalty("max_focus", 2, "Nightmares")
        elif result == "ESCAPED_COWARDLY":
            lines.append("You fled in terror. You lost ground.")
            self.player.apply_decision_effect({"insight": -3}, silent=True)
        else:
            lines.append(f"Encounter ended with status: {result}")
            
        box_text(lines, width=60, title="AFTERMATH", color="MAGENTA")
        input("\nPress Enter to continue...")

    def _get_philosophical_ending(self, dominant, scars):
        """Returns a philosophical message based on playstyle."""
        
        if dominant in ["ATTACK", "PRESSURE"]:
            title = f"{CLR['RED']}The Path of the Conqueror{CLR['RESET']}"
            msg = "You chose force as your ultimate answer. In the end, the world is shaped by those who strike first, but one must wonder if a heart of iron can still feel the sun's warmth."
        elif dominant == "OBSERVE":
            title = f"{CLR['CYAN']}The Path of the Watcher{CLR['RESET']}"
            msg = "Knowledge was your shield. You saw the world for what it was, but in watching the storm, you may have forgotten how to dance in the rain."
        elif dominant == "BAIT":
            title = f"{CLR['MAGENTA']}The Path of the Deceiver{CLR['RESET']}"
            msg = "You played with fire and expected others to burn. Strategy is a sharp blade, but it requires a steady hand not to cut oneself."
        else:
            title = f"{CLR['GREEN']}The Path of the Wanderer{CLR['RESET']}"
            msg = "You balanced on the edge of many paths. Harmony is not the absence of conflict, but the ability to remain yourself amidst the chaos."

        if len(scars) >= 2:
            msg += f"\n{CLR['YELLOW']}Your burdens weigh heavy, but it is the scars that prove you lived.{CLR['RESET']}"
            
        return title, msg

    def _shutdown(self):
        clear_screen()
        print_header("FINAL CHRONICLE", color="MAGENTA")
        
        dominant = "None"
        if self.player_history:
            dominant = max(set(self.player_history), key=self.player_history.count)
            
        summary = {
            "player_name": self.player.name,
            "fights": self.fight_count,
            "dominant_decision": dominant,
            "final_hp": f"{self.player.hp}/{self.player.max_hp}",
            "scars": self.player.permanent_scars,
            "ending_type": "MANUAL_EXIT" if self.player.hp > 0 else "TERMINATED"
        }
        
        # Display Ending Text
        title, philosophy = self._get_philosophical_ending(dominant, summary['scars'])
        print(f"\n{title}")
        print(f"{CLR['BOLD']}{philosophy}{CLR['RESET']}\n")
        
        print_subheader("Session Statistics")
        print(f"Total Fights      : {CLR['YELLOW']}{summary['fights']}{CLR['RESET']}")
        print(f"Dominant Tactic   : {CLR['CYAN']}{summary['dominant_decision']}{CLR['RESET']}")
        print(f"Final Condition   : {CLR['GREEN']}{summary['final_hp']} HP{CLR['RESET']}")
        if summary['scars']:
            print(f"Permanent Scars   : {CLR['MAGENTA']}{', '.join(summary['scars'])}{CLR['RESET']}")
        print(f"Ending Status     : {CLR['BOLD']}{summary['ending_type']}{CLR['RESET']}")
        
        # Save to JSON
        try:
            history_file = "run_history.json"
            history_data = []
            if os.path.exists(history_file):
                with open(history_file, "r") as f:
                    history_data = json.load(f)
            
            history_data.append(summary)
            with open(history_file, "w") as f:
                json.dump(history_data, f, indent=4)
            print(f"\n{CLR['BLUE']}[System] Chronicle updated in {history_file}{CLR['RESET']}")
        except Exception as e:
            print(f"\n{CLR['RED']}[Warning] Could not record history: {e}{CLR['RESET']}")

        print(f"\n{CLR['CYAN']}Safe travels, {self.player.name}.{CLR['RESET']}")
        self.is_running = False
