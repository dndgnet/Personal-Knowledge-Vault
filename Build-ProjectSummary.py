#!/usr/bin/env python3

import os 
import datetime

from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 


print(f"{myTerminal.INFORMATION}Prepare a project summary...{myTerminal.RESET}\n")

print("Available projects:") 
_,selectedProject, _ = myInputs.select_project_name_withDict()

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)
    
notesAll = myTools.get_Notes_as_list(myPreferences.root_pkv())
notes = []

for note in notesAll:
    if note.project == selectedProject:
        notes.append(note)
    elif f"p_{selectedProject}" in note.tags:
        notes.append(note)
        print("debug project is a note", note.title)

notes = myTools.sort_Notes_by_date(notes, descending=True)

includeBodyInTimeline = myInputs.ask_yes_no("Include body in timeline?", default=False)
includeBackLinkInTimeline = myInputs.ask_yes_no("Include backlinks in timeline?", default=False)
includeGannt = myInputs.ask_yes_no("Include Gantt chart?", default=False)
 

progressBody = ""
timeLine = ""
gantt = ""

for note in notes:
    note: NoteData = note  # type hint for better IDE support
    
    # find the latest status update note, put it at the top of the output
    if progressBody == "" and (note.type == "progress" or note.type == "project-progress"):
        progressBody = myTools.remove_noteHeaders(note.noteBody)
        print(f"{myTerminal.SUCCESS}Found progress note: {note.title}{myTerminal.RESET}")
    
    # for the rest of items build a timeline in descending order of date
    if not includeBackLinkInTimeline and not includeBodyInTimeline:
        timeLine += f"\n- {note.date} {note.type} {note.title}\n"
    else:
        timeLine += f"\n### {note.date} {note.type} {note.title}\n"
        
    if includeBodyInTimeline:
        timeLine += f"\n{myTools.remove_noteHeaders(note.noteBody)}\n"

    if includeBackLinkInTimeline:
        timeLine += f"\n[[{note.id}]]\n"
    
    if includeGannt: 
        gantt += f"{ myTools.letters_and_numbers_only(note.title)} : {note.date}, 1d\n"

    #debug
    #print(f"{myTerminal.INFORMATION}{note.date:<20} {note.project[:30]:<31} {note.title[:30]:<31}{myTerminal.RESET}")

if includeGannt:
    gantt = f"""
    

```mermaid

gantt
    title {selectedProject}
    dateFormat YYYY-MM-DD
    section Timeline

        {gantt}
    
```
"""


summary = f"""
# {selectedProject} Project Summary\n\n

prepared: {datetime.datetime.now().strftime(myPreferences.date_format())}

## Progress

{progressBody}

## Timeline
{timeLine}

{gantt}

"""

# use the dot prefix to hide the file in the project directory (at least in civilized file managers)
output_path = os.path.join(myPreferences.root_projects(), selectedProject, ".ProjectSummary.md")

if os.path.exists(output_path):
    print(f"{myTerminal.WARNING}Project summary already exists: {output_path}{myTerminal.RESET}")
    if not myInputs.ask_yes_no("Do you want to overwrite it?", default=True):
        print(f"{myTerminal.INFORMATION}Exiting without changes.{myTerminal.RESET}")
        exit(0)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(summary)
    
os.system(f'{myPreferences.default_editor()} "{output_path}"')    