"""
Notes module - Contains NoteData class and all note-related operations.
"""

from . import Preferences as myPreferences
from . import Terminal as myTerminal
from dataclasses import dataclass
from typing import List
import json
import os
import re
import datetime
from dataclasses import field  
import time


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
    endDate: str = ""  # optional end date for gantt charts
    
    def to_dict(self):
        return {
            "id": self.id.strip(),
            "fileName": self.fileName.strip(),
            "filePath": self.filePath.strip(),
            "date": self.date.strip(),
            "osFileDateTime": self.osFileDateTime.strip(),
            "type": self.type.strip(),
            "title": self.title.strip(),
            "project": self.project.strip(),
            "tags": self.tags,
            "keywords": self.keywords,
            "retention": self.retention.strip(),
            "author": self.author.strip(),
            "private": self.private,
            "frontMatter": self.frontMatter,
            "noteBody": self.noteBody,
            "backLinks": self.backLinks,
            "archived": self.archived,
            "hasActionItems": self.hasActionItems,
            "actionItems": self.actionItems,
            "actionItemsWithComments": self.actionItemsWithComments,
            "archivedProject": self.archivedProject,
            "endDate": self.endDate.strip()
        }
      
    def __str__(self):
        if self.project != "":
            return f"{self.title} ({self.date}) from {self.project}"
        else:
            return f"{self.title} ({self.date})"

#== main functions to open notes by id or file name ===
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

#=== Functions to get notes by various criteria ===
def get_Notes_from_Project(projectName: str) -> list[NoteData]:
    """
    Returns a list of NoteData objects from a project name.
    
    Args:
        projectName (str): The name of the project.
    """
    
    notesInProject = []
    notes = get_Notes_as_list(myPreferences.root_pkv())
    for note in notes:
        if note.project == projectName:
            notesInProject.append(note)

    return notesInProject

def get_TaskNotes_from_Project(projectName: str) -> list[NoteData]:
    """
    Returns a list of NoteData objects of type 'task' from a project name.
    
    Args:
        projectName (str): The name of the project.
    """
    
    taskNotesInProject = []
    notes = get_Notes_as_list(myPreferences.root_pkv())
    for note in notes:
        if note.project == projectName and note.type.lower() == "project-task":
            taskNotesInProject.append(note)

    return taskNotesInProject

def read_Note_from_path(notePathAndFile: str) -> str:
    """
    Reads the content of a note file.
    
    Args:
        notePathAndFile (str): The full path and filename of the note.
        
    Returns:
        str: The content of the note file.
        
    Raises:
        FileNotFoundError: If the note file does not exist.
    """
    if os.path.exists(notePathAndFile) is False:
        print(f"{myTerminal.ERROR}Note file '{notePathAndFile}' does not exist.{myTerminal.RESET}")
        return ""

    with open(notePathAndFile, 'r', encoding='utf-8') as f:
        noteContent = f.read()
                    
    return noteContent

def read_Note_from_path_and_file(notePath: str, noteFileName: str) -> str:
    """
    Reads the content of a note file.
    
    Args:
        notePath (str): The directory containing the note.
        noteFileName (str): The filename of the note.
        
    Returns:
        str: The content of the note file.
        
    Raises:
        FileNotFoundError: If the note file does not exist.
    """
    
    notePathAndFile = os.path.join(notePath, noteFileName)
    return read_Note_from_path(notePathAndFile)

def write_Note_to_path(notePathAndFile: str, noteContent: str) -> bool:
    """
    Writes content to a note file.
    
    Args:
        notePathAndFile (str): The full path and filename of the note.
        noteContent (str): The content to write to the note file.
        
    Returns:
        bool: True if the write was successful, False otherwise.
    """
    try:
        if not os.path.exists(os.path.dirname(notePathAndFile)):
            os.makedirs(os.path.dirname(notePathAndFile), exist_ok=True)
            time.sleep(1)

        with open(notePathAndFile, 'w', encoding='utf-8') as f:
            f.write(noteContent)
        return True
    except Exception as e:
        print(f"{myTerminal.ERROR}Failed to write to note file '{notePathAndFile}': {e}{myTerminal.RESET}")
        return False

def get_Note_from_path(notePath: str, noteFileName: str) -> NoteData:
    """
    Loads a NoteData object from a file path.
    
    Args:
        notePath (str): The directory containing the note.
        noteFileName (str): The filename of the note.
        
    Returns:
        NoteData: The loaded note data object.
    """
    # Import here to avoid circular dependency
    from . import Tools as myTools
    
    notePathAndFile = os.path.join(notePath, noteFileName)

    if os.path.exists(notePathAndFile) is False:
        print(f"{myTerminal.ERROR}Note file '{notePathAndFile}' does not exist.{myTerminal.RESET}")
        return NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)

    with open(os.path.join(notePath, noteFileName), 'r', encoding='utf-8') as f:
        noteContent = f.read()
                    
    frontMatter = get_note_frontMatter(noteContent)
    
    osFileDateTime = datetime.datetime.fromtimestamp(os.path.getmtime(notePathAndFile)).strftime("%Y-%m-%d %H:%M:%S")
    date = get_note_date_from_frontMatter(frontMatter, dateProperty = "start date")
    dateEnd = get_note_date_from_frontMatter(frontMatter, dateProperty = "end date")
    
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
        projectConfig = myTools.get_ProjectConfig_as_dict(project)
        if projectConfig.get("Archived", False) is True:
            archivedProject = True

    type = get_stringValue_from_frontMatter("type", frontMatter)
    if type == "":
        type = "unknown"
    title = get_stringValue_from_frontMatter("title", frontMatter)
    tags = get_tags_from_Text(noteContent)
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
        actionItemsWithComments = actionItemsWithComments,
        endDate = dateEnd
    )

    return note

def get_Notes_as_list(target_dir: str, includePrivateNotes = True, includeArchivedProjects = True) -> list[NoteData]:
    """
    Workhorse method to return a list of NoteData objects from the target directory.
    """
    # Import here to avoid circular dependency
    from . import Tools as myTools
    
    noteList = []
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.') and not file.startswith('_') and file.endswith('.md'):  # Skip hidden files and non markdown files
                
                note = get_Note_from_path(root, file)
                
                if note.private is True and includePrivateNotes is False:
                    pass  # skip private notes if not including them
                elif note.project != "" and includeArchivedProjects is False:
                    projectConfig = myTools.get_ProjectConfig_as_dict(note.project)
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

    allTags = get_tags_from_Text(note)
    
    return filename, allTags

def get_tags_from_Text(note: str) -> list:
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

def load_MostRecentProjectProgressNote(projectName: str) -> tuple[bool,NoteData]:
    """
    Loads the most recent progress note for a given project.
    
    Args:
        projectName (str): The name of the project.
        
    Returns:
        tuple: A tuple containing a boolean indicating success and the NoteData object if found.
    """

    allNotes = get_Notes_as_list(myPreferences.root_pkv())
    sortedNotes = sorted(allNotes, key=lambda note: (note.project, note.date), reverse=True)

    if not sortedNotes:
        print(f"{myTerminal.ERROR}No notes found.{myTerminal.RESET}")
        return False, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)
    
    for note in sortedNotes:
        if note.project.upper() == projectName.upper() and "progress".upper() in note.type.upper():
            return True, note  # Return the first matching note
           
    return False, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)

#=== JSON Dump and Load Functions ===
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

#=== Note Cloning and Opening Functions ===
def clone_note(sourceNotePath) -> str:
    """
    Clones an existing note to a new note with a unique identifier.
    
    Args:
        sourceNotePath (str): The path to the source note file.
        
    Returns:
        str: The path to the newly created cloned note.
    """
    # Import here to avoid circular dependency
    from . import Tools as myTools
    
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
    

    oldTitle = get_stringValue_from_frontMatter("title", frontMatter)

    timestamp_id = datetime.datetime.now().strftime(myPreferences.timestamp_id_format())
    selectedDateTime = datetime.datetime.now()
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    

    newFileName = myTools.generate_unique_identifier(timestamp_id, "", oldTitle) + ".md"
    
    newFrontMatter = frontMatter
    newFrontMatter = re.sub(r'id:\s*.*', f'id: {timestamp_id}', newFrontMatter)  # Update the id in front matter
    newFrontMatter = re.sub(r'created:\s*.*', f'created: {timestamp_full}', newFrontMatter)  # Update the created in front matter
    newFrontMatter = re.sub(r'modified:\s*.*', f'modified: {timestamp_full}', newFrontMatter)  # Update the modified in front matter

    newNoteContent = f"---\n{newFrontMatter}\n---\n\n{newBody}"

    with open(os.path.join(notePath, newFileName), 'w', encoding='utf-8') as f:
        f.write(newNoteContent)

    return os.path.join(notePath, newFileName)

#=== Note Opening Functions ===
def open_note_in_editor(notePath: str):
    """
    Opens a note in the default editor specified in preferences.
    
    Args:
        notePath (str): The path to the note file.
    """
    
    # Import here to avoid circular dependency
    from . import Tools as myTools

    os.system(f'{myPreferences.default_editor()} "{notePath}"')
    if myPreferences.default_editor() != "obsidian":
        os.system(f'{myPreferences.default_editor()} "{notePath}"')
    else:
        # For Obsidian, open the vault and the specific note
        vaultName = myPreferences.root_pkv().split("/")[-1]
        fileName = notePath.split("/")[-1]
        encodedFileName = myTools.obsidian_Encode_for_URI(fileName)
        openCmd = f"obsidian://advanced-uri?vault={vaultName}&filepath={encodedFileName}&openmode=true"
        os.system(f'open "{openCmd}"')

# === Front Matter and Note Body Parsing Functions ===
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

def get_note_body(wholeNote: str) -> str:
    """
    Extracts the content of a note, excluding the front matter.
    
    Args:
        noteBody (str): The content of the note.
        
    Returns:
        str: The content of the note, excluding the front matter.
    """
    body = ""
    frontMatter = get_note_frontMatter(wholeNote)
    
    body = wholeNote.replace(f"---\n{frontMatter}\n---", "").strip()
    
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

def replace_lineLabelValue_in_noteBody(lineLabel:str, newValue:str, noteBody: str) -> str:
    """
    Replaces a line label value in the note body with a new value.
    
    Args:
        lineLabel (str): The label of the line to replace.
        newValue (str): The new value to set.
        noteBody (str): The content of the note.
        
    Returns:
        str: The updated note body.
    """
    pattern = rf'{re.escape(lineLabel)}[^\n]*'
    replacement = f'{lineLabel} {newValue}'
    updatedNoteBody = re.sub(pattern, replacement, noteBody, flags=re.IGNORECASE)
    return updatedNoteBody

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
