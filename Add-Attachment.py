#!/usr/bin/env python3

from _library import Tools as myTools, Preferences as myPreferences, Terminal as myTerminal
import os

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
        pass  # Skip hidden files
    
    fileIndex += 1
    print(f"\t{myTerminal.INPUTPROMPT}{fileIndex}: {file_name}{myTerminal.RESET}")
    if fileIndex > 20:
        print(f"\t\t{myTerminal.YELLOW}only showing the first 20.{myTerminal.RESET}")
        break

if fileIndex == 0:
    print(f"{myTerminal.ERROR}No files found in the attachment pick up folder.{myTerminal.RESET}")
    exit(1)    

#select a file
input_string = input(f"{myTerminal.INPUTPROMPT}Select a file (1-{fileIndex}):{myTerminal.RESET} ")
if input_string.isdigit() and 1 <= int(input_string) <= fileIndex:
    selected_file = list(downloads_dict.keys())[int(input_string) - 1]
    sourcefile_path = os.path.join(downloads_folder, selected_file)

    print(f"{myTerminal.INPUTPROMPT}Available projects:{myTerminal.RESET} ")
    projectIndex = 0
    print(f"\t{myTerminal.INPUTPROMPT}{projectIndex}: No Project (use PKV root){myTerminal.RESET}")
    for key, value in myTools.get_pkv_projects().items():
        projectIndex += 1
        print(f"\t{myTerminal.INPUTPROMPT}{projectIndex}: {key}{myTerminal.RESET}")
    selectedProject = input(f"{myTerminal.INPUTPROMPT}Select a project (1-{projectIndex}):{myTerminal.RESET} ")        
    if selectedProject.isdigit() and 0 <= int(selectedProject) <= projectIndex:
        if int(selectedProject) == 0:
            # No project selected, use PKV root
            destination_path = myPreferences.root_attachments()
        else:
            # Use the selected project
            destination_path = os.path.join(myPreferences.root_projects(),
                                            list(myTools.get_pkv_projects().keys())[int(selectedProject) - 1],
                                            "_Attachments")
    else:
        print(f"{myTerminal.ERROR}Invalid project selection.{myTerminal.RESET}")
        exit(1)
        
    # Move the file to the attachments root
    if not os.path.exists(destination_path):
        os.makedirs(destination_path)
    destination_path = os.path.join(destination_path, selected_file)
    
    if os.path.exists(destination_path):
        input_replace = input(f"{myTerminal.ERROR}Replace the existing '{selected_file}' in the attachments (Y/N)?{myTerminal.RESET}").strip().upper()
        if input_replace != 'Y':
            print(f"{myTerminal.YELLOW}File '{selected_file}' not moved.{myTerminal.RESET}")
            exit(1)
    
    os.rename(sourcefile_path, destination_path)
    #print(f"{myTools.GREEN}File '{selected_file}' moved to attachments.{myTerminal.RESET}")
    print(f"\t{myTerminal.SUCCESS}moved file to PKV, use  \n \t\t[{selected_file}]({selected_file}) \n\tas a back link in notes.{myTerminal.RESET}")
    