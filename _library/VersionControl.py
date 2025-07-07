import os 
from . import Preferences as myPreferences
from . import Terminal as myTerminal

# for now assume that git is the version control of choice 
vaultIsVersionControlled = os.path.isdir(os.path.join(myPreferences.root_pkv(), '.git'))
useVersionControl = myPreferences.use_versioncontrol()

if not useVersionControl and not vaultIsVersionControlled:
    print (f"""{myPreferences.myTerminal.WARNING}Version control is not enabled in your preferences but your vault root has been initialized for Git.
           Consider enabling version control in your preferences{myPreferences.myTerminal.RESET}""")
elif useVersionControl and not vaultIsVersionControlled:
    print (f"""{myPreferences.myTerminal.WARNING}Version control is enabled in your preferences but your vault root has NOT been initialized for Git.
           Consider initializing your vault root for Git. {myPreferences.myTerminal.RESET}""")

if not vaultIsVersionControlled and useVersionControl:
    #even if the preferences say to use version control, turn it off if the vault is not set up for it
    useVersionControl = False

if os.path.exists(os.path.join(myPreferences.root_pkv(),".gitignore")) is False:
    #create a .gitignore file if it does not exist
    with open(os.path.join(myPreferences.root_pkv(), ".gitignore"), "w") as gitignore_file:
        gitignore_file.write("# Ignore PKV specific files\n")
        gitignore_file.write("#\n")
        gitignore_file.write("# dictionary of all notes in vault\n")
        gitignore_file.write("AllNotes.json\n")
        gitignore_file.write("# Scripted Search log for debugging\n")
        gitignore_file.write("search.log\n")
        gitignore_file.write("# any hidden files including Search Results, diagram exports, etc\n")
        gitignore_file.write(".*\n")
        

def startVersionControlMessage() -> None:
    """
    Prints a message indicating that version control is starting.
    
    This function is used to signal the beginning of a version control operation.
    """
    print(f"\n\t{myTerminal.CYAN}***Starting version control operation...")

def stopVersionControlMessage() -> None:
    """
    Prints a message indicating that version control has ended.
    
    This function is used to signal the end of a version control operation.
    """
    print(f"\t***Version control operation completed.{myTerminal.RESET}\n")

def add_all() -> None:
    """
    Adds all changes in the current repository to the staging area.
    
    This function uses the `git add .` command to stage all changes.
    """

    if useVersionControl:       
        startVersionControlMessage()
        cmd = f"""git -C "{myPreferences.root_pkv()}" add . """
        os.system(cmd)
        stopVersionControlMessage()

def add_and_commit(fileAndPath, message = "Updated notes") -> None:
    """
    Adds specified files to the staging area and commits them with a message.
    
    Args:
        filesAsString (str): A string of file paths to add.
        message (str): The commit message.
    """
    
    if useVersionControl:       
        startVersionControlMessage()
        cmd = f"""git -C "{myPreferences.root_pkv()}" add "{fileAndPath}" """
        os.system(cmd)
        cmd = f"""git -C "{myPreferences.root_pkv()}" commit "{fileAndPath}" -m "{message}" """
        os.system(cmd)
        stopVersionControlMessage()

def add_and_commit_all(message = "add and commit all vault changes") -> None:
    """
    Adds specified files to the staging area and commits them with a message.
    
    Args:
        filesAsString (str): A string of file paths to add.
        message (str): The commit message.
    """
    
    if useVersionControl:       
        startVersionControlMessage()
        cmd = f"""git -C "{myPreferences.root_pkv()}" add . """
        os.system(cmd)
        cmd = f"""git -C "{myPreferences.root_pkv()}" commit -m "{message}" """
        os.system(cmd)
        stopVersionControlMessage()

def commit_existingChange(fileAndPath, message = "Updated notes") -> None:
    """
    Adds specified files to the staging area and commits them with a message.
    
    Args:
        filesAsString (str): A string of file paths to add.
        message (str): The commit message.
    """
    
    if useVersionControl:       
        startVersionControlMessage()
        cmd = f"""git -C "{myPreferences.root_pkv()}" commit "{fileAndPath}" -m "{message}" """
        os.system(cmd)
        stopVersionControlMessage()

def log() -> None:
    """
    Displays the commit log of the repository.
    
    This function uses the `git log` command to show the commit history.
    """
    
    if useVersionControl:       
        startVersionControlMessage()
        cmd = f"""git -C "{myPreferences.root_pkv()}" log --oneline --graph --decorate --all"""
        os.system(cmd)
        stopVersionControlMessage()