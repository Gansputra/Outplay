from .utils import clear_screen, safe_input, print_header
from .player import Player
from .enemy import Enemy

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
        self.player.display_status()
        print_header("Dungeon - Level 1")
        print("\nYou are in a dark room. Not much to see here yet...")
        print("\nType 'back' to return to menu or 'quit' to exit.")
        
        action = safe_input("\nWhat do you do? ")
        if action is None:
            self.state = "EXIT"
            return
            
        action = action.lower()
        if action == "back":
            self.state = "MENU"
        elif action == "quit":
            self.state = "EXIT"
        else:
            print(f"I don't know how to '{action}'. Press Enter to continue.")
            input()

    def _shutdown(self):
        print("\nThanks for playing! Goodbye.")
        self.is_running = False
