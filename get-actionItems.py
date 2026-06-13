#!/usr/bin/env python3
import os
from _library import Terminal  as myTerminal, Preferences as myPreferences, Notes as myNotes

todoNotes = myNotes.get_Note_with_ActionItems(myPreferences.root_pkv())

filterProject = input(f"{myTerminal.WHITE}Filter by project name (leave blank for all): {myTerminal.RESET}").strip().lower()
filterOwner = input(f"{myTerminal.WHITE}Filter by owner (leave blank for all): {myTerminal.RESET}").strip().lower()
filterDueDate = input(f"{myTerminal.WHITE}Filter by due date (YYYY-MM-DD, leave blank for no date filter): {myTerminal.RESET}").strip()
if len(filterDueDate) == 4:
    #they probably entered a year, so add the current month and day to make it a valid date string 
    filterDueDate += "-00-00"
elif len(filterDueDate) == 7:
    #they probably entered a year and month, so add the current day to make it a valid date string 
    filterDueDate += "-00"

if not todoNotes:
    print(f"{myTerminal.GREEN}No Action items found.{myTerminal.RESET}")
    exit(0)

#sort notes by project name 
todoNotes.sort(key=lambda x: (x.project.lower(), x.date))

if filterProject:
    todoNotes = [note for note in todoNotes if  filterProject in note.project.lower()]

actionItemList = []
for note in todoNotes:
    for actionItem in note.actionItems:
        actionOwner = actionItem.Owner.strip().lower()
        if (filterOwner == "" or  filterOwner == actionOwner) and \
           (filterDueDate == "" or actionItem.Date.strip() <= filterDueDate):
            #keep this action item
            actionItemList.append(actionItem)

del todoNotes

actionItemList.sort(key=lambda x: (x.project.lower(),x.Owner.lower(),  x.Date))

selected = "start"
while selected.lower() != "stop":
    myTerminal.clearTerminal()
    print(f"{myTerminal.SUCCESS} {len(actionItemList)} Action items found:{myTerminal.RESET}")
    index = 0    
    project = None
    noteId = None
    noteTitle = None
    for actionItem in actionItemList:
        if actionItem.project != project:
            project = actionItem.project
            if project == "":
                print(f"{myTerminal.BLUE}no project{myTerminal.RESET}")
            else:
                print(f"{myTerminal.BLUE}Project: {project}{myTerminal.RESET}")
        
        index += 1
        if actionItem.note_id != noteId:
            noteId = actionItem.note_id
            noteTitle = actionItem.note_title
            if len(noteTitle) > 40:
                print(f"\t{myTerminal.GREY}Note: {noteTitle[:40]:<40}...{myTerminal.RESET}")
            else:
                print(f"\t{myTerminal.GREY}Note: {noteTitle[:40]:<40}{myTerminal.RESET}")

        dateString = f" (Due: {actionItem.Date})" if actionItem.Date else ""
        myTerminal.printWithoutLineWrap(prefixText=f"\t\t{myTerminal.WHITE}{index:>2} ", textToAdd=f"{actionItem}{myTerminal.RESET}") 
        
        if actionItem.Comment:
            if len(actionItem.Comment) > 40:
                print(f"\t\t\t{myTerminal.GREY}  - Comment: {actionItem.Comment[:40]:<40}...{myTerminal.RESET}")
            else:
                print(f"\t\t\t{myTerminal.GREY}  - Comment: {actionItem.Comment[:40]:<40}{myTerminal.RESET}")


    selected = input(f"\n{myTerminal.WHITE}Select note item by number (1-{index}) or press Enter or 'q' to exit: {myTerminal.RESET}")

    if selected.isdigit() and 1 <= int(selected) <= index:
        selectedActionItem = actionItemList[int(selected) - 1]
        notePathAndFile = selectedActionItem.note_path
        if myPreferences.default_editor() == "code":    
            cmdString = f"""{myPreferences.default_editor()}  --goto "{notePathAndFile}:{selectedActionItem.noteRow}" """
        else:
            cmdString = f"""{myPreferences.default_editor()} "{notePathAndFile}" """
        os.system(cmdString)
    elif selected.lower().startswith("done "):
        selectedActionItem = selected.replace("done ", "").strip()
        if selectedActionItem.isdigit() and 1 <= int(selectedActionItem) <= index:
            selectedActionItem = actionItemList[int(selectedActionItem) - 1]
            selectedActionItem.Complete()
            print(f"{myTerminal.GREEN}Marked as completed: {selectedActionItem}{myTerminal.RESET}")
            input("Press Enter to continue...")
    else:
        selected = "stop"