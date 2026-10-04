#!/usr/bin/env python3

import os
import sys 

from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Terminal as myTerminal
from _library import Tools as myTools

myTerminal.clearTerminal()

selectedProject = ""
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        selectedProject += arg + " "
    selectedProject = selectedProject.strip()
    print(f"Using project from arguments: '{selectedProject}'")

print(f"{myTerminal.INFORMATION}Generate AI Context File{myTerminal.RESET}\n")

if selectedProject == "":
    print("Available target projects:")
    selectedProject = myInputs.select_project_name(False, False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    sys.exit(1)

print(f"Generating AI Context File for project: {selectedProject}")

# Load all notes for the project
allNotes = myNotes.get_Notes_from_Project(selectedProject)

if not allNotes:
    print(f"{myTerminal.WARNING}No notes found for project '{selectedProject}'.{myTerminal.RESET}")
    sys.exit(1)

# Sort notes by date (oldest first)
sortedNotes = myNotes.sort_Notes_by_date(allNotes, descending=False)

# Find executive summary if it exists (move to top)
executiveSummaryNote = None
regularNotes = []
for note in sortedNotes:
    if note.typeSimple.lower() == "executive_summary" or "executive_summary" in note.type.lower():
        executiveSummaryNote = note
    else:
        regularNotes.append(note)

# Reassemble list with executive summary at the top if present
orderedNotes = []
if executiveSummaryNote:
    orderedNotes.append(executiveSummaryNote)
    print(f"{myTerminal.SUCCESS}Found executive summary note - placing at top.{myTerminal.RESET}")
orderedNotes.extend(regularNotes)

# Build the AI Context File content
contextContent = f"""# AI Context File for {selectedProject}

**Generated**: {myTools.now_YYYY_MM_DD_HH_MM_SS() if hasattr(myTools, 'now_YYYY_MM_DD_HH_MM_SS') else 'now'}
**Total notes**: {len(orderedNotes)}
**Order**: Executive Summary (if present) first, then chronological by note.date

---

"""

for note in orderedNotes:
    note_date = note.date[:10] if len(note.date) >= 10 else note.date
    contextContent += f"""## {note_date} - {note.title}

**Type**: {note.type}
**ID**: {note.id}

{note.noteBody.strip()}

---

"""
    
# Write to project folder
projectPath = os.path.join(myPreferences.root_projects(), selectedProject)
contextFilePath = os.path.join(projectPath, "AI Context File.md")

# Ensure project directory exists
os.makedirs(projectPath, exist_ok=True)

success = myTools.write_text_to_file(contextFilePath, contextContent)

if success:
    print(f"{myTerminal.SUCCESS}Successfully created/updated: {contextFilePath}{myTerminal.RESET}")
    print(f"   - {len(orderedNotes)} notes included")
    if executiveSummaryNote:
        print(f"   - Executive summary placed at top")
    myTools.open_note_in_editor(contextFilePath)
else:
    print(f"{myTerminal.ERROR}Failed to write AI Context File.{myTerminal.RESET}")
    sys.exit(1)

print(f"\n{myTerminal.INFORMATION}AI Context File ready for use with LLMs or other tools.{myTerminal.RESET}")
