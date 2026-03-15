#!/usr/bin/env python3
import datetime 
import os 

from _library import Preferences as myPreferences, Tools as myTools, Terminal as myTerminal, Inputs as myInputs, HTML as myHTML, Summary as mySummary
from _library import Search as mySearch
from _library import Notes as myNotes
import sys

# build a dictionary of all notes in the root_pkv directory
allNotes = myTools.get_Notes_as_list(myPreferences.root_pkv(),includePrivateNotes=True, includeArchivedProjects=True)
if not myNotes.dump_notes_to_json(notes=allNotes, file_path=os.path.join(myPreferences.root_pkv(), "AllNotes.json"), indent=4):
    print(f"{myTerminal.ERROR}Failed to create AllNotes.json.{myTerminal.RESET}")
    exit(-1)

#retrieve the dictionary of all notes from AllNotes.json
allNotes = []
allNotes = myNotes.load_notes_from_json(file_path = os.path.join(myPreferences.root_pkv(), "AllNotes.json"))

projects = myTools.get_pkv_projects()

#declare an empty datetime 
firstNoteDate = None
lastNoteDate = None


for project in sorted(projects.keys()):
    print("\n")
    print(f"\nProject '{project}'")
    print("-" * len(f"Project '{project}'"))
    # noteTypes = {}
    # for note in allNotes:
    #     if note.project != project:
    #         if firstNoteDate is None or firstNoteDate > note.date:
    #             firstNoteDate = note.date
    #         if lastNoteDate is None or lastNoteDate < note.date:
    #             lastNoteDate = note.date
    #         noteTypes[note.type] = noteTypes.get(note.type, 0) + 1

    #     for key,value in noteTypes.items():
    #         print(f"\t{key}: {value}")
        
    #     print(f"\n\tFirst note date: {firstNoteDate}")
    #     print(f"\tLast note date: {lastNoteDate}")    