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

CURSOR_UP = '\033[1A'
CLEAR = '\x1b[2K'
CLEAR_LINE = CURSOR_UP + CLEAR


def clearTerminal() -> None:
    """
    Clears the terminal screen.
    
    This function works on both Windows and Unix-like systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(separator: str = "-", length: int = 80) -> None:
    """
    Prints a separator line to the console.
    
    Args:
        separator (str): The character to use for the separator. Default is '-'.
        length (int): The length of the separator line. Default is 80 characters.
    """
    print(separator * length)
    
def getTerminalWidth() -> int:
    """
    Get the width of the terminal window in characters.
    
    Returns:
        int: The width of the terminal window. Defaults to 80 if unable to determine.
    """
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Default width if terminal size cannot be determined
    
def maximizeTerminal() -> None:
    """
    Maximizes the terminal window.
    
    Note: This function may not work on all systems or terminal emulators.
    """
    if os.name == 'nt':  # Windows
        os.system('mode con: cols=700 lines=300')
    else:
        # For Unix-like systems, we can try to use 'resize' command
        os.system('printf "\e[8;50;200t"')  # Resize to 50 rows and 200 columns

def printWithoutLineWrap (prefixText: str, textToAdd: str):  
    """
    Returns as much of textToAdd without wrapping the terminal to the next line.
    
    Args:
        prefixText (str): The text that must be displayed on the current line first.
        
    Returns:
        str: The existing text padded with spaces to fill the terminal width.
    """
    terminalWidth = getTerminalWidth()
    # Calculate visible length accounting for tab characters (typically 8 spaces)
    visibleLength = sum(8 if c == '\t' else 1 for c in prefixText)
    remainingLength = terminalWidth - visibleLength
    
    printText = ""
    if remainingLength <= 0:
        #put the extra text on a new line
        printText = prefixText + "\n\t" + textToAdd[:terminalWidth - 8]
    else:
        if len(textToAdd) >= remainingLength:
            printText = prefixText + ' ' + textToAdd[:remainingLength - 3] + '...'
        else:
            printText = prefixText + ' ' + textToAdd[:remainingLength]
    
    print(printText)