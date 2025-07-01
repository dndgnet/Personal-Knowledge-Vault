# #!/usr/bin/env python3
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 
 
_,selectedProject, _ = myInputs.select_project_name()

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
        print("debug project is a note",note.title)


# find the latest status update note, put it at the top of the output

# for the rest of items build a timeline in descending order of date


for note in notes:
    print(f"{myTerminal.INFORMATION}{note.date:<20} {note.project[:30]:<31} {note.title[:30]:<31}{myTerminal.RESET}")