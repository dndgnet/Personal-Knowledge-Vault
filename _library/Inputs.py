""" 
Collect inputs from users for specific tasks.
"""

from . import Preferences as myPreferences
from . import Tools as myTools
from . import Terminal as myTerminal

import os
import re
from datetime import datetime

# Define the template and output paths
template_pathRoot = os.path.join(os.getcwd(),"_templates")

def get_datetime_and_title_from_user(datePrompt = "enter a date time", defaultIfNone = datetime.now(), 
                                     titlePrompt = "enter note title", titleDefault = "untitled" ) -> tuple[datetime,str]:
    """
    Get a datetime from the user.
    returns the default datetime if the user doesn't provide a valid datetime
    for example, if the user enters an empty string
    """
    inputDate = input(f"{myTerminal.INPUTPROMPT}{datePrompt}{myTerminal.RESET}").strip()
    isDateTime, d = myTools.datetime_fromString(inputDate)
    if not isDateTime:
        print(f"\t{myTerminal.YELLOW}Using default: {defaultIfNone.strftime(myPreferences.datetime_format())}{myTerminal.RESET}")
        d = defaultIfNone
        
    title = input(f"{myTerminal.INPUTPROMPT}{titlePrompt}: {myTerminal.RESET}").strip()
    
    if not title:
        title = titleDefault
        print(f"\t{myTerminal.YELLOW}Using default title: {title}{myTerminal.RESET}")
    
    return d, title
    
def select_project_name(showNewProjectOption = True) -> tuple[dict,str, int]:
    """
    Prompt the user to select a project from a list of available projects.
    If the user selects "No Project", return an empty string.
    If the user selects "New Project", prompt for a new project name and create it.
    returns 
    projects dictionary, 
    selected project name, 
    selected project integer
    """
    projectIndex = 1
    projects = {}

    #let hte user pic which project to use
    #print(f"{myTerminal.INPUTPROMPT}Available projects:{myTerminal.RESET}")
    projectIndex = 0
    projects[projectIndex] = "No Project"
    print(f"\t{projectIndex}. {projects.get(1, 'No Project')}")
    
    projectIndex = 1
    if showNewProjectOption:
        projects[projectIndex] = "New Project"
        print(f"\t{projectIndex}. {projects.get(1, 'New Project')}")
    
    for filename in sorted(os.listdir(myPreferences.root_projects())):
        if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
            projectIndex += 1
            print(f"\t{projectIndex}. {filename}")
            projects[projectIndex] = filename

    selectedProject = input(f"Select a project (0-{projectIndex}): ")

    if not selectedProject.isdigit() or int(selectedProject) not in projects:
        # print(f"{myTerminal.ERROR}Invalid selection. Please select a valid project number.{myTerminal.RESET}")
        # exit(1)
        return projects, "", 0

    if int(selectedProject) == 0:
        # print(f"{myTerminal.ERROR}Not yet implemented, I haven't decided what to do with no project calls. Exiting.{myTerminal.RESET}")
        # exit(1)
        return projects, "", 0

    if int(selectedProject) == 1:
        newProjectName = input(f"{myTerminal.INPUTPROMPT}Enter a new project name: {myTerminal.RESET}").strip()
        if not newProjectName:
            print(f"{myTerminal.ERROR}Project name cannot be empty.{myTerminal.RESET}")
            exit(1)
        newProjectPath = os.path.join(myPreferences.root_projects(), f"Project {newProjectName}")
        os.makedirs(newProjectPath, exist_ok=True)
        selectedProject = projectIndex + 1
        projects[selectedProject] = f"Project {newProjectName}"
        print(f"{myTerminal.SUCCESS}New project created: {newProjectPath}{myTerminal.RESET}")
        
    print(f"{myTerminal.SUCCESS}Selected project: {projects[int(selectedProject)]}{myTerminal.RESET}\n")
    return projects, projects[int(selectedProject)], int(selectedProject)

def select_template(templateType = "All") -> tuple[dict,str, int]:
    """ 
        Get the template from the user.
        exits if the user does not select a valid template
    """  
    
    templateIndex = 1
    templates = {}
    print(f"{myTerminal.INPUTPROMPT}Available templates:{myTerminal.RESET}")
    for filename in os.listdir(template_pathRoot):
        if filename.upper().startswith(f"{templateType.upper()}_") or templateType.upper() in ("ALL",""):
            
            if templateType.upper() == "ALL" or templateType =="":
                print(f"""\t{templateIndex}. {filename.replace("_template.markdown","")}""")
            else:
                #don't show the template type in the list if it's not "All"
                print(f"""\t{templateIndex}. {filename.replace(f"{templateType}_","").replace("_template.markdown","")}""")
                
            templates[templateIndex] = filename
            templateIndex += 1
        
    selectedTemplate = input(f"Select a template (1-{len(templates)}): ")

    if not selectedTemplate.isdigit() or int(selectedTemplate) not in templates:
        print(f"{myTerminal.ERROR}Invalid selection. Please select a valid template number.{myTerminal.RESET}")
        exit(1)

    print(f"{myTerminal.SUCCESS}Selected template: {templates[int(selectedTemplate)]}{myTerminal.RESET}\n")
    
    return templates, templates[int(selectedTemplate)], int(selectedTemplate)

def select_attachment_from_user(projectName="", uniqueIdentifier = "") -> tuple[str, str]:
    """
    Get the attachment file path from the user.
    Returns the full path to the attachment file.
    """
    
    downloads_folder = myPreferences.attachmentPickUp_path()
    files = [
        (f, os.path.getmtime(os.path.join(downloads_folder, f)))
        for f in os.listdir(downloads_folder)
        if os.path.isfile(os.path.join(downloads_folder, f))
    ]
    files_sorted = sorted(files, key=lambda x: x[1], reverse=True)
    downloads_dict = {f: mtime for f, mtime in files_sorted}

    fileIndex = 0
    print(f"{myTerminal.INPUTPROMPT}Recent files in attachment pick up folder:{myTerminal.RESET}")
    for file_name in downloads_dict:
        if file_name.startswith('.'):
            continue  # Skip hidden files
        
        fileIndex += 1
        print(f"\t{myTerminal.INPUTPROMPT}{fileIndex}: {file_name}{myTerminal.RESET}")
        if fileIndex > 20:
            print(f"\t\t{myTerminal.YELLOW}only showing the first 20.{myTerminal.RESET}")
            break

    if fileIndex == 0:
        print(f"{myTerminal.ERROR}No files found in the attachment pick up folder.{myTerminal.RESET}")
        return "",""

    #select a file
    input_string = input(f"{myTerminal.INPUTPROMPT}Select a file (1-{fileIndex} or 0 to skip attachment):{myTerminal.RESET} ")
    if input_string.isdigit() and 1 <= int(input_string) <= fileIndex:
        selected_file = list(downloads_dict.keys())[int(input_string) - 1]
        sourcefile_path = os.path.join(downloads_folder, selected_file)
    else:
        return "",""
    
    if projectName is None or projectName == "":
        destination_path = myPreferences.root_attachments()
    else:
        destination_path = os.path.join(myPreferences.root_projects(),
                                        projectName,
                                        "_Attachments")        
    # Move the file to the attachments root
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    
    newFileName = f"{uniqueIdentifier}_{selected_file}".replace(" ","_").replace(":","-").replace("/","-")    
    destination_path = os.path.join(destination_path, newFileName)
    
    os.rename(sourcefile_path, destination_path)
    
    return selected_file,newFileName

def select_recent_note() -> tuple[str, dict]:
    """
    Get the most recent note from the user.
    Returns the note ID and the note dictionary.
    """
    
    allNotes = myTools.get_NoteFiles_as_dict(myPreferences.root_pkv())
    sortedNotes = dict(sorted(allNotes.items(), key=lambda item: item[1]["date"], reverse=True))
    
    if not sortedNotes:
        print(f"{myTerminal.ERROR}No notes found.{myTerminal.RESET}")
        return "", {}
    
    print(f"{myTerminal.INPUTPROMPT}Recent notes:{myTerminal.RESET}")
    noteIndex = 0
    for noteId, note in sortedNotes.items():
        noteIndex += 1
        print(f"\t {noteIndex}) {note.get('date', 'No date')} - {note.get('title', 'No title')}")
        if noteIndex > 5:
            break  # Show only the first 5 notes for brevity
        
    selectedNoteId = input(f"{myTerminal.INPUTPROMPT}Select a note number or press Enter to skip: {myTerminal.RESET}").strip()
    
    if not selectedNoteId.isdigit() or int(selectedNoteId) < 1 or int(selectedNoteId) > noteIndex:
        return "", {}
    
    selectedNote = list(sortedNotes.items())[int(selectedNoteId) - 1]
    return selectedNoteId, dict(selectedNote[1])
    
def get_templateMerge_Values_From_User(timestamp_id,timestamp_date,timestamp_full,
                                       selectedProjectName,title,note_Content: str) -> str:
    """
    Get the template merge values from the user.
    Returns the populated note content with user inputs replacing template tags.
    """
    
    note_Content = note_Content.strip()
    templateTags = re.findall(r"\[(.*?)\]", note_Content)
    templateTags = set(templateTags)  # remove duplicates
    
    #get title and tags captured first
    if "Title" in templateTags:
        note_Content = note_Content.replace("[Title]", title)
        templateTags.remove("Title")
    
    if "tags" in templateTags:
        if myPreferences.show_tag_prompt():
             #ask the user for tags
            tags = ""
            templateTagValue = input(f"{myTerminal.INPUTPROMPT}Enter tags (comma-separated) or leave blank for none: {myTerminal.RESET}").strip()
            for tag in templateTagValue.split(","):
                tag = tag.strip().replace(" ","_")
                tags += f"#{tag} "
            templateTagValue = tags
        else:
            #skip tags if the user doesn't want to be prompted
            templateTagValue = ""
                
        note_Content = note_Content.replace("[tags]", templateTagValue)
        templateTags.remove("tags")
    
    #capture the rest of the tags in the template
    for templateTag in templateTags:
        templateTagValue = ""
        if "[" in templateTag or "]" in templateTag:
            pass  # skip malformed tags and images
        if templateTag.strip() == "":
            pass
        elif templateTag.upper() in ("YYYYMMDDHHMMSS", "TIMESTAMP_ID"):
            templateTagValue = timestamp_id
        elif templateTag.upper() in ("YYYY-MM-DD HH:MM:SS","DATETIME"):
            templateTagValue = timestamp_full
        elif templateTag.upper() in ("YYYY-MM-DD","DATE"):
            templateTagValue = timestamp_date
        elif templateTag in ("Project Name","ProjectName","Project"):
            templateTagValue = selectedProjectName
        elif templateTag in ("Current User","User","Username","Author","author"):
            templateTagValue = myPreferences.author_name()
        elif templateTag in ["tags","Tags","TAGS"]:
            if myPreferences.show_tag_prompt():
                #ask the user for tags
                templateTagValue = input(f"{myTerminal.INPUTPROMPT}Enter tags (comma-separated) or leave blank for none: {myTerminal.RESET}").strip()
                tags = ""
                for tag in templateTagValue.split(","):
                    tag = tag.strip().replace(" ","_")
                    tags += f"#{tag} "
                templateTagValue = tags
            else:
                #skip tags if the user doesn't want to be prompted
                templateTagValue = ""
        else:
            templateTagValue = input(f"{myTerminal.INPUTPROMPT}Enter value for [{templateTag}]: {myTerminal.RESET}").strip()

        note_Content = note_Content.replace(f"[{templateTag}]", templateTagValue)
        
    attachmentCount = 0
    addAttachment = input(f"{myTerminal.INPUTPROMPT}Add attachment? (y/n): {myTerminal.RESET}").strip().upper()

    print("")
    while addAttachment == "Y":
        selectedFile, attachmentTagValue = select_attachment_from_user(projectName=selectedProjectName, uniqueIdentifier=timestamp_id)
        if attachmentTagValue != "":
            if attachmentCount == 0:
                note_Content += "\n#### Attachments\n"
            
            attachmentCount += 1
            note_Content += f"\n[{selectedFile}](./_Attachments/{attachmentTagValue})\n"
            print(f"\t\t{myTerminal.SUCCESS}Attachment added '{selectedFile}'.{myTerminal.RESET}")
            addAttachment = input(f"{myTerminal.INPUTPROMPT}Add another attachment? (y/n): {myTerminal.RESET}").strip().upper()
        else:
            print(f"\t\t{myTerminal.WARNING}No attachment selected.{myTerminal.RESET}")
            addAttachment = "N"
               
    return note_Content

def get_templateMerge_Values_From_ExistingData( templateData: dict ,note_Content: str) -> tuple[str,str,str]:
    """
    Populate a note template using values from an existing templateData source.
    Returns the populated note content with user inputs replacing template tags.
    """
    
    note_Content = note_Content.strip()
    templateTags = re.findall(r"\[(.*?)\]", note_Content)
    templateTags = set(templateTags)  # remove duplicates
    
    _,selectedDateTime = myTools.datetime_fromString(templateData.get("date", datetime.now().strftime(myPreferences.datetime_format())))
    timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
    timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    title = templateData.get("Title", "untitled")
    selectedProjectName = templateData.get("project", "")
    
    #get title and tags captured first
    if "Title" in templateTags:
        note_Content = note_Content.replace("[Title]", title)
        templateTags.remove("Title")
    
    if "tags" in templateTags:
        tags = ""
        templateTagValue = templateData.get("tags", "")
        for tag in templateTagValue.split(","):
            tag = tag.strip().replace(" ","_")
            tags += f", {tag}"
        templateTagValue = tags[1:]  # remove the leading comma and space
                 
        note_Content = note_Content.replace("[tags]", templateTagValue)
        templateTags.remove("tags")
    
    #capture the rest of the tags in the template
    for templateTag in templateTags:
        templateTagValue = ""
        if "[" in templateTag or "]" in templateTag:
            pass  # skip malformed tags and images
        if templateTag.strip() == "":
            pass
        elif templateTag.upper() in ("YYYYMMDDHHMMSS", "TIMESTAMP_ID"):
            templateTagValue = timestamp_id
        elif templateTag.upper() in ("YYYY-MM-DD HH:MM:SS","DATETIME"):
            templateTagValue = timestamp_full
        elif templateTag.upper() in ("YYYY-MM-DD","DATE"):
            templateTagValue = timestamp_date
        elif templateTag in ("Project Name","ProjectName","Project"):
            templateTagValue = selectedProjectName
        elif templateTag in ("Current User","User","Username","Author","author"):
            templateTagValue = myPreferences.author_name()
        else:
            templateTagValue = templateData.get(templateTag, "")

        note_Content = note_Content.replace(f"[{templateTag}]", templateTagValue)
                
    return timestamp_id, title, note_Content
