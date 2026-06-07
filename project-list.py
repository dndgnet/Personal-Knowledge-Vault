#!/usr/bin/env python3

import os
import shutil
from datetime import datetime

from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Projects as myProjects
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Notes import addLine

myTerminal.clearTerminal()

projectList = addLine("# List of Projects in Vault")
projectList += addLine(f"prepared *{datetime.now().strftime('%Y-%m-%d')}*")

# iterate through the project folder and find each project folder
for filename in sorted(os.listdir(myPreferences.root_projects())):
    if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
        projectConfig = myTools.get_ProjectConfig_as_dict(filename)
        projectName = projectConfig.get("ProjectName", "")
        projectFolder = projectConfig.get("ProjectFolder", "")
        archived = projectConfig.get("Archived", False)
        noteTypes = {}
        lastNote = None
        projectNotes = myNotes.get_Notes_from_Project(projectName=projectName)

        for note in projectNotes:
            noteTypes[note.typeSimple] = noteTypes.get(note.typeSimple, 0) + 1
            if lastNote:
                if note.date > lastNote.date:
                    lastNote = note
            else:
                lastNote = note

        if archived:
            projectList += addLine(f"## Project '{projectName}' (archived)**")
        else:
            projectList += addLine(f"## Project '{projectName}'")

        if lastNote:
            projectList += addLine(
                f"last note is {lastNote.typeSimple} '{lastNote.title}' from {lastNote.date}"
            )
            projectList += addLine("Note types:")

            for noteType, noteTypeCount in noteTypes.items():
                projectList += addLine(f"- {noteTypeCount:>3}: {noteType}")
        else:
            projectList += addLine("- has no notes")

        projectList += addLine("")

projectListFileNameAndPath = os.path.join(myPreferences.root_pkv(), "ProjectList.md")
myNotes.write_Note_to_path(
    notePathAndFile=projectListFileNameAndPath, noteContent=projectList
)
myNotes.open_note_in_editor(projectListFileNameAndPath)
