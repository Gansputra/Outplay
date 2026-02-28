import os
import sys

def clear_screen():
    """
    Clears the terminal screen based on the operating system.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def safe_input(prompt="> "):
    """
    Safely handles user input, catching KeyboardInterrupt and EOFError.
    
    Args:
        prompt (str): The text to display before input.
        
    Returns:
        str: The user's input, or None if the input was interrupted.
    """
    try:
        user_input = input(prompt).strip()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\n[!] Input cancelled.")
        return None

def print_header(text):
    """Prints a styled header."""
    width = 40
    print("=" * width)
    print(f"{text.center(width)}")
    print("=" * width)
