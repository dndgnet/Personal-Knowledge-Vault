import datetime 
import os 
import re 

from . import Preferences as myPreferences

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

def get_NoteFiles_dict(target_dir: str) -> dict:
    files_dict = {}
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.'):  # Skip hidden files
                uniqueIdentifier = file.split(".")[0]
                if file.endswith('.md'):
                    files_dict[uniqueIdentifier] = [file, os.path.join(root, file)]
                    
    return files_dict

def get_NoteFiles_withTags_dict(target_dir: str) -> dict:
    files_dict = {}
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.'):  # Skip hidden files
                uniqueIdentifier = file.split(".")[0]
                if file.endswith('.md'):
                    files_dict[uniqueIdentifier] = [file, os.path.join(root, file), get_note_tags(os.path.join(root, file))]
                    
    return files_dict

def get_NoteFiles_as_dict(target_dir: str) -> dict:
    files_dict = {}
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.') and file.endswith('.md'):  # Skip hidden files and non markdown files
                
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    noteContent = f.read()
                    
                frontMatter = get_note_frontMatter(noteContent)
                
                uniqueIdentifier = file.split(".")[0]
                osFileDateTime = datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(root, file))).strftime("%Y-%m-%d %H:%M:%S")
                date = get_note_date_from_frontMatter(frontMatter)
                if date == "":
                    # If no date in front matter, use the file's last modified date
                    date = osFileDateTime
                
                project = get_stringValue_from_frontMatter("project", frontMatter)
                type = get_stringValue_from_frontMatter("type", frontMatter)
                if type == "":
                    type = "unknown"
                title = get_stringValue_from_frontMatter("title", frontMatter)
                tags = get_tags_from_noteText(noteContent)
                keywords = get_listValue_from_frontMatter("keywords",frontMatter)
                retention = get_stringValue_from_frontMatter("retention", frontMatter)
                author = get_stringValue_from_frontMatter("author", frontMatter)
            
                if title == "" or title is None:
                    title = uniqueIdentifier
                    
                body = get_note_body(noteContent)
                backLinks = get_note_backlinks(noteContent)
                
                note = {"fileName": file,
                        "filePath": os.path.join(root, file),
                        "date": date,
                        "osFileDateTime": osFileDateTime,
                        "type": type,
                        "title": title,
                        "project": project,
                        "tags": tags, 
                        "keywords": keywords,
                        "retention": retention,
                        "author": author,
                        "frontMatter": frontMatter,
                        "noteBody": body,
                        "backLinks": backLinks
                        } 
                
                files_dict[uniqueIdentifier] = note
                    
    return files_dict

def get_pkv_NoteFiles() -> dict:
    """
    Returns a dictionary of all files in the PKV.
    
    Returns:
        dict: A dictionary where keys are filenames and values are their full paths.
    """
    
    pkvPath = myPreferences.root_pkv()
    if not os.path.isdir(pkvPath):
        return {}
    
    files_dict = get_NoteFiles_dict(pkvPath)
    
    return files_dict

def get_project_NoteFiles(projectName: str) -> dict:
    """
    Returns a dictionary of all files in a specific project.
    
    Args:
        projectName (str): The name of the project.
        
    Returns:
        dict: A dictionary where keys are filenames and values are their full paths.
    """
    
    projectPath = os.path.join(myPreferences.root_projects(), projectName)
    if not os.path.isdir(projectPath):
        return {}
    
    files_dict = get_NoteFiles_dict(projectPath)
    
    return files_dict

def is_NewNote_identifier_unique(noteIdentifier) -> bool:
    """
    Checks if a note identifier is unique across all notes in the PKV.
    
    Args:
        noteIdentifier (str): The identifier to check for uniqueness.
        
    Returns:
        bool: True if the identifier is unique, False otherwise.
    """
    pkvFiles = get_pkv_NoteFiles()
    
    if noteIdentifier in pkvFiles.keys():
        return False
    else: 
        return True

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

def get_Note_with_TODO(target_dir: str) -> dict:
    """
    Returns a dictionary of notes that contain TODO items.
    value dictionary contains keys "notePathAndFile" and "frontMatter".
    """
    files_dict = {}
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.') and file.endswith(".md"):  # skip hidden files
                notePathAndFile = os.path.join(root, file)
                with open(notePathAndFile, 'r', encoding='utf-8') as f:
                    noteBody  = f.read()
                    if '#TODO' in noteBody:  
                        uniqueIdentifier = file.split(".")[0]
                        files_dict[uniqueIdentifier] = {"notePathAndFile": notePathAndFile,
                                                        "frontMatter": get_note_frontMatter(noteBody)}
                    
    return files_dict

def get_Note_with_INCOMPLETE(target_dir: str) -> dict:
    """
    Returns a dictionary of notes that contain INCOMPLETE items.
    value dictionary contains keys "notePathAndFile" and "frontMatter".
    """
    files_dict = {}
    for root, dirs, files in os.walk(target_dir, topdown=True):
        for file in files:
            if not file.startswith('.') and file.endswith(".md"):  # skip hidden files
                notePathAndFile = os.path.join(root, file)
                with open(notePathAndFile, 'r', encoding='utf-8') as f:
                    noteBody  = f.read()
                    if '#INCOMPLETE' in noteBody:  
                        uniqueIdentifier = file.split(".")[0]
                        files_dict[uniqueIdentifier] = {"notePathAndFile": notePathAndFile,
                                                        "frontMatter": get_note_frontMatter(noteBody)}
                    
    return files_dict

def get_Note_with_ActionItems(target_dir: str) -> dict:
    """
    Returns a dictionary of notes that contain Action items.
    value dictionary contains keys "notePathAndFile" and "frontMatter".
    """
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