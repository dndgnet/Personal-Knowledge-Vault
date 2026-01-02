from . import Preferences as myPreferences
from . import Terminal as myTerminal
import json
import os
import re
import datetime
import csv
from decimal import Decimal

# Import NoteData from Notes module
from .Notes import NoteData, get_Notes_as_list, get_note_tags

_datetime_formats = (
    "%Y-%m-%d %H:%M:%S",    # Full datetime with seconds
    "%Y-%m-%d %H:%M",       # Full datetime without seconds
    "%Y %m %d %H %M %S",    # Full datetime with seconds spaces
    "%Y-%m-%d %H %M",       # Full datetime without seconds and spaces
    "%Y-%m-%d",             # Date only
)

def clearTerminal() -> None:
    """
    Clears the terminal screen.
    
    This function works on both Windows and Unix-like systems.
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def letters_and_numbers_only(input_string: str, maxLength = 400) -> str:
    """
    Removes all characters from the input string except letters and numbers.
    
    Args:
        input_string (str): The string to process.
        
    Returns:
        str: The processed string containing only letters and numbers.
    """
    return re.sub(r'[^A-Za-z0-9_\s]', '', input_string)[:maxLength]
    
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

def now_YYYY_MM_DD_HH_MM_SS() -> str:
    """
    Returns the current date and time in the format 'YYYY-MM-DD HH:MM:SS'.
    
    Returns:
        str: The current date and time as a formatted string.
    """
    return datetime.datetime.now().strftime(myPreferences.datetime_format())

def now_YYYY_MM_DD() -> str:
    """
    Returns the current date in the format 'YYYY-MM-DD'.
    
    Returns:
        str: The current date as a formatted string.
    """
    return datetime.datetime.now().strftime(myPreferences.date_format())

def obsidian_Encode_for_URI(input_string: str) -> str:
    """
    Encodes a string for use in an Obsidian URI.
    
    Args:
        input_string (str): The string to encode.
        
    Returns:
        str: The encoded string.
    """
    encoded_string = input_string.replace(" ", "%20").replace("#", "%23").replace(":", "%3A").replace("/", "%2F").replace("%", "%25")
    return encoded_string

def read_csv_to_dict_list(full_path):
    data = []
    # Try different encodings
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(full_path, mode='r', encoding=encoding) as csvFile:
                reader = csv.DictReader(csvFile)
                for row in reader:
                    data.append(row)
            print(f"Successfully read file using {encoding} encoding")
            return data
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error with {encoding}: {e}")
            continue
    raise ValueError(f"Could not decode file with any of the attempted encodings: {encodings}")

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

#global declaration for caching project configs
dictProjectConfigs = {}
def get_ProjectConfig_as_dict(projectName: str) -> dict:
    """
    Returns the project configuration for a given project name.
    
    Args:
        projectName (str): The name of the project.
    """
    global dictProjectConfigs
    if projectName in dictProjectConfigs:
        return dictProjectConfigs[projectName]
    
    projectPath = os.path.join(myPreferences.root_projects(), projectName)
    
    if not os.path.isdir(projectPath):
        print(f"{myTerminal.ERROR}Project '{projectName}' path does not exist.{myTerminal.RESET}")
        return {}

    if not os.path.exists(os.path.join(projectPath, ".ProjectConfig.json")):
        configBody = {
                    "ProjectFolderName": f"{projectName}",
                    "ProjectName": f"{projectName}",
                    "Programs": [],
                    "Archived": False,
                    "Sync": False,
                    "PublicShareFolder": "",
                    "Needs Weekly Progress Update": False,
                    "Needs Monthly Progress Update": False
                    }
        with open(os.path.join(projectPath, ".ProjectConfig.json"), 'w', encoding='utf-8') as f:
            json.dump(configBody, f, indent=4)
        
    configPath = os.path.join(projectPath, ".ProjectConfig.json")
    if not os.path.isfile(configPath):
        return {}
    
    with open(configPath, 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
            dictProjectConfigs[projectName] = config    
            return config
        except json.JSONDecodeError:
            print(f"{myTerminal.ERROR}Error decoding JSON from {configPath}{myTerminal.RESET}")
            return {}
        
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

def is_NewNote_identifier_unique(noteIdentifier) -> bool:
    """
    Checks if a note identifier is unique across all notes in the PKV.
    
    Args:
        noteIdentifier (str): The identifier to check for uniqueness.
        
    Returns:
        bool: True if the identifier is unique, False otherwise.
    """
    notes = get_Notes_as_list(myPreferences.root_pkv())
    uniqueIds = list(map(lambda note: note.id, notes))
    
    if noteIdentifier in uniqueIds:
        return False
    else: 
        return True

def generate_unique_identifier(timestamp_id, noteType, title) -> str:
    """
    Ensures that the unique identifier is not already used in the target directory.
    
    Args:
        uniqueIdentifier (str): The identifier to check for uniqueness.
        target_dir (str): The directory where notes are stored.
        
    Returns:
        str: A unique identifier, modified if necessary to ensure uniqueness.
    """
    
    titleLettersAndNumbers = letters_and_numbers_only(title, maxLength=200)  # Limit to 200 characters and remove special characters
    uniqueIdentifier = f"{timestamp_id}_{noteType}_{titleLettersAndNumbers}"
    while not is_NewNote_identifier_unique(uniqueIdentifier):
        #Convert timestamp_id back to a datetime object and add a second to it
        print (f"\t{myTerminal.WARNING}Note identifier '{uniqueIdentifier}' already exists. Generating a new one...{myTerminal.RESET}")
        selectedDateTime = datetime.datetime.strptime(timestamp_id, myPreferences.timestamp_id_format())
        timestamp_id = (selectedDateTime + datetime.timedelta(seconds=1)).strftime(myPreferences.timestamp_id_format())
        uniqueIdentifier = f"{timestamp_id}_{noteType}_{titleLettersAndNumbers}"


    return uniqueIdentifier

def generate_tag_from_projectName(projectName: str) -> str:
    """
    Generates a tag from a project name by removing special characters and replacing spaces with underscores.
    
    Args:
        projectName (str): The project name to convert into a tag.
        
    Returns:
        str: The generated tag.
    """
    
    tag = "p_" + letters_and_numbers_only(projectName).replace(" ", "_").replace("&", "and")
    if not tag.startswith("#"):
        tag = f"#{tag}"
    
    return tag

def get_note_frontMatter(noteBody: str) -> str:
    """
    Extracts the front matter from a note body.
    
    Args:
        noteBody (str): The content of the note.
        
    Returns:
        str: The front matter of the note, if present; otherwise, an empty string.
    """
    frontMatterStart = noteBody.find('---')
    frontMatterEnd = noteBody.find('---', frontMatterStart + 3)

    if frontMatterStart != -1 and frontMatterEnd != -1:
        return noteBody[frontMatterStart + 3:frontMatterEnd].strip()
    
    return ""   
    
    # frontMatter_match = re.search(r'^---\n(.*?)\n---', noteBody, re.DOTALL)
    # if frontMatter_match:
    #     return frontMatter_match.group(1).strip()
    
def get_note_body(noteBody: str) -> str:
    """
    Extracts the content of a note, excluding the front matter.
    
    Args:
        noteBody (str): The content of the note.
        
    Returns:
        str: The content of the note, excluding the front matter.
    """
    body = ""
    frontMatter = get_note_frontMatter(noteBody)
    
    body = noteBody.replace(f"---\n{frontMatter}\n---", "").strip()
    
    #Removing this as some notes may not have front matter but still use --- to separate sections
    # if "---" in body:
    #     body = body.split("---", 1)[-1].strip()
    
    return body 

def get_note_backlinks(noteBody: str) -> list:
    """
    Extracts backlinks from a note body.
    
    Args:
        noteBody (str): The content of the note.
        
    Returns:
        list: A list of backlinks found in the note.
    """
    
    backlinks = re.findall(r'\[\[([^\]]+)\]\]', noteBody)
    return [backlink.strip() for backlink in backlinks if backlink.strip()]

def get_note_date_from_frontMatter(frontMatter: str, dateProperty ="start date") -> str:
    """
    Extracts the desired date from the front matter of a note.  If the date is not found
    the created date is returned.  If the note is created with PKV, the created date is always present.
    
    Args:
        frontMatter (str): The front matter of the note.
        
    Returns:
        str: The date of the note, if present; otherwise, an empty string.
    """
    
    date_match = re.search(rf'{dateProperty}:\s*(.*)', frontMatter.replace("*",""))
    if date_match:
        return date_match.group(1).strip()
    
    date_match = re.search(r'created:\s*(.*)', frontMatter)
    if date_match:
        return date_match.group(1).strip()
    
    return ""

def remove_noteHeaders(noteBody: str) -> str:   
    """
    Removes headers from the note body.
    
    Args:
        noteBody (str): The content of the note.
        
    Returns:
        str: The note body with headers removed.
    """
    headers = ["###### ", "##### ", "#### ", "### ","## ","# "]
    
    for header in headers:
        noteBody = noteBody.replace(header, "")
        
    return noteBody.strip()

def get_listValue_from_frontMatter(valuePrefix:str, frontMatter: str) -> list:
    """
    Extracts keywords from the front matter of a note.
    
    Args:
        frontMatter (str): The front matter of the note.
        
    Returns:
        list: A list of keywords found in the front matter.
    """
    
    keywords_match = re.search(r'keywords:[^\n](.*)', frontMatter)
    if keywords_match:
        keywords_string = keywords_match.group(1).strip()
        return [keyword.strip() for keyword in keywords_string.split(',') if keyword.strip()]
    
    return []

def get_stringValue_from_frontMatter(valuePrefix:str,frontMatter: str) -> str:
    """
    Extracts value from the front matter of a note based on a given prefix.
    
    Args:
        frontMatter (str): The front matter of the note.
        
    Returns:
        list: A list of keywords found in the front matter.
    """
    pattern = rf'{valuePrefix}:[^\n](.*)'
    match = re.search(pattern, frontMatter, re.IGNORECASE)
    # match = re.search(pattern, frontMatter)
    if match:
        return match.group(1).strip()
    else:
        return ""

def get_stringValue_from_noteBody(valueLabel:str,noteBody: str) -> str:
    """
    Extracts value from the body of a note based on a given label.  Assumes the 
    label will include a colon (:) followed by the value.  For example, given 
    
    **Budget Amount:** 1000.
    
    the label is "**Budget Amount:**" and the value is "1000".

    Args:
        noteBody (str): The front matter of the note.
        
    Returns:
        str: found value or blank string if not found.
    """
    
    escaped_valueLabel = valueLabel.replace("*",r"\*")
    pattern = rf"""{escaped_valueLabel}[^\n](.*)"""
    match = re.search(pattern, noteBody, re.IGNORECASE)
    
    # match = re.search(pattern, frontMatter)
    if match:
        # most label/value pairs will be in the format of "**Label**: value"
        # or "**Label:** value" so we need to remove the leading colon and asterisks
        value = match.group(1).strip()
        if value.startswith("**:"):
            value = value[3:].strip()
        elif value.startswith("*:"):
            value = value[2:].strip()   
        elif value.startswith(":"):
            value = value[1:].strip()
        elif value.startswith(":**"):
            value = value[3:].strip()
        elif value.startswith(":*"):
            value = value[2:].strip()   

        return value
    else:
        return ""

def decimal_from_string(value: str) -> Decimal:
    """
    Converts a string to a decimal, handling potential float precision issues.
    
    Args:
        value (str): The string to convert.
        
    Returns:
        decimal.Decimal: The converted decimal value.
        
    Raises:
        ValueError: If the string cannot be converted to a decimal.
    """
    returnValue = Decimal("0.00")
    value = value.replace(",","").replace("$","").replace(" ","").replace("%","").strip()  # Remove commas and dollar signs, and strip whitespace
    
    try:
        returnValue = Decimal(value)
    except Exception as e:
        print(f"'{value}' is not a valid decimal value: {e}")
        returnValue = Decimal("0.00")  # Default to zero if conversion fails
    
    return returnValue
        
def get_sectionValue_from_noteBody(valueLabel:str,noteBody: str) -> str:
    """
    Extracts section from the body of a note based on a given label.  Assumes the 
    label will start with #
    and the section ends at the next section header.
    
    Args:
        noteBody (str): The front matter of the note.
        
    Returns:
        str: found value or blank string if not found.
    """
    returnValue = ""
    sectionFound = False
    for line in noteBody.splitlines():
        if line.startswith(f"# {valueLabel}"):
            sectionFound = True
            continue
        
        if sectionFound:
            if "# " in line:
                break # we reached the next section header
            else:
                returnValue += line.strip() + "\n"
             
    return returnValue

def load_MostRecentProjectProgressNote(projectName: str) -> tuple[bool,NoteData]:
     

    allNotes = get_Notes_as_list(myPreferences.root_pkv())
    sortedNotes = sorted(allNotes, key=lambda note: (note.project, note.date), reverse=True)

    if not sortedNotes:
        print(f"{myTerminal.ERROR}No notes found.{myTerminal.RESET}")
        return False, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)
    
    for note in sortedNotes:
        if note.project.upper() == projectName.upper() and "progress".upper() in note.type.upper():
            return True, note  # Return the first matching note
           
    return False, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)

def get_pkv_tags() -> dict:
    """
    Extracts tags from all notes in the PKV.
        
    Returns:
        dict: A dictionary where keys are note filenames and values are sets of tags found in those notes.
    """
    
    pkvPath = os.path.join(myPreferences.root_projects())
    
    tags = {}
    for filename in sorted(os.listdir(pkvPath)):
        noteFilePath = os.path.join(pkvPath, filename)
        if os.path.isfile(noteFilePath) and filename.endswith(".md"):
            _, noteTags = get_note_tags(noteFilePath)
            for tag in noteTags:
                existing_tags = tags.get(tag, set())
                existing_tags.add(filename)
                tags[tag] = existing_tags
    
    return tags
        
def open_note_in_editor(notePath: str):
    """
    Opens a note in the default editor specified in preferences.
    
    Args:
        notePath (str): The path to the note file.
    """
    
    os.system(f'{myPreferences.default_editor()} "{notePath}"')
    if myPreferences.default_editor() != "obsidian":
        os.system(f'{myPreferences.default_editor()} "{notePath}"')
    else:
        # For Obsidian, open the vault and the specific note
        vaultName = myPreferences.root_pkv().split("/")[-1]
        fileName = notePath.split("/")[-1]
        encodedFileName = obsidian_Encode_for_URI(fileName)
        openCmd = f"obsidian://advanced-uri?vault={vaultName}&filepath={encodedFileName}&openmode=true"
        os.system(f'open "{openCmd}"')

def write_text_to_file(filePath: str, textContent: str) -> bool:
    """
    Writes text content to a file.
    
    Args:
        filePath (str): The path to the file.
        textContent (str): The text content to write.
        
    Returns:
        bool: True if the write operation is successful, False otherwise.
    """
    try:
        with open(filePath, 'w', encoding='utf-8') as f:
            f.write(textContent)
        return True
    except Exception as e:
        print(f"{myTerminal.ERROR}Error writing to file '{filePath}': {e}{myTerminal.RESET}")
        return False