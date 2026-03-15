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

print(f"{myTerminal.INFORMATION}Build Project Burndown Visualization{myTerminal.RESET}\n")
print("")


#debug
#selectedProject = "Legal Services Request App 2026 Enhancements"

if selectedProject is None or selectedProject == "":
    print("Available target projects:") 
    selectedProject = myInputs.select_project_name(False,False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

#get the hub note for the selected project 
hubNoteFound, hubNote = myNotes.get_Note_Last_Project_Note_ByType(selectedProject, "project-hub")

if not hubNoteFound:
    print(f"{myTerminal.WARNING}No hub note found for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

"""
<!--Start_BurnDown-->

<!--End_BurnDown-->
"""

burnDownVisualization = myProjects.diagram_Burndown(selectedProject)

success, newNoteBody = myNotes.replace_text_between_tags("BurnDown", hubNote.noteBody, burnDownVisualization)

# replace the content between the <!--StartBurnDown--> and <!--EndBurnDown--> tags in the hub note with the new burn down visualization
if success:
    hubNote.noteBody = newNoteBody
    myNotes.update_NoteBody(hubNote, newNoteBody)
else:
    print(f"{myTerminal.WARNING}BurnDown tags not found in hub note for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

 
myTools.open_note_in_editor(hubNote.filePath)