from src.engine import GameEngine

def main():
    """Entry point for the RPG game."""
    try:
        game = GameEngine()
        game.start()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        print("System shutdown.")

if __name__ == "__main__":
    main()
