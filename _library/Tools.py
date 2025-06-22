import datetime 
import os 
import re 

from . import Preferences as myPreferences

_datetime_formats = (
    "%Y-%m-%d %H:%M:%S",  # Full datetime with seconds
    "%Y %m %d %H %M %S",  # Full datetime with seconds spaces
    "%Y-%m-%d %H:%M:%S",  # Full datetime
    "%Y-%m-%d",           # Date only
)

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
    
def datetime_fromString(date_string: str) -> tuple [bool,datetime.datetime]:
    """
    Converts a date string to a datetime object.
    
    Args:
        date_string (str): The date string to convert.
        
    Returns:
        bool: True if conversion is successful, False otherwise.
        datetime.datetime: The converted datetime object.
        
    Raises:
        ValueError: If the date string does not match any of the expected formats.
    """
    
    isDateTime = False
    d = datetime.datetime.now()
    for date_format in _datetime_formats:
        try:
            d = datetime.datetime.strptime(date_string, date_format)
            isDateTime = True
            break
        except ValueError:
            isDateTime = False
            continue
    
    return isDateTime, d

def get_pkv_projects() -> dict:
    """
    Returns a dictionary of projects with their names as keys and their paths as values.
    
    Returns:
        dict: A dictionary containing project names and their corresponding paths.
    """
    projects = {}
    for filename in sorted(os.listdir(myPreferences.root_projects())):
        projectPath = os.path.join(myPreferences.root_projects(), filename)
        if os.path.isdir(projectPath):
            projects[filename] = projectPath
    
    return projects

def get_pkv_attachments() -> dict:
    """
    Returns a dictionary of attachments with their names as keys and their paths as values.
    
    Returns:
        dict: A dictionary containing attachments names and their corresponding paths.
    """
    _attachments = {}
    for filename in sorted(os.listdir(myPreferences.root_attachments())):
        if filename.startswith('.'):
            pass  # Skip hidden files
        
        attachmentPath = os.path.join(myPreferences.root_attachments(), filename)
        if os.path.isfile(attachmentPath):
            _attachments[filename] = attachmentPath
    
    return _attachments

def get_note_tags(noteFileNameAndPath: str) -> tuple [str,set]:
    """
    Extracts tags from a note file.
    
    Args:
        noteFileNameAndPath (str): The path to the note file.
        
    Returns:
        filename: The name of the note file.
        set: A set of unique tags found in the note file.
    """
    
    filename =  noteFileNameAndPath.split("/")[-1]
    
    # Read the template content
    with open(noteFileNameAndPath, 'r', encoding='utf-8') as f:
        note  = f.read()

    allTags = set()
    #get front matter tags
    frontMatterTags_match = re.search(r'tags:\s*(.*)', note)
    frontMatterTagsString = frontMatterTags_match.group(1).strip() if frontMatterTags_match else ""
    frontMatterTagsString = frontMatterTagsString.replace('#', ',')
    for tag in frontMatterTagsString.split(','):
        tag = tag.strip()
        if tag != "":
            allTags.add(tag)  

    #get other tags
    otherTags = re.findall(r'#(\w+)', note)
    for tag in otherTags:
        tag = tag.strip()
        if tag.startswith("#"):
            tag = tag[1:]  # Remove the leading hash if present
        
        allTags.add(tag)

    return filename, allTags

def get_project_tags(projectName: str) -> dict:
    """
    Extracts tags from all notes in a project.
    
    Args:
        projectName (str): The name of the project.
        
    Returns:
        dict: A dictionary where keys are note filenames and values are sets of tags found in those notes.
    """
    
    projectPath = os.path.join(myPreferences.root_projects(), projectName)
    if not os.path.isdir(projectPath):
        return {}
    
    tags = {}
    for filename in sorted(os.listdir(projectPath)):
        noteFilePath = os.path.join(projectPath, filename)
        if os.path.isfile(noteFilePath) and filename.endswith(".md"):
            _, noteTags = get_note_tags(noteFilePath)
            for tag in noteTags:
                existing_tags = tags.get(tag, set())
                existing_tags.add(filename)
                tags[tag] = existing_tags
    
    return tags