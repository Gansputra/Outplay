from .utils import clear_screen, safe_input, print_header
from .player import Player
from .enemy import Enemy
from .combat import CombatManager

class GameEngine:
    def __init__(self):
        self.is_running = True
        self.player = Player()
        self.player_history = []
        self.state = "MENU" # MENU, PLAYING, EXIT

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
        print_header("OUTPLAY RPG")
        print("\n1. Start Game")
        print("2. Quit")
        
        choice = safe_input("\nChoose an option: ")
        
        if choice == "1":
            self.state = "PLAYING"
        elif choice == "2" or choice is None:
            self.state = "EXIT"
        else:
            print("Invalid choice. Press Enter to try again.")
            input()

    def _handle_gameplay(self):
        clear_screen()
        # For demo purposes, we trigger an encounter when entering gameplay
        print_header("A Shadow Approaches...")
        enemy = Enemy("Stalker", aggression=7, patience=3, adapt_rate=4)
        combat = CombatManager(self.player, enemy, self.player_history)
        
        result = combat.start_encounter()
        
        if result == "EXIT":
            self.state = "EXIT"
        else:
            self._process_combat_result(result)
            input("\nPress Enter to return to menu...")
            self.state = "MENU"

    def _process_combat_result(self, result):
        clear_screen()
        print_header("AFTERMATH")
        
        if result == "VICTORY":
            print("\nYou emerged victorious. Your resolve strengthens.")
            self.player.apply_decision_effect({"focus": 2, "insight": 1})
        
        elif result == "PHYSICAL_TRAUMA":
            print("\nYou were beaten down brutally.")
            self.player.apply_permanent_penalty("max_hp", 5, "Shattered Ribs")
            self.player.hp = 10 # Recover slightly
            
        elif result == "MENTAL_COLLAPSE":
            print("\nYour mind gave way before your body did.")
            self.player.apply_permanent_penalty("max_focus", 2, "Nightmares")
            self.player.focus = 2 # Recover slightly
            
        elif result == "ESCAPED_COWARDLY":
            print("\nYou fled in terror, leaving your pride behind.")
            self.player.apply_decision_effect({"insight": -3})
            self.player.hp = 20
            
        else:
            print(f"\nEncounter ended with status: {result}")
            self.player.hp = 15

    def _shutdown(self):
        print("\nThanks for playing! Goodbye.")
        self.is_running = False
