#!/usr/bin/env python3
import os
from _library import Terminal  as myTerminal, Preferences as myPreferences, Tools as myTools


todoNotes = myTools.get_Note_with_ActionItems(myPreferences.root_pkv())

if not todoNotes:
    print(f"{myTerminal.GREEN}No Action items found.{myTerminal.RESET}")
    exit(0)

index = 0    

print(f"{myTerminal.SUCCESS} {len(todoNotes)} Action items found:{myTerminal.RESET}")

projects = [note.project for note in todoNotes]
projects = list(set(projects))
projects.sort()

for project in projects:
    if project == "":
        print(f"{myTerminal.BLUE}no project{myTerminal.RESET}")
    else:
        print(f"{myTerminal.BLUE}Project: {project}{myTerminal.RESET}")
    projectNotes = [note for note in todoNotes if note.project == project]

    for note in projectNotes:
        index += 1
        print(f"\t{myTerminal.WHITE}{index:>2}. - {note.title[:40]:<40} ({note.date}){myTerminal.RESET}")
        for actionItem in note.actionItems: 
            myTerminal.printWithoutLineWrap(prefixText=f"\t\t{myTerminal.GREY} - [ ] ", textToAdd=f"{actionItem}{myTerminal.RESET}")

selected = input(f"{myTerminal.WHITE}Select note item by number (1-{index}) or press Enter to exit: {myTerminal.RESET}")

if selected.isdigit() and 1 <= int(selected) <= index:
    selectedNote = todoNotes[int(selected) - 1]
    notePathAndFile = selectedNote.filePath
    os.system(f"""{myPreferences.default_editor()} "{notePathAndFile}" """)
    