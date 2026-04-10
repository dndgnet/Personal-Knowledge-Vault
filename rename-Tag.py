#!/usr/bin/env python3

import os
import re
from datetime import datetime
from urllib.parse import quote

#my stuff
from _library import Preferences as myPreferences
from _library import Inputs as myInputs
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library import VersionControl as myVersionControl
from _library import Search as mySearch
from _library import Notes as myNotes


print(f"Select the {myTerminal.BLUE} tag {myTerminal.RESET} `that you want to rename")
oldTag = myInputs.select_tag()
newTag = input("enter the new name for the tag: ").replace("#","").strip()

if not oldTag or not newTag:
    print("invalid input, exiting")
    exit()


# for each note that includes the old tag print the line that includes the old tag
allNotes = myNotes.get_Notes_as_list(myPreferences.root_pkv(),True, True)
msg, notes = mySearch.search_tags(allNotes, oldTag)


oldTag = f"#{oldTag}"
oldTagHighlighted = f"{myTerminal.BLUE} {oldTag} {myTerminal.RESET}"

lineCount = 0
for note in notes:
    print(f"note: {note.title}")

    for line in note.frontMatter.splitlines():
        if oldTag in line:
            lineCount += 1
            print(f"\tline {lineCount}: {line.replace(oldTag, oldTagHighlighted)}")

    for line in note.noteBody.splitlines():
        if oldTag in line:
            lineCount += 1
            print(f"\tline {lineCount}: {line.replace(oldTag, oldTagHighlighted)}")

print(f"\n{myTerminal.YELLOW} {lineCount} {myTerminal.RESET} lines found with the tag {oldTagHighlighted}")
confirm = myInputs.ask_yes_no_from_user("are you sure you want to rename the tag?")
if not confirm:
    print("aborting")
    exit()


for note in notes:
    newFrontMatter = note.frontMatter.replace(oldTag, f"#{newTag}")
    newNoteBody = note.noteBody.replace(oldTag, f"#{newTag}")
    if myNotes.update_NoteFrontMatterAndBody(note, newFrontMatter, newNoteBody):
        print(f"updated note: {note.title}")
    else:
        print(f"failed to update note: {note.title}")
    