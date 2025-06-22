""" 
Collect inputs from users for specific tasks.
"""

from . import Preferences as myPreferences
from . import Tools as myTools

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
    inputDate = input(f"{myTools.BLUE}{prompt}{myTools.RESET}").strip()
    isDateTime, d = myTools.datetime_fromString(inputDate)
    if not isDateTime:
        print(f"\t{myTools.YELLOW}Using default: {defaultIfNone.strftime(myPreferences.datetime_format())}{myTools.RESET}")
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
    print(f"{myTools.BLUE}Available projects:{myTools.RESET}")
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
        print(f"{myTools.RED}Invalid selection. Please select a valid project number.{myTools.RESET}")
        exit(1)

    if int(selectedProject) == 0:
        print(f"{myTools.RED}Not yet implemented, I haven't decided what to do with no project calls. Exiting.{myTools.RESET}")
        exit(1)

    if int(selectedProject) == 1:
        newProjectName = input(f"{myTools.BLUE}Enter a new project name: {myTools.RESET}").strip()
        if not newProjectName:
            print(f"{myTools.RED}Project name cannot be empty.{myTools.RESET}")
            exit(1)
        newProjectPath = os.path.join(myPreferences.root_projects(), f"Project {newProjectName}")
        os.makedirs(newProjectPath, exist_ok=True)
        selectedProject = projectIndex + 1
        projects[selectedProject] = f"Project {newProjectName}"
        print(f"{myTools.GREEN}New project created: {newProjectPath}{myTools.RESET}")
        
        
    return projects, projects[int(selectedProject)], int(selectedProject)

def get_template(templateType = "All") -> tuple[dict,str, int]:
    """ 
        Get the template from the user.
        exits if the user does not select a valid template
    """  
    
    templateIndex = 1
    templates = {}
    print(f"{myTools.BLUE}Available templates:{myTools.RESET}")
    for filename in os.listdir(template_pathRoot):
        if filename.upper().startswith(f"{templateType.upper()}_") or templateType.upper() in ("ALL",""):
            print(f"\t{templateIndex}. {filename.replace(f"{templateType}_",f"{templateType} ")}")
            templates[templateIndex] = filename
            templateIndex += 1
        
    selectedTemplate = input(f"Select a template (1-{len(templates)}): ")

    if not selectedTemplate.isdigit() or int(selectedTemplate) not in templates:
        print(f"{myTools.RED}Invalid selection. Please select a valid template number.{myTools.RESET}")
        exit(1)

    return templates, templates[int(selectedTemplate)], int(selectedTemplate)