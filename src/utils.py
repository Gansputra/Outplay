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

def get_progress_bar(current, max_val, length=20, full_char="█", empty_char="░", color_mapping=None):
    """Returns a colored progress bar string."""
    percent = max(0, min(100, (current / max_val) * 100))
    filled_length = int(length * percent // 100)
    bar = full_char * filled_length + empty_char * (length - filled_length)
    
    color = CLR["WHITE"]
    if color_mapping == "HP":
        if percent > 60: color = CLR["GREEN"]
        elif percent > 30: color = CLR["YELLOW"]
        else: color = CLR["RED"]
    elif color_mapping == "FOCUS":
        color = CLR["BLUE"]
    elif color_mapping == "RISK":
        if percent < 30: color = CLR["GREEN"]
        elif percent < 70: color = CLR["YELLOW"]
        else: color = CLR["RED"]
        
    return f"{color}[{bar}]{CLR['RESET']} {int(percent)}%"

def box_text(lines, width=60, title=None, color="CYAN"):
    """Wraps lines of text in an ASCII box."""
    c = CLR.get(color, CLR["CYAN"])
    reset = CLR["RESET"]
    
    top = f"┌{'─' * (width-2)}┐"
    bottom = f"└{'─' * (width-2)}┘"
    
    if title:
        title_text = f" {title} "
        top = f"┌─{title_text}{'─' * (width - 4 - len(title_text))}┐"
    
    print(f"{c}{top}{reset}")
    for line in lines:
        content = line[:width-4]
        padding = " " * (width - 4 - len(content))
        print(f"{c}│{reset} {content}{padding} {c}│{reset}")
    print(f"{c}{bottom}{reset}")

def print_header(text, color="CYAN"):
    width = 60
    c = CLR.get(color, CLR["CYAN"])
    print(f"\n{c}{'=' * width}")
    print(f"{CLR['BOLD']}{text.center(width)}{CLR['RESET']}")
    print(f"{c}{'=' * width}{CLR['RESET']}")

def print_subheader(text, color="WHITE"):
    c = CLR.get(color, CLR["WHITE"])
    print(f"{c}--- {text} ---{CLR['RESET']}")

def get_player_ascii():
    return [
        "   _O_   ",
        "    |    ",
        "   / \\   "
    ]

def get_enemy_ascii(name):
    # Default for "Stalker" or others
    return [
        "  / V \\  ",
        " /  |  \\ ",
        "  ^---^  "
    ]

def print_logo():
    logo = f"""
{CLR['CYAN']} ██████╗ ██╗   ██╗████████╗██████╗ ██╗      █████╗ ██╗   ██╗
██╔═══██╗██║   ██║╚══██╔══╝██╔══██╗██║     ██╔══██╗╚██╗ ██╔╝
██║   ██║██║   ██║   ██║   ██████╔╝██║     ███████║ ╚████╔╝ 
██║   ██║██║   ██║   ██║   ██╔═══╝ ██║     ██╔══██║  ╚██╔╝  
╚██████╔╝╚██████╔╝   ██║   ██║     ███████╗██║  ██║   ██║   
 ╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝   ╚═╝   {CLR['RESET']}
    """
    print(logo)
