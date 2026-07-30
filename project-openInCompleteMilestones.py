#!/usr/bin/env python3

import os
import sys
import shutil

from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Projects as myProjects
from _library import Terminal as myTerminal
from _library import Tools as myTools

myTerminal.clearTerminal()
selectedProject: str = ""
silentMode: bool = False

#get selected project from command line argument if provided
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        selectedProject += arg + " "
    selectedProject = selectedProject.strip()
    silentMode = True
    print (f"'{selectedProject}'")


print(
    f"{myTerminal.INFORMATION}Open Incomplete Milestone Notes{myTerminal.RESET}\n"
)
print()

# debug
#selectedProject = "Adaptive Project Management Software"

if selectedProject == "":
    print("Available target projects:")
    selectedProjectInput = myInputs.select_project_name(False, False)
    if selectedProjectInput is not None:
        selectedProject = selectedProjectInput

if selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

projectConfig = myProjects.get_ProjectConfig_as_dict(selectedProject)

projectNotes = myNotes.get_Notes_from_Project(selectedProject)
projectNotes.sort(key=lambda note: myTools.datetime_fromString(note.plannedDate)[1])

notesToOpen = []
for note in projectNotes:
    if note.isMilestone and note.actualDate == "":
        notesToOpen.append(note)

if not notesToOpen:
    print(f"{myTerminal.WARNING}No incomplete milestone notes found for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

myTools.open_vault()
for note in notesToOpen:
    myTools.open_note_in_editor(note.filePath)