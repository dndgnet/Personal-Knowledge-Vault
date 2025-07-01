import os
# Console color variables   
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
GREY = "\033[90m"

ERROR = RED
SUCCESS = GREEN
WARNING = YELLOW    
INFORMATION = MAGENTA
INPUTPROMPT = WHITE
MUTED = GREY
RESET = "\033[0m"


def clearTerminal() -> None:
    """
    Clears the terminal screen.
    
    This function works on both Windows and Unix-like systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')