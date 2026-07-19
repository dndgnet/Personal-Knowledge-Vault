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
print(f"Preparing list of projects in {myPreferences.root_projects()}")
# iterate through the project folder and find each project folder
for filename in sorted(os.listdir(myPreferences.root_projects())):
    if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
        projectConfig = myTools.get_ProjectConfig_as_dict(filename)
        projectName = projectConfig.get("ProjectName", "")
        print(f"\tProcessing project '{projectName}'")
        publicShareFolder = projectConfig.get("PublicShareFolder", "")
        archived = projectConfig.get("Archived", False)
        if archived:
            continue  # skip archived projects
        noteTypes = {}
        lastNote = None
        firstNote = None
        hubNote = None
        lastProgressNote = None
        projectNotes = myNotes.get_Notes_from_Project(projectName=projectName)

        for note in projectNotes:
            noteTypes[note.typeSimple] = noteTypes.get(note.typeSimple, 0) + 1
            if lastNote:
                if note.date > lastNote.date:
                    lastNote = note
            else:
                lastNote = note

            if firstNote:
                if note.date < firstNote.date:
                    firstNote = note
            else:
                firstNote = note

            if hubNote is None and note.typeSimple == "hub":
                hubNote = note

            if lastProgressNote is None and note.typeSimple == "progress":
                lastProgressNote = note
            elif (
                lastProgressNote
                and note.typeSimple == "progress"
                and note.date > lastProgressNote.date
            ):
                lastProgressNote = note

        if archived:
            projectList += addLine(f"## Archived Project '{projectName}'")
        else:
            projectList += addLine(f"## Project '{projectName}'")

        projectList += addLine(f"Public Share Folder: {publicShareFolder}") 

        if firstNote:
            projectList += addLine(
                f"first note is {firstNote.typeSimple} '{firstNote.title}' from {firstNote.date}"
            )

            if lastNote:
                projectList += addLine(
                    f"last note is {lastNote.typeSimple} '{lastNote.title}' from {lastNote.date}"
                )

            if hubNote:
                projectList += addLine(
                    f"hub note is '{hubNote.title}' [[./_projects/{hubNote.project}/{hubNote.fileName}]]"
                )

            if lastProgressNote:
                projectList += addLine(
                    f"last progress note is [[./_projects/{lastProgressNote.project}/{lastProgressNote.fileName}]] from {lastProgressNote.date}"
                )

                projectList += f"""<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'>\n\n{lastProgressNote.noteBody.replace("# ", "## ")}\n\n</div>\n\n"""

                projectList += addLine("")

            projectList += addLine("Note types:")

            for noteType, noteTypeCount in noteTypes.items():
                projectList += addLine(f"- {noteTypeCount:>3}: {noteType}")

            projectList += addLine("")

        else:
            projectList += addLine("- has no notes")
            projectList += addLine("")

projectListFileNameAndPath = os.path.join(myPreferences.root_pkv(), "ProjectList.md")
myNotes.write_Note_to_path(
    notePathAndFile=projectListFileNameAndPath, noteContent=projectList
)

myTerminal.executePythonScript("open-vault.py")
myNotes.open_note_in_editor(projectListFileNameAndPath)
