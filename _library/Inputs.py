""" 
Collect inputs from users for specific tasks.
"""

from . import Preferences as myPreferences
from . import Tools as myTools
from . import Terminal as myTerminal

import os
from datetime import datetime

# Define the template and output paths
template_pathRoot = os.path.join(os.getcwd(),"_templates")

def get_datetime_from_user(prompt = "enter a date time", defaultIfNone = datetime.now()) -> datetime:
    """
    Get a datetime from the user.
    returns the default datetime if the user doesn't provide a valid datetime
    for example, if the user enters an empty string
    """
    inputDate = input(f"{myTerminal.INPUTPROMPT}{prompt}{myTerminal.RESET}").strip()
    isDateTime, d = myTools.datetime_fromString(inputDate)
    if not isDateTime:
        print(f"\t{myTerminal.YELLOW}Using default: {defaultIfNone.strftime(myPreferences.datetime_format())}{myTerminal.RESET}")
        return defaultIfNone
    else:
        return d 
    
def get_project_name() -> tuple[dict,str, int]:
    """Get the project name from the user.
        exits if the user does not select a valid project
    """
    projectIndex = 1
    projects = {}

    #let hte user pic which project to use
    print(f"{myTerminal.INPUTPROMPT}Available projects:{myTerminal.RESET}")
    projectIndex = 0
    projects[projectIndex] = "No Project"
    print(f"\t{projectIndex}. {projects.get(1, 'No Project')}")
    projectIndex = 1
    projects[projectIndex] = "New Project"
    print(f"\t{projectIndex}. {projects.get(1, 'New Project')}")


    for filename in sorted(os.listdir(myPreferences.root_projects())):
        if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
            projectIndex += 1
            print(f"\t{projectIndex}. {filename}")
            projects[projectIndex] = filename

    selectedProject = input(f"Select a project (0-{projectIndex}): ")

    if not selectedProject.isdigit() or int(selectedProject) not in projects:
        print(f"{myTerminal.ERROR}Invalid selection. Please select a valid project number.{myTerminal.RESET}")
        exit(1)

    if int(selectedProject) == 0:
        print(f"{myTerminal.ERROR}Not yet implemented, I haven't decided what to do with no project calls. Exiting.{myTerminal.RESET}")
        exit(1)

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
        
        
    return projects, projects[int(selectedProject)], int(selectedProject)

def get_template(templateType = "All") -> tuple[dict,str, int]:
    """ 
        Get the template from the user.
        exits if the user does not select a valid template
    """  
    
    templateIndex = 1
    templates = {}
    print(f"{myTerminal.INPUTPROMPT}Available templates:{myTerminal.RESET}")
    for filename in os.listdir(template_pathRoot):
        if filename.upper().startswith(f"{templateType.upper()}_") or templateType.upper() in ("ALL",""):
            print(f"""\t{templateIndex}. {filename.replace(f"{templateType}_",f"{templateType} ")}""")
            templates[templateIndex] = filename
            templateIndex += 1
        
    selectedTemplate = input(f"Select a template (1-{len(templates)}): ")

    if not selectedTemplate.isdigit() or int(selectedTemplate) not in templates:
        print(f"{myTerminal.ERROR}Invalid selection. Please select a valid template number.{myTerminal.RESET}")
        exit(1)

    return templates, templates[int(selectedTemplate)], int(selectedTemplate)