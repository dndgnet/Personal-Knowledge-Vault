#!/usr/bin/env python3
import os
from _library import Terminal  as myTerminal, Preferences as myPreferences, Tools as myTools

todo = myTools.get_Note_with_ActionItems(myPreferences.root_pkv())

if not todo:
    print(f"{myTerminal.GREEN}No Action Items found.{myTerminal.RESET}")
    exit(0)

index = 0    
print(f"{myTerminal.SUCCESS} {len(todo)} Notes with Action Items found:{myTerminal.RESET}")
for key, value in todo.items():
    index += 1
    title = value.get("title", "No Title")
    noteDate = value.get("date", "Unknown Date")
    print(f"\t{myTerminal.WHITE}{index:>2}) {title} {myTerminal.GREY}({noteDate}) {myTerminal.RESET}")

selected = input(f"{myTerminal.BLUE}Select note by number (1-{index}) or press Enter to exit: {myTerminal.RESET}")

if selected.isdigit() and 1 <= int(selected) <= index:
    selected_key = list(todo.keys())[int(selected) - 1]
    notePathAndFile = todo[selected_key].get("notePathAndFile", "")
    os.system(f"""{myPreferences.default_editor()} "{notePathAndFile}" """)
    