#!/usr/bin/env python3
import os
from _library import Terminal  as myTerminal, Preferences as myPreferences, Tools as myTools


todoNotes = myTools.get_Note_with_INCOMPLETE(myPreferences.root_pkv())

if not todoNotes:
    print(f"{myTerminal.GREEN}No INCOMPLETE items found.{myTerminal.RESET}")
    exit(0)

index = 0    
print(f"{myTerminal.SUCCESS} {len(todoNotes)} INCOMPLETE items found:{myTerminal.RESET}")
for note in todoNotes:
    index += 1
    print(f"\t{myTerminal.BLUE}{index:>2}. - {note.title} ({note.date}){myTerminal.RESET}")

selected = input(f"{myTerminal.BLUE}Select note item by number (1-{index}) or press Enter to exit: {myTerminal.RESET}")

if selected.isdigit() and 1 <= int(selected) <= index:
    selectedNote = todoNotes[int(selected) - 1]
    notePathAndFile = selectedNote.filePath
    os.system(f"""{myPreferences.default_editor()} "{notePathAndFile}" """)
    