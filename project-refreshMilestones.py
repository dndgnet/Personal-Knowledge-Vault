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
for arg in sys.argv[1:]:
    if arg.startswith("--project="):
        selectedProject = arg.split("=")[1]
        silentMode = True


print(
    f"{myTerminal.INFORMATION}Refresh Milestone note{myTerminal.RESET}\n"
)
print("")

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

hasMilestone = False
milestoneNote = myNotes.blankNoteData()

for note in projectNotes:
    if note.type.lower().endswith("milestones"):
        hasMilestone = True
        milestoneNote = note
        break

if not hasMilestone:
    print(f"{myTerminal.WARNING}No milestone note found for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

table = "|Title|Planned Date|Actual Date|\n|------------|-----------|-----|\n"

plannedString = "\tsection Planned\n"
actualString = "\tsection Actual\n"
plannedCounter = 0
actualAndPlannedAreTheSame = True

for note in projectNotes:
    if note.isMilestone:
        plannedIsDate, plannedDate = myTools.datetime_fromString(note.plannedDate)
        actualIsDate, actualDate = myTools.datetime_fromString(note.actualDate)
        if plannedIsDate:
            plannedCounter += 1
            table += f"|{note.title}|{myTools.format_datetimeAsPreferred_Date_String(plannedDate)}|{myTools.format_datetimeAsPreferred_Date_String(actualDate) if actualIsDate else ''}|\n"
            style = "milestone"
            if actualIsDate:
                if actualDate <= plannedDate:
                    style = "milestone"
                else:
                    style = "done"
                    actualAndPlannedAreTheSame = False
            else:
                style = "crit"
                actualAndPlannedAreTheSame = False

            plannedString += f"\t{myTools.letters_and_numbers_only(note.title)} : {style}, p{plannedCounter}, {myTools.format_datetimeAsPreferred_Date_String(plannedDate)}, 1d\n"
        if actualIsDate:
            style = "milestone"
            if actualDate <= plannedDate:
                    style = "milestone"
            else:
                style = "done"

            actualString += f"\t{myTools.letters_and_numbers_only(note.title)} : {style}, a{plannedCounter}, {myTools.format_datetimeAsPreferred_Date_String(actualDate)}, 1d\n"

if plannedCounter == 0:
    print(f"{myTerminal.WARNING}No planned dates found for milestone notes in project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

if actualAndPlannedAreTheSame:
    print(f"{myTerminal.INFORMATION}All actual milestone dates are the same as planned dates.{myTerminal.RESET}")
    plannedString = ""
else:
    
    if not myInputs.ask_yes_no_from_user("Show planned baseline for milestones?", True):
        plannedString = "" 


gantt = f"""
```mermaid
---
config:
  theme: 'forest'
---

gantt
    title       Timeline
    dateFormat  YYYY-MM-DD
    axisFormat  %b-%d
    excludes    weekends

{plannedString}

{actualString}

```
"""
print(gantt)

if myInputs.ask_yes_no_from_user("Show gantt diagram?", True):    
    milestoneContent = f"\n{gantt}\n\n{myTools.divTagSmall}\n\n{table}\n\n{myTools.divTagEnd}\n\n"
else:
    milestoneContent = f"\n{myTools.divTagSmall}\n\n{table}\n\n{myTools.divTagEnd}\n\n"

if milestoneNote is not None:
    success, newNoteBody = myNotes.replace_text_between_tags("milestones", milestoneNote.noteBody, milestoneContent)
    if success:
        myNotes.update_NoteBody(milestoneNote, newNoteBody)

myTools.open_note_in_editor(milestoneNote.filePath)