from . import Preferences as myPreferences
from . import Terminal as myTerminal
from . import VersionControl as myVersionControl
from dataclasses import dataclass
from typing import List
import json
import os
import re
import datetime
from decimal import Decimal
from dataclasses import field  

@dataclass
class NoteData:
    id: str # Unique identifier for the note, typically a timestamp or unique string
    fileName: str
    filePath: str = field(metadata={"description": "os.path.join(notePath, noteFileName) full file name and path"})
    date: str
    osFileDateTime: str
    type: str
    title: str
    project: str
    tags: List[str]
    keywords: List[str]
    retention: str
    author: str
    frontMatter: str 
    noteBody: str
    backLinks: List[str]
    actionItems: List[str]
    archived: bool = False
    hasActionItems: bool = False
    actionItemsWithComments: dict = field(default_factory=dict)

    private: bool = False # indicates that note is only for the vault owner's use
    archivedProject: bool = False # indicates that note belongs to an archived project

    def to_dict(self):
        return {
            "id": self.id,
            "fileName": self.fileName,
            "filePath": self.filePath,
            "date": self.date,
            "osFileDateTime": self.osFileDateTime,
            "type": self.type,
            "title": self.title,
            "project": self.project,
            "tags": self.tags,
            "keywords": self.keywords,
            "retention": self.retention,
            "author": self.author,
            "private": self.private,
            "frontMatter": self.frontMatter,
            "noteBody": self.noteBody,
            "backLinks": self.backLinks,
            "archived": self.archived,
            "hasActionItems": self.hasActionItems,
            "actionItems": self.actionItems,
            "actionItemsWithComments": self.actionItemsWithComments,
            "archivedProject": self.archivedProject
        }
      
    def __str__(self):
        if self.project != "":
            return f"{self.title} ({self.date}) from {self.project}"
        else:
            return f"{self.title} ({self.date})"

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

def print_separator(separator: str = "-", length: int = 80) -> None:
    """
    Prints a separator line to the console.
    
    Args:
        separator (str): The character to use for the separator. Default is '-'.
        length (int): The length of the separator line. Default is 80 characters.
    """
    print(separator * length)

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

def get_Note_from_id(noteId: str) -> NoteData:
    """
    Returns a NoteData object from a note Id.
    
    Args:
        note id (str): The name of the note id.

        """
    
    notes = get_Notes_as_list(myPreferences.root_pkv())
    for note in notes:
        if note.id == noteId:
            return note

    return NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)   


def get_Note_from_fileName(noteFileName: str) -> NoteData:
    """
    Returns a NoteData object from a note file name.
    
    Args:
        noteFileName (str): The name of the note file.

        """
    
    notes = get_Notes_as_list(myPreferences.root_pkv())
    for note in notes:
        if note.fileName == noteFileName:
            return note

    return NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)   
    
def get_Note_from_path(notePath: str, noteFileName: str) -> NoteData:
    
    notePathAndFile = os.path.join(notePath, noteFileName)

    if os.path.exists(notePathAndFile) is False:
        print(f"{myTerminal.ERROR}Note file '{notePathAndFile}' does not exist.{myTerminal.RESET}")
        return NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)

    with open(os.path.join(notePath, noteFileName), 'r', encoding='utf-8') as f:
                    noteContent = f.read()
                    
    frontMatter = get_note_frontMatter(noteContent)
    
    osFileDateTime = datetime.datetime.fromtimestamp(os.path.getmtime(notePathAndFile)).strftime("%Y-%m-%d %H:%M:%S")
    date = get_note_date_from_frontMatter(frontMatter)
    
    if date == "":
        # If no date in front matter, use the file's last modified date
        date = osFileDateTime
    
    uniqueIdentifier = get_stringValue_from_frontMatter("id", frontMatter) 
    if uniqueIdentifier == "":
        uniqueIdentifier = noteFileName.split(".")[0].split("_")[0]  # Use the file name without extension as the unique identifier

    project = get_stringValue_from_frontMatter("project", frontMatter)
    archivedProject = False
    if project != "":
        #todo cache project configs to avoid multiple reads
        projectConfig = get_ProjectConfig_as_dict(project)
        if projectConfig.get("Archived", False) is True:
            archivedProject = True

    type = get_stringValue_from_frontMatter("type", frontMatter)
    if type == "":
        type = "unknown"
    title = get_stringValue_from_frontMatter("title", frontMatter)
    tags = get_tags_from_noteText(noteContent)
    keywords = get_listValue_from_frontMatter("keywords",frontMatter)
    retention = get_stringValue_from_frontMatter("retention", frontMatter)
    author = get_stringValue_from_frontMatter("author", frontMatter)
    private = True if get_stringValue_from_frontMatter("private", frontMatter).lower() in ("true","t","yes","y","positive") else False
    archived = True if get_stringValue_from_frontMatter("archived", frontMatter) == "True" else False
    

    if title == "" or title is None:
        title = uniqueIdentifier
        
    body = get_note_body(noteContent)
    backLinks = get_note_backlinks(noteContent)
    hasActionItems = True if "[ ]" in body else False
    actionItems = [] 
    actionItemsWithComments = {}
    for actionItem in re.findall(r'\[ \](.*)', body):  # Find all action items in the note body
        actionItems.append(actionItem.strip())
       
        # Extract details that follow the action item until the next "- [" or blank line
        action_item_pattern = re.escape(actionItem)
        # Find the position of this action item in the body
        match = re.search(rf'\[ \]\s?{action_item_pattern}', body)
        if match:
            start_pos = match.end()
            remaining_text = body[start_pos:]
            nextLine = remaining_text.splitlines()[1].strip() if len(remaining_text.splitlines()) > 1 else ""
            if "<comment>" in nextLine:
                # Extract comment from <comment></comment> tags if present
                comment_match = re.search(r'<comment>(.*?)</comment>',remaining_text, re.DOTALL)
                actionItemComment = comment_match.group(1).strip() if comment_match else ""
            else:
                actionItemComment = ""

        # # Extract details that follow the action item until the next "- [" or blank line
        # action_item_pattern = re.escape(actionItem)
        # # Find the position of this action item in the body
        # match = re.search(rf'\[ \]\s?{action_item_pattern}', body)
        # if match:
        #     start_pos = match.end()
        #     # Extract text from after the action item to the next "- [" or blank line
        #     remaining_text = body[start_pos:]
        #     # Find the end position (next "- [" or double newline)
        #     end_match = re.search(r'(\n\s*- \[|\n\s*\n)', remaining_text)
        #     if end_match:
        #         actionItemDetails = remaining_text[:end_match.start()].strip()
        #     else:
        #         actionItemDetails = remaining_text.strip()
        # else:
        #     actionItemDetails = ""

            actionItemsWithComments[actionItem.strip()] = actionItemComment
        

    # Replace the dictionary with an instance of the Note dataclass
    note = NoteData(
        id=uniqueIdentifier,
        fileName = noteFileName,
        filePath = os.path.join(notePath, noteFileName),
        date = date,
        osFileDateTime = osFileDateTime,
        type = type,
        title = title,
        project = project,
        archivedProject = archivedProject,
        tags = tags,
        keywords = keywords,
        retention = retention,
        author = author,
        private = private,
        frontMatter = frontMatter,
        noteBody = body,
        backLinks = backLinks,
        archived = archived,
        hasActionItems = hasActionItems,
        actionItems = actionItems,
        actionItemsWithComments = actionItemsWithComments
    )

    return note

def get_Notes_as_list(target_dir: str, includePrivateNotes = True, includeArchivedProjects = True) -> list[NoteData]:
    """
    Workhorse method to return a list of NoteData objects from the target directory.
    """
    noteList = []
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.') and not file.startswith('_') and file.endswith('.md'):  # Skip hidden files and non markdown files
                
                note = get_Note_from_path(root, file)
                
                if note.private is True and includePrivateNotes is False:
                    pass  # skip private notes if not including them
                elif note.project != "" and includeArchivedProjects is False:
                    projectConfig = get_ProjectConfig_as_dict(note.project)
                    if projectConfig.get("Archived", False) is True:
                        pass  # skip notes from archived projects
                    else:
                        noteList.append(note)
                else:
                    noteList.append(note)
                    
    return noteList

def sort_Notes_by_date(notes: list[NoteData], descending: bool = True) -> list[NoteData]:
    """
    Sorts a list of NoteData objects by date.
    
    Args:
        notes (list[NoteData]): The list of NoteData objects to sort.
        reverse (bool): If True, sorts in descending order; if False, sorts in ascending order. Default is True.
        
    Returns:
        list[NoteData]: The sorted list of NoteData objects.
    """
    
    return sorted(notes, key=lambda note: note.date, reverse=descending)

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

def get_note_tags(noteFileNameAndPath: str) -> tuple [str,list]:
    """
    Extracts tags from a note file.
    
    Args:
        noteFileNameAndPath (str): The path to the note file.
        
    Returns:
        filename: The name of the note file.
        set: A set of unique tags found in the note file.
    """
    
    filename =  noteFileNameAndPath.split("/")[-1]
    
    if not filename.endswith(".md"):
        return filename, list()  # return empty set if not a markdown file
    
    # Read the template content
    with open(noteFileNameAndPath, 'r', encoding='utf-8') as f:
        note  = f.read()

    allTags = get_tags_from_noteText(note)
    
    return filename, allTags

def get_tags_from_noteText(note: str) -> list:
    """
    Extracts tags from a note content.
    
    Args:
        note (str): the note content as a string
        
    Returns:
        filename: The name of the note file.
        set: A set of unique tags found in the note file.
    """
    
    allTags = set()
    #get front matter tags
    frontMatterTags_match = re.search(r'tags:\s*(.*)', note)
    frontMatterTagsString = frontMatterTags_match.group(1).strip() if frontMatterTags_match else ""
    frontMatterTagsString = frontMatterTagsString.replace('#', ',')
    for tag in frontMatterTagsString.split(','):
        tag = tag.strip()
        if tag != "" and  ":" not in tag:
            allTags.add(tag)  

    #get other tags
    otherTags = re.findall(r'#(\w+)', note)
    for tag in otherTags:
        tag = tag.strip()
        if tag.startswith("#"):
            tag = tag[1:]  # Remove the leading hash if present
        allTags.add(tag)

    return list(allTags)  # Convert set to list for consistency

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

def read_templateBody(templatePath: str) -> str:
    """
    Reads the content of a template file.
    
    Args:
        templatePath (str): The path to the template file.
        
    Returns:
        str: The content of the template file.
        
    Raises:
        FileNotFoundError: If the template file does not exist.
    """
    
    if os.path.exists(templatePath) is False:
        print (f"{myTerminal.ERROR}Template file '{templatePath}' does not exist.{myTerminal.RESET}")
        return ""
    else:
        with open(templatePath, 'r', encoding='utf-8') as f:
            return f.read()

def merge_template_with_values(timestamp_id, timestamp_full, selectedProjectName, templateBody: str, mergeData: dict) -> str:
    """
    Merges a template string with values from a dictionary.
    
    Args:
        template (str): The template string containing placeholders.
        values (dict): A dictionary containing values to replace the placeholders.
        
    Returns:
        str: The merged string with placeholders replaced by actual values.
    """
     
    #handle the common date tags with hard coded values 
    timestamp_id = timestamp_id.split("_")[0]  # Ensure timestamp_id is just the date part
    templateBody = templateBody.replace("[YYYYMMDDHHMMSS]", timestamp_id)
    templateBody = templateBody.replace("[TIMESTAMP_ID]", timestamp_id)
    templateBody = templateBody.replace("[YYYY-MM-DD HH:MM:SS]", timestamp_full)
    templateBody = templateBody.replace("[DATETIME]", timestamp_full)
    templateBody = templateBody.replace("[YYYY-MM-DD]", timestamp_full.split(" ")[0])
    templateBody = templateBody.replace("[DATE]", timestamp_full.split(" ")[0])

    #handle the project, author and tags with synonyms    
    projectTag_synonyms = ["Project Name", "ProjectName", "Project"]
    authorTag_synonyms = ["Current User", "User", "Username", "Author", "author"]
    tagTag_synonyms = ["tags", "Tags", "TAGS"]
    title = ""
    for key, value in mergeData.items():
        if key in projectTag_synonyms:
            for synonym in projectTag_synonyms:
                placeholder = f"[{synonym}]"
                templateBody = templateBody.replace(placeholder, value)
        elif key in authorTag_synonyms:
            for synonym in authorTag_synonyms:
                placeholder = f"[{synonym}]"
                templateBody = templateBody.replace(placeholder, value)
        elif key in tagTag_synonyms:
            for synonym in tagTag_synonyms:
                placeholder = f"[{synonym}]"
                templateBody = templateBody.replace(placeholder, value)
                tags = ""
                for tag in value.split(","):
                    tag = tag.strip().replace(" ","_")
                    tags += f"#{tag} "
                templateBody = templateBody.replace(placeholder, tags.strip())
        else:
            if key.upper() == "TITLE":
                title = value
            placeholder = f"[{key}]"
            # Case-insensitive replace for placeholders
            pattern = re.compile(re.escape(placeholder), re.IGNORECASE)
            templateBody = pattern.sub(str(value), templateBody)
    
    #make sure the new note directory directory exists
    if selectedProjectName == "" or selectedProjectName is None:
        #project selected, save in the project folder
        newNote_directory = myPreferences.root_pkv()
    else:
        #project not selected, save in the root of the PKV            
        newNote_directory = os.path.join(myPreferences.root_projects(), selectedProjectName)

    titleLettersAndNumbers = letters_and_numbers_only(title)  # Limit to 200 characters and remove special characters
    uniqueIdentifier = generate_unique_identifier(timestamp_id, "atomic", titleLettersAndNumbers)

    output_filename = f"{uniqueIdentifier}.md"
    output_path = os.path.join(newNote_directory, output_filename)

    # Save the new note
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(templateBody)
    
    myVersionControl.add_and_commit(output_path, f"create atomic note note: {title} from a fleeting note on {timestamp_full}")

    print(f"{myTerminal.SUCCESS}Note created:{myTerminal.RESET} {output_path}")
    #os.system(f'{myPreferences.default_editor()} "{output_path}"')
    
    return uniqueIdentifier

def get_note_frontMatter(noteBody: str) -> str:
    """
    Extracts the front matter from a note body.
    
    Args:
        noteBody (str): The content of the note.
        
    Returns:
        str: The front matter of the note, if present; otherwise, an empty string.
    """
    
    frontMatter_match = re.search(r'^---\n(.*?)\n---', noteBody, re.DOTALL)
    if frontMatter_match:
        return frontMatter_match.group(1).strip()
    
    return ""

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
    
    if "---" in body:
        body = body.split("---", 1)[-1].strip()
    
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

def get_note_date_from_frontMatter(frontMatter: str) -> str:
    """
    Extracts the date from the front matter of a note.
    
    Args:
        frontMatter (str): The front matter of the note.
        
    Returns:
        str: The date of the note, if present; otherwise, an empty string.
    """
    
    date_match = re.search(r'date:\s*(.*)', frontMatter.replace("*",""))
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
        return match.group(1).strip()
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

def get_Note_with_TODO(target_dir: str) -> list[NoteData]:
    """
    Returns a dictionary of notes that contain TODO items.
    value dictionary contains keys "notePathAndFile" and "frontMatter".
    """
    filteredNotes = []
    for note in get_Notes_as_list(target_dir):
        if "#TODO" in note.noteBody:
            filteredNotes.append(note)
    
    return filteredNotes

def get_Note_with_INCOMPLETE(target_dir: str) -> list[NoteData]:
    """
    Returns a dictionary of notes that contain INCOMPLETE items.
    """
    filteredNotes = []
    for note in get_Notes_as_list(target_dir):
        if "#INCOMPLETE" in note.noteBody:
            filteredNotes.append(note)
    
    return filteredNotes

def get_Note_with_ActionItems(target_dir: str) -> list[NoteData]:
    """
    Returns a dictionary of notes that contain Action items.
    value dictionary contains keys "notePathAndFile" and "frontMatter".
    """
    
    filteredNotes = []
    for note in get_Notes_as_list(target_dir):
        if "[ ]" in note.noteBody:
            filteredNotes.append(note)
    
    filteredNotes = sorted(
            filteredNotes,
            key=lambda item: item.date,
            reverse=False
        )
    
    return filteredNotes

    files_dict = {}
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.') and file.endswith(".md"):  # skip hidden files
                notePathAndFile = os.path.join(root, file)
                with open(notePathAndFile, 'r', encoding='utf-8') as f:
                    noteBody  = f.read()
                    if "[ ]" in noteBody:  
                        uniqueIdentifier = file.split(".")[0]
                        frontMatter = get_note_frontMatter(noteBody)
                        files_dict[uniqueIdentifier] = {"notePathAndFile": notePathAndFile,
                                                        "date": get_note_date_from_frontMatter(frontMatter),
                                                        "title": get_stringValue_from_frontMatter("title", frontMatter),
                                                        "project": get_stringValue_from_frontMatter("project", frontMatter),
                                                        "frontMatter": get_note_frontMatter(noteBody)}
    
    files_dict = dict(
        sorted(
            files_dict.items(),
            key=lambda item: item[1].get("date", ""),
            reverse=False
        )
    )
         
    return files_dict

def get_Note_Last_Project_Note_ByType(projectName: str, noteType: str) -> tuple[bool,NoteData]:
    """
    Returns the most recent note of a specific type for a given project.
    
    Args:
        projectName (str): The name of the project.
        noteType (str): The type of note to filter by.
        
    Returns:
        tuple: A tuple containing a boolean indicating success and the NoteData object if found.
    """
    if projectName == "" or projectName is None:
        #if there is no project name, return notes from the root PKV
        allNotes = get_Notes_as_list(myPreferences.root_pkv(), True)
    else:
        #if there is a project name, only return notes for that project
        allNotes = get_Notes_as_list(os.path.join(myPreferences.root_projects(), projectName), True)

    sortedNotes = sorted(allNotes, key=lambda note: (note.project, note.date), reverse=True)

    if not sortedNotes:
        print(f"{myTerminal.ERROR}No notes found.{myTerminal.RESET}")
        return False, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)
    
    for note in sortedNotes:
        if note.project.upper() == projectName.upper() and noteType.upper() in note.type.upper():        
            return True, note  # Return the first matching note
           
    return False, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)
# todo at some point dumping and loading notes to/from JSON files would be useful
# for now, at least with small vaults, the entire vault can be loaded into memory 
# so quickly that we don't need to get fancy.
def dump_notes_to_json(notes: List[NoteData], file_path: str, indent: int = 2) -> bool:
    """
    Dumps a list of Note objects to a JSON file.
    
    Args:
        notes (List[Note]): List of Note objects to serialize.
        file_path (str): Path where the JSON file will be saved.
        indent (int): Number of spaces for JSON indentation. Default is 2.
        
    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        # Convert Note objects to dictionaries
        notes_data = [note.to_dict() for note in notes]
        
        # Write to JSON file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(notes_data, f, indent=indent, ensure_ascii=False)
        
        return True
    except Exception as e:
        print(f"Error writing notes to JSON file: {e}")
        return False
    
def load_notes_from_json(file_path: str) -> List[NoteData]:

    """
    Loads Note objects from a JSON file.
    
    Args:
        file_path (str): Path to the JSON file to load.
        
    Returns:
        List[Note]: List of Note objects loaded from the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            notes_data = json.load(f)
        
        # Convert dictionaries back to Note objects
        notes = [NoteData(**note_dict) for note_dict in notes_data]
        
        return notes
    except Exception as e:
        print(f"Error loading notes from JSON file: {e}")
        return []

def clone_note(sourceNotePath) -> str:
    """
    Clones an existing note to a new note with a unique identifier.
    
    Args:
        sourceNotePath (str): The path to the source note file.
        
    Returns:
        str: The path to the newly created cloned note.
    """
    
    if not os.path.isfile(sourceNotePath):
        print(f"{myTerminal.ERROR}Source note '{sourceNotePath}' does not exist.{myTerminal.RESET}")
        return ""
    
    notePath = os.path.dirname(sourceNotePath)

    with open(sourceNotePath, 'r', encoding='utf-8') as f:
        noteContent = f.read()
        
    frontMatter = get_note_frontMatter(noteContent)
    body = get_note_body(noteContent)
    
    date = get_note_date_from_frontMatter(frontMatter)
    if date == "":
        date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    newBody = body
    # Replace the date line in the body with the current date
    date_pattern = r'\*\*Date:\*\*.*'
    replacement_date = f"**Date:** {date}"
    newBody = re.sub(date_pattern, replacement_date, body)
    
    oldId = get_stringValue_from_frontMatter("id", frontMatter)
    oldCreated = get_stringValue_from_frontMatter("created", frontMatter)
    oldModified = get_stringValue_from_frontMatter("modified", frontMatter)
    oldTitle = get_stringValue_from_frontMatter("title", frontMatter)
    oldType = get_stringValue_from_frontMatter("type", frontMatter)

    timestamp_id = datetime.datetime.now().strftime(myPreferences.timestamp_id_format())
    selectedDateTime = datetime.datetime.now()
    timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    

    newFileName = generate_unique_identifier(timestamp_id, "", oldTitle) + ".md"
    
    newFrontMatter = frontMatter
    newFrontMatter = re.sub(r'id:\s*.*', f'id: {timestamp_id}', newFrontMatter)  # Update the id in front matter
    newFrontMatter = re.sub(r'created:\s*.*', f'created: {timestamp_full}', newFrontMatter)  # Update the created in front matter
    newFrontMatter = re.sub(r'modified:\s*.*', f'modified: {timestamp_full}', newFrontMatter)  # Update the modified in front matter

    newNoteContent = f"---\n{newFrontMatter}\n---\n\n{newBody}"

    with open(os.path.join(notePath, newFileName), 'w', encoding='utf-8') as f:
        f.write(newNoteContent)

    return os.path.join(notePath, newFileName)
        
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