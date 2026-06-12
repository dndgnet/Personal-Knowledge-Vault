#!/usr/bin/env python3
import os
from _library import Terminal  as myTerminal, Preferences as myPreferences, Notes as myNotes


todoNotes = myNotes.get_Note_with_ActionItems(myPreferences.root_pkv())

if not todoNotes:
    print(f"{myTerminal.GREEN}No Action items found.{myTerminal.RESET}")
    exit(0)

filterOwner = input(f"{myTerminal.WHITE}Filter by owner (leave blank for all): {myTerminal.RESET}").strip().lower()
filterDueDate = input(f"{myTerminal.WHITE}Filter by due date (YYYY-MM-DD, leave blank for today or late): {myTerminal.RESET}").strip()

#sort notes by project name 
todoNotes.sort(key=lambda x: (x.project.lower(), x.date))

if filterOwner:
    filterNotes = []
    for note in todoNotes:
        for actionItem in note.actionItems:
            actionOwner = actionItem.Owner.strip().lower()
            if actionOwner == filterOwner:
                filterNotes.append(note)
                break
            
    todoNotes = filterNotes

if filterDueDate:
    filterNotes = []
    for note in todoNotes:
        for actionItem in note.actionItems:
            actionDate = actionItem.Date.strip()    
            if actionDate <= filterDueDate:
                filterNotes.append(note)
                break
            
    todoNotes = filterNotes

selected = "start"
if len(todoNotes) == 0:
    print(f"{myTerminal.GREEN}No Action items found with the specified filters.{myTerminal.RESET}")
    exit(0)
    
while selected.lower() != "stop":
    print(f"{myTerminal.SUCCESS} {len(todoNotes)} Action items found:{myTerminal.RESET}")
    
    index = 0    
    project = None
    for note in todoNotes:
        if note.project != project:
            project = note.project
            if project == "":
                print(f"{myTerminal.BLUE}no project{myTerminal.RESET}")
            else:
                print(f"{myTerminal.BLUE}Project: {project}{myTerminal.RESET}")
        
        index += 1
        print(f"\t{myTerminal.WHITE}{index:>2}. - {note.title[:40]:<40} ({note.date}){myTerminal.RESET}")
        for actionItem in note.actionItems: 
            myTerminal.printWithoutLineWrap(prefixText=f"\t\t{myTerminal.GREY} - [ ] ", textToAdd=f"{actionItem}{myTerminal.RESET}") 

    selected = input(f"{myTerminal.WHITE}Select note item by number (1-{index}) or press Enter or 'q' to exit: {myTerminal.RESET}")

    if selected.isdigit() and 1 <= int(selected) <= index:
        selectedNote = todoNotes[int(selected) - 1]
        notePathAndFile = selectedNote.filePath
        os.system(f"""{myPreferences.default_editor()} "{notePathAndFile}" """)
    else:
        selected = "stop"