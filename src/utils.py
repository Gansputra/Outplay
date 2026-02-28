import os
import sys

# ANSI Color Codes
CLR = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "RED": "\033[91m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "BLUE": "\033[94m",
    "MAGENTA": "\033[95m",
    "CYAN": "\033[96m",
    "WHITE": "\033[97m",
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def safe_input(prompt="> "):
    try:
        color_prompt = f"{CLR['CYAN']}{prompt}{CLR['RESET']}"
        user_input = input(color_prompt).strip()
        return user_input
    except (KeyboardInterrupt, EOFError):
        print(f"\n{CLR['RED']}[!] Input cancelled.{CLR['RESET']}")
        return None

def print_header(text, color="CYAN"):
    width = 50
    c = CLR.get(color, CLR["CYAN"])
    print(f"\n{c}{'=' * width}")
    print(f"{text.center(width)}")
    print(f"{'=' * width}{CLR['RESET']}")

def print_subheader(text, color="WHITE"):
    c = CLR.get(color, CLR["WHITE"])
    print(f"{c}--- {text} ---{CLR['RESET']}")
