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
            print(f"\nEncounter Result: {result}")
            input("Press Enter to return to menu...")
            self.state = "MENU"

    def _shutdown(self):
        print("\nThanks for playing! Goodbye.")
        self.is_running = False
