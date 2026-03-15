#!/usr/bin/env python3

import os
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Preferences as myPreferences
from _library import Tools as myTools
from _library import Inputs as myInputs 
from _library import Notes as myNotes

myTerminal.clearTerminal()
selectedProject = None

print(f"{myTerminal.INFORMATION}Edit Project Data{myTerminal.RESET}\n")
print("")


#debug
#selectedProject = "Legal Services Request App 2026 Enhancements"

if selectedProject is None or selectedProject == "":
    print("Available target projects:") 
    selectedProject = myInputs.select_project_name(False,False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

#select the type of project data to edit
success, dataTypeSelection = myInputs.select_dictionary_Item_from_user("Select the type of project data to edit:", myProjects.dataTypeDictionary)

if not success:
    print(f"{myTerminal.WARNING}No data type selected.{myTerminal.RESET}")
    exit(1)

myProjects.open_ProjectData_in_Editor(selectedProject, dataTypeSelection)
