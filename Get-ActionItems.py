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
    frontMatter = value.get("frontMatter", "")
    title = myTools.get_stringValue_from_frontMatter("Title",frontMatter)
    noteDate = myTools.get_note_date_from_frontMatter(frontMatter)
    print(f"\t{myTerminal.BLUE}{index:>2}. {key}{myTerminal.RESET} - {title} ({noteDate})")

selected = input(f"{myTerminal.BLUE}Select note by number (1-{index}) or press Enter to exit: {myTerminal.RESET}")

if selected.isdigit() and 1 <= int(selected) <= index:
    selected_key = list(todo.keys())[int(selected) - 1]
    notePathAndFile = todo[selected_key].get("notePathAndFile", "")
    os.system(f"""{myPreferences.default_editor()} "{notePathAndFile}" """)
    