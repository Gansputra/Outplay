from .utils import clear_screen, safe_input, print_header
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
        from .utils import print_logo, box_text
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
        clear_screen()
        print_header("A SHADOW APPROACHES", color="RED")
        from .utils import CLR
        print(f"\n{CLR['BOLD']}A figure emerges from the gloom...{CLR['RESET']}")
        
        # Adjust Enemy base on difficulty
        if self.difficulty == "EASY":
            enemy = Enemy("Stalker", aggression=4, patience=3, adapt_rate=2)
            enemy.hp = 40
        elif self.difficulty == "HARD":
            enemy = Enemy("Elite Stalker", aggression=9, patience=6, adapt_rate=8)
            enemy.hp = 80
        else: # MEDIUM
            enemy = Enemy("Stalker", aggression=7, patience=3, adapt_rate=4)
            enemy.hp = 50
            
        combat = CombatManager(self.player, enemy, self.player_history)
        
        result = combat.start_encounter()
        self.fight_count += 1
        
        if result == "EXIT":
            self.state = "EXIT"
        else:
            self._process_combat_result(result)
            input("\nPress Enter to return to menu...")
            self.state = "MENU"

    def _process_combat_result(self, result):
        clear_screen()
        from .utils import box_text
        print_header("CHRONICLE UPDATE", color="YELLOW")
        
        lines = []
        if result == "VICTORY":
            lines.append("You emerged victorious. Your resolve strengthens.")
            self.player.apply_decision_effect({"focus": 2, "insight": 1}, silent=True)
        elif result == "PHYSICAL_TRAUMA":
            lines.append("You were beaten down brutally.")
            self.player.apply_permanent_penalty("max_hp", 5, "Shattered Ribs")
            self.player.hp = 10
        elif result == "MENTAL_COLLAPSE":
            lines.append("Your mind gave way before your body did.")
            self.player.apply_permanent_penalty("max_focus", 2, "Nightmares")
            self.player.focus = 2
        elif result == "ESCAPED_COWARDLY":
            lines.append("You fled in terror, leaving your pride behind.")
            self.player.apply_decision_effect({"insight": -3}, silent=True)
            self.player.hp = 20
        else:
            lines.append(f"Encounter ended with status: {result}")
            self.player.hp = 15
            
        box_text(lines, width=60, title="AFTERMATH", color="MAGENTA")

    def _get_philosophical_ending(self, dominant, scars):
        """Returns a philosophical message based on playstyle."""
        from .utils import CLR
        
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
        from .utils import print_subheader, CLR
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
