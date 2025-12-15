#!/usr/bin/env python3

from _library import Preferences as myPreferences, Terminal as myTerminal, Inputs as myInputs, VersionControl as myVersionControl
import os
import datetime

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
    exit(1)    

#select a file
input_string = input(f"{myTerminal.INPUTPROMPT}Select a file (1-{fileIndex}):{myTerminal.RESET} ")
if input_string.isdigit() and 1 <= int(input_string) <= fileIndex:
    selected_file = fileList[int(input_string) - 1]
    sourcefile_path = os.path.join(downloads_folder, selected_file)

    selectedNoteId, selectedNote = myInputs.select_recent_note(noteTypeContains="Any", showActionItems = False)

    if selectedNoteId != 0:
        selectedProject = selectedNote.project
    else:
        selectedProject = myInputs.select_project_name(showNewProjectOption=False)

    destination_path = ""
    if selectedProject is not None and selectedProject != "":
        # Use the selected project
        destination_path = os.path.join(myPreferences.root_projects(),
                                        selectedProject,
                                        "_Attachments")
    else:
        # No project selected, use PKV root
        destination_path = myPreferences.root_attachments()

    if os.path.exists(destination_path) is False:
        os.makedirs(destination_path, exist_ok=True)

    # Move the file to the attachments root
    selected_fileDisplayName = selected_file.split(".")[0]
    attachment_file_name = f"""{datetime.datetime.now().strftime(myPreferences.timestamp_id_format())}_{selected_file.replace(" ", "_").replace("/", "_")}"""
    destination_path = os.path.join(destination_path, attachment_file_name)
    
    if os.path.exists(destination_path):
        input_replace = input(f"{myTerminal.ERROR}Replace the existing '{selected_file}' in the attachments (Y/N)?{myTerminal.RESET}").strip().upper()
        if input_replace != 'Y':
            print(f"{myTerminal.YELLOW}File '{selected_file}' not moved.{myTerminal.RESET}")
            exit(1)
    
    os.rename(sourcefile_path, destination_path)
    myVersionControl.add_and_commit(destination_path, message=f"Added attachment '{selected_fileDisplayName}' to '{selectedNote.title}' note.")
    print(f"\t{myTerminal.SUCCESS}moved file to '{destination_path}'{myTerminal.RESET}")

    newNoteBody = selectedNote.noteBody
    if selectedNoteId != 0:
        if "### Attachments" not in selectedNote.noteBody:
            newNoteBody +=  "\n\n\n### Attachments\n\n"
        
        newNoteBody += f"""\n\n[{selected_file}](./_Attachments/{attachment_file_name})\n"""

        _ = input(f"{myTerminal.WARNING} Make sure you have saved the note '{selectedNote.title}' before continuing (pressing enter).{myTerminal.RESET}")
        
        # Save the fleeting note with the new atomic thought link
        with open(selectedNote.filePath, 'w', encoding='utf-8') as f:
            f.write(f"""---\n{selectedNote.frontMatter}\n---\n\n {newNoteBody}""")
        print(f"\t{myTerminal.SUCCESS}moved file to PKV, and attached to '{selectedNote.title}' note as a link.{myTerminal.RESET}")
        os.system(f'{myPreferences.default_editor()} "{selectedNote.filePath}"')
        myVersionControl.add_and_commit_all(message=f"'{selected_fileDisplayName}' link added to '{selectedNote.title}' note.")

    else:
        #print(f"{myTools.GREEN}File '{selected_file}' moved to attachments.{myTerminal.RESET}")
        print(f"\t{myTerminal.SUCCESS}moved file to PKV, use  \n \t\t[{selected_file}]({selected_file}) \n\tas a back link in notes.{myTerminal.RESET}")
    