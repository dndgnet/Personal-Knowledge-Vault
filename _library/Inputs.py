""" 
Collect inputs from users for specific tasks.
"""

from . import Preferences as myPreferences
from . import Tools as myTools
from . import Terminal as myTerminal
from .Tools import NoteData

import os
import re
from datetime import datetime
from datetime import timedelta
from typing import Union, List

# Define the template and output paths
template_pathRoot = os.path.join(os.getcwd(),"_templates")

maxNumberOfNotesToShow = 99
maxNumberOfDaysToGoBackWhenShowingNotes = 10  # Number of days to go back when showing recent notes

def ask_yes_no(prompt: str, default: bool = True) -> bool:
    """
    Ask the user a yes/no question and return True for yes, False for no.
    If the user presses Enter without typing anything, return the default value.
    """
    default_str = "Y" if default else "N"
    response = input(f"{myTerminal.INPUTPROMPT}{prompt} (Y/n enter for {default_str}): {myTerminal.RESET}").strip().upper()
    
    if response == "":
        return default
    elif response in ("Y", "YES"):
        return True
    elif response in ("N", "NO"):
        return False
    else:
        print(f"{myTerminal.ERROR}Invalid input. Please enter 'Y' or 'N'.{myTerminal.RESET}")
        return ask_yes_no(prompt, default)

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
    
def select_project_name_withDict(showNewProjectOption = True, showNoProjectOption = True) -> tuple[dict,str, int]:
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
    
    if showNewProjectOption or showNoProjectOption:
        print(f"\n{myTerminal.WHITE}Available options:{myTerminal.RESET}")
    
    projectIndex = 0
    projects[projectIndex] = "No Project"
    
    if showNoProjectOption:
        print(f"\t{myTerminal.GREY}{projectIndex:>2}. {projects.get(1, 'No Project')}{myTerminal.RESET}")
    
    projectIndex = 1
    if showNewProjectOption:
        projects[projectIndex] = "Start a new project"
        print(f"""\t{myTerminal.GREY}{projectIndex:>2}. {projects.get(1, "Start a new project")}{myTerminal.RESET}""")
    
    print(f"{myTerminal.WHITE}Available projects:{myTerminal.RESET}")
    for filename in sorted(os.listdir(myPreferences.root_projects())):
        if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
            projectConfig = myTools.get_ProjectConfig_as_dict(filename)
            if projectConfig.get("Archived", False):
                continue  # Skip archived projects
            else:
                projectIndex += 1
                print(f"\t{projectIndex:>2}. {filename}")
                projects[projectIndex] = filename
    
    selectedProject = input(f"Select (0-{projectIndex}): ")

    if not selectedProject.isdigit() or int(selectedProject) not in projects or int(selectedProject) == 0:
        # print(f"{myTerminal.ERROR}Invalid selection. Please select a valid project number.{myTerminal.RESET}")
        # exit(1)
        print(f"{myTerminal.SUCCESS}no project selected{myTerminal.RESET}\n")
        return projects, "", 0

    if int(selectedProject) == 1:
        newProjectName = input(f"{myTerminal.INPUTPROMPT}Enter a new project name: {myTerminal.RESET}").strip()
        if not newProjectName:
            print(f"{myTerminal.ERROR}Project name cannot be empty.{myTerminal.RESET}")
            exit(1)
        newProjectPath = os.path.join(myPreferences.root_projects(), f"{newProjectName.strip()}")
        os.makedirs(newProjectPath, exist_ok=True)
        selectedProject = projectIndex + 1
        projects[selectedProject] = f"{newProjectName.strip()}"
        print(f"{myTerminal.SUCCESS}New project created: {newProjectPath}{myTerminal.RESET}")
        
    print(f"{myTerminal.SUCCESS}Selected project: {projects[int(selectedProject)]}{myTerminal.RESET}\n")
    return projects, projects[int(selectedProject)], int(selectedProject)

def select_project_name(showNewProjectOption = True, showNoProjectOption = True) -> str:
    """
    simplified version of select_project_name_withDict that only returns the selected project name.
    """
    projects, selectedProjectName, selectedProject = select_project_name_withDict(showNewProjectOption,showNoProjectOption)

    return selectedProjectName

def select_template(templateType = "All") -> tuple[dict,str, str]:
    """ 
        Get the template from the user.
        exits if the user does not select a valid template
        returns: dictionary of templates, selected template name, selected template key
    """  
    
    templateIndex = 1
    templates = {}
    print(f"\n{myTerminal.INPUTPROMPT}Available templates:{myTerminal.RESET}")
    for filename in os.listdir(template_pathRoot):
        if filename.upper().startswith(f"{templateType.upper()}_") or templateType.upper() in ("ALL",""):
            templateName = filename.replace("_template.markdown","").replace("pkv_","").replace("project_","")
            templateKey = templateName[:1]
            while templateKey in templates.keys():
                templateKey = templateName[:len(templateKey)+1]

            if templateType.upper() == "ALL" or templateType =="":
                print(f"""\t{templateKey:<4}) {filename.replace("_template.markdown","")}""")
            else:
                #don't show the template type in the list if it's not "All"
                print(f"""\t{templateKey:>4}) {filename.replace(f"{templateType}_","").replace("_template.markdown","")}""")
                
            templates[templateKey] = filename
            templateIndex += 1
        
    selectedTemplate = input("Select a template: ").strip()

    if selectedTemplate not in templates.keys():
        print(f"{myTerminal.ERROR}Invalid selection. Please select a valid template number.{myTerminal.RESET}")
        exit(1)

    print(f"""{myTerminal.SUCCESS}Selected template: {templates[selectedTemplate].replace("_template.markdown","").replace("pkv_","").replace("project_","")}{myTerminal.RESET}\n""")
    
    return templates, templates[selectedTemplate], selectedTemplate

def select_tag(projectName="") -> str:
    
    if projectName is None or projectName == "":
        targetDirectory = myPreferences.root_pkv()
    else:
        targetDirectory = os.path.join(myPreferences.root_projects(), projectName)
        if not os.path.exists(targetDirectory):
            print(f"{myTerminal.ERROR}Project directory '{targetDirectory}' does not exist.{myTerminal.RESET}")
            return ""
    notes = myTools.get_Notes_as_list(targetDirectory)

    return select_tags_from_noteList(notes)

def select_tags_from_noteList(notes: List[myTools.NoteData]) -> str:    
    allTags = {}
    for note in notes:
        if note.tags:
            for tag in note.tags:
                tag = tag.strip()
                allTags[tag] = allTags.get(tag, 0) + 1

    tagCount = 0 
    sortedTags = sorted(allTags.items(), key=lambda x: x[1], reverse=True)

    print("available tags:")
    
    column = 0 
    line = ""
    for tag, count in sortedTags:
        tagCount += 1    
        if count == 1:
            newTag = f"{tagCount:>3}. {tag}"
        else:
            newTag = f"{tagCount:>3}. {tag} (x{count})"
        line += f"{newTag:<45}"
        column += 1
        
        if column >2:
            print(line)
            column = 0
            line = ""
            
    if line:  # Print any remaining tags on the last line
        print(line)

    userInput = input(f"Select a tag to search by number (1-{len(sortedTags)}) or 0 for no tag search: ")
    
    selectedTag = ""
    if userInput.isdigit() and 1 <= int(userInput) <= len(sortedTags):
        selectedTagIndex = int(userInput)
        selectedTag = sortedTags[selectedTagIndex - 1][0]
    else:
        selectedTag = ""
        
    return selectedTag

def select_attachment_from_user(projectName="", uniqueIdentifier = "") -> tuple[str, str]:
    """
    Get the attachment file path from the user.
    Returns the full path to the attachment file.
    """
    
    downloads_folder = myPreferences.attachmentPickUp_path()
    files = []
    for file in os.listdir(downloads_folder):
        if file.startswith('.') or file.upper() == 'DESKTOP.INI':
            continue
        
        files.append((file, os.path.getctime(os.path.join(downloads_folder, file))))

    recentFiles = sorted(files, key=lambda x: x[1], reverse=True)

    fileIndex = 0
    fileList = []
    print(f"{myTerminal.INPUTPROMPT}Recent files in attachment pick up folder:{myTerminal.RESET}")
    for file in recentFiles:
        fileIndex += 1
        fileList.append(file[0])
        print(f"\t{myTerminal.INPUTPROMPT}{fileIndex}: {file[0]}{myTerminal.RESET}")
        if fileIndex > 25:
            print(f"\t\t{myTerminal.YELLOW}only showing the first {fileIndex}.{myTerminal.RESET}")
            break


    if fileIndex == 0:
        print(f"{myTerminal.ERROR}No files found in the attachment pick up folder.{myTerminal.RESET}")
        return "",""

    #select a file
    input_string = input(f"{myTerminal.INPUTPROMPT}Select a file (1-{fileIndex} or 0 to skip attachment):{myTerminal.RESET} ")
    if input_string.isdigit() and 1 <= int(input_string) <= fileIndex:
        selected_file = fileList[int(input_string) - 1]
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

def select_recent_note(noteTypeContains = "",  showActionItems = False, 
                       groupByProject = True) -> tuple[int, NoteData]:
    """
    Get the most recent note from the user.
    Returns the note ID and the NoteData object.
    """
    
    numberOfNotesToShow = maxNumberOfNotesToShow

    allNotes = myTools.get_Notes_as_list(myPreferences.root_pkv())
    sortedNotes = sorted(allNotes, key=lambda note: (note.project, note.date), reverse=True)

    displayedNotes = []

    if not sortedNotes:
        print(f"{myTerminal.ERROR}No notes found.{myTerminal.RESET}")
        return 0, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)
    
    if noteTypeContains == "":
        print(f"{myTerminal.INPUTPROMPT}Recent notes:{myTerminal.RESET}")
    else:
        print(f"{myTerminal.INPUTPROMPT}Recent {noteTypeContains} notes:{myTerminal.RESET}")
   
    noteIndex = 0
    project = ""
    for note in sortedNotes:
        if (noteTypeContains == "Any" or noteTypeContains.upper() == "ANY" 
            or (noteTypeContains.upper() in note.type.upper()) and note.noteBody != "") and note.archived is False and note.date > (datetime.now() - timedelta(days=maxNumberOfDaysToGoBackWhenShowingNotes)).strftime(myPreferences.datetime_format()):
            displayedNotes.append(note)
            noteIndex += 1

            if groupByProject and note.project != project:
                project = note.project
                if project == "":
                    print(f"\n{myTerminal.WHITE}no project: {project}{myTerminal.RESET}")
                else:
                    print(f"\n{myTerminal.WHITE}Project: {project}{myTerminal.RESET}")    

            print(f"\t {noteIndex:>3}) {note.title[:40]:<40} ({note.date})")
            if showActionItems:
                if note.actionItems:
                    for actionItem in note.actionItems:
                        print(f"\t\t{myTerminal.GREY}- [ ] {actionItem}{myTerminal.RESET}")
                else:
                    print(f"\t\t{myTerminal.GREY}No Action Items found.{myTerminal.RESET}")

            if noteIndex > numberOfNotesToShow:
                break  # Show only the first numberOfNotesToShow notes for brevity
        
    selectedNoteId = input(f"\n{myTerminal.INPUTPROMPT}Select a note number or press Enter to skip: {myTerminal.RESET}").strip()
    
    if not selectedNoteId.isdigit() or int(selectedNoteId) < 1 or int(selectedNoteId) > noteIndex:
        return 0, NoteData("", "", "", "", "", "", "", "", [], [], "", "", "", "", [],[], False, False)


    selectedNote = displayedNotes[int(selectedNoteId) - 1]
    return int(selectedNoteId), selectedNote
    
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
        elif templateTag.upper() in ("CHECKBOX_UNCHECKED","CHECKBOX_EMPTY", "TASK CHECKBOX"):
            templateTagValue = "- [ ]"
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
            
            if templateTag.upper() in ("ASSIGNED TO","TASK OWNER", "OWNER") and templateTagValue == "":
                templateTagValue = myPreferences.author_name()

        note_Content = note_Content.replace(f"[{templateTag}]", templateTagValue)
        
    attachmentCount = 0
    addAttachment = input(f"{myTerminal.INPUTPROMPT}Add attachment? (y/n): {myTerminal.RESET}").strip().upper()

    print("")
    while addAttachment == "Y":
        selectedFile, attachmentTagValue = select_attachment_from_user(projectName=selectedProjectName, uniqueIdentifier=timestamp_id)
        if attachmentTagValue != "":
            if attachmentCount == 0:
                note_Content += "\n\n#### Attachments\n"
            
            attachmentCount += 1
            note_Content += f"\n[{selectedFile}](./_Attachments/{attachmentTagValue})\n"
            print(f"\t\t{myTerminal.SUCCESS}Attachment added '{selectedFile}'.{myTerminal.RESET}")
            addAttachment = input(f"{myTerminal.INPUTPROMPT}Add another attachment? (y/n): {myTerminal.RESET}").strip().upper()
        else:
            print(f"\t\t{myTerminal.WARNING}No attachment selected.{myTerminal.RESET}")
            addAttachment = "N"
               
    return note_Content

def get_templateMerge_Values_From_ExistingData(templateData: Union[NoteData, dict], note_Content: str) -> tuple[str,str,str]:
    """
    Populate a note template using values from an existing NoteData object or dictionary.
    Returns the populated note content with user inputs replacing template tags.
    """
    
    note_Content = note_Content.strip()
    templateTags = re.findall(r"\[(.*?)\]", note_Content)
    templateTags = set(templateTags)  # remove duplicates
    
    # Handle both NoteData objects and dictionaries
    if isinstance(templateData, NoteData):
        date_str = templateData.date
        title = templateData.title if templateData.title else "untitled"
        selectedProjectName = templateData.project if templateData.project else ""
        tags_list = templateData.tags if templateData.tags else []
    else:  # dictionary
        date_str = templateData.get("date", datetime.now().strftime(myPreferences.datetime_format()))
        title = templateData.get("Title", "untitled")
        selectedProjectName = templateData.get("Project Name", templateData.get("project", ""))
        tags_str = templateData.get("tags", "")
        tags_list = [tag.strip() for tag in tags_str.split(",") if tag.strip()] if tags_str else []
    
    _,selectedDateTime = myTools.datetime_fromString(date_str)
    timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
    timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    
    #get title and tags captured first
    if "Title" in templateTags:
        note_Content = note_Content.replace("[Title]", title)
        templateTags.remove("Title")
    
    if "tags" in templateTags:
        if tags_list:
            # Join tags with commas if they exist
            templateTagValue = ", ".join(tags_list)
        else:
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
        else:
            # For other template tags, try to get the value from the data source
            if isinstance(templateData, NoteData):
                templateTagValue = getattr(templateData, templateTag, "")
                if not isinstance(templateTagValue, str):
                    templateTagValue = str(templateTagValue) if templateTagValue else ""
            else:  # dictionary
                templateTagValue = templateData.get(templateTag, "")

        note_Content = note_Content.replace(f"[{templateTag}]", templateTagValue)
                
    return timestamp_id, title, note_Content
