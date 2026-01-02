#!/usr/bin/env python3

import os
from pathlib import Path
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 

myTerminal.clearTerminal()
print(f"{myTerminal.INFORMATION}Import and Update Project Tasks{myTerminal.RESET}\n")
print("Select the target project then select the CSV file (exported from Jira, DevOps, Trello, etc.) from your downloads folder")

print("Available target projects:") 
selectedProject = myInputs.select_project_name(False,False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

#display a list of the files CSV files in the download folder and the user select which file to 
#import and use as a project task update source
downloads_folder = Path(myPreferences.attachmentPickUp_path())
csv_files = {}
index = 1
for file in downloads_folder.glob("*.csv"):
    csv_files[index] = file.name
    print(f"{index}. {file.name}")
    index += 1

if not csv_files:
    print(f"{myTerminal.WARNING}No CSV files found in Downloads folder.{myTerminal.RESET}")
    exit(1)

file_choice = myInputs.ask_for_list_selection_from_user("Select a CSV file to import and update project tasks:", csv_files, no_selection_made_value=-99)
if file_choice == -99 or file_choice is None:
    print(f"{myTerminal.WARNING}No CSV file selected.{myTerminal.RESET}")
    exit(1)

file = os.path.join(downloads_folder, csv_files[file_choice])
myTerminal.clearTerminal()
myProjects.import_or_update_tasks_from_CSV(file, selectedProject)    