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
print(f"Preparing list of projects in {myPreferences.root_projects()}")

projectList = addLine("# PKV Project Summary")
projectList += addLine(f"prepared *{datetime.now().strftime('%Y-%m-%d')}*")

# iterate through the project folder and find each project folder
for filename in sorted(os.listdir(myPreferences.root_projects())):
    if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
        projectConfig = myTools.get_ProjectConfig_as_dict(filename)
        projectName = projectConfig.get("ProjectName", "")
        print(f"\tProcessing project '{projectName}'")
        publicShareFolder = projectConfig.get("PublicShareFolder", "")
        PublicShareFolderURL = projectConfig.get("PublicShareFolderURL", "")
        NeedsWeeklyProgressUpdate = projectConfig.get("Needs Weekly Progress Update", False)
        TimeCode = projectConfig.get("TimeCode", "")
        ProjectManagementSoftwareURL = projectConfig.get("ProjectManagementSoftwareURL", "")
        archived = projectConfig.get("Archived", False)
        noteTypes = {}
        lastNote = None
        firstNote = None
        hubNote = None
        lastProgressNote = None
        executiveSummaryNote = None

        if archived:
            continue  # skip archived projects
        if not NeedsWeeklyProgressUpdate:
            continue  # skip projects that don't need weekly progress updates   
        

        projectNotes = myNotes.get_Notes_from_Project(projectName=projectName)

        #gather important notes
        for note in projectNotes:
            #skip private notes
            if note.private:
                continue

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

            if executiveSummaryNote is None and note.typeSimple == "executive_summary":
                executiveSummaryNote = note

            if lastProgressNote is None and note.typeSimple == "progress":
                lastProgressNote = note
            elif (
                lastProgressNote
                and note.typeSimple == "progress"
                and note.date > lastProgressNote.date
            ):
                lastProgressNote = note

        #display project information
        if archived:
            projectList += addLine(f"<div style='break-after: page;'></div>\n\n # Archived Project '{projectName}'")
        else:
            projectList += addLine(f"<div style='break-after: page;'></div>\n\n # Project '{projectName}'")
        
        if PublicShareFolderURL:
            projectList += addLine(f"Public Share Folder: [link]({PublicShareFolderURL})")

        if TimeCode:
            projectList += addLine(f"Time Code: {TimeCode}")
        
        if ProjectManagementSoftwareURL:
            projectList += addLine(f"Project Management Software URL: [link]({ProjectManagementSoftwareURL})")

        projectList += addLine("**Note and Event types:**")
        for noteType, noteTypeCount in noteTypes.items():
            projectList += addLine(f"- {noteTypeCount:>3}: {noteType}")

        if firstNote:
            if firstNote != lastNote:
                projectList += addLine(
                    f"First project event is '{firstNote.typeSimple}' from {firstNote.date}, last project event is '{lastNote.typeSimple}' from {lastNote.date}"
                )
            else:   
                projectList += addLine(
                    f"First project event is '{firstNote.typeSimple}' from {firstNote.date}"
            ) 

            # if hubNote:
            #     projectList += addLine(
            #         f"hub note is '{hubNote.title}' [[./_projects/{hubNote.project}/{hubNote.fileName}]]"
            #     )

            if executiveSummaryNote:
                projectList += addLine(
                    f"Executive summary note is from {executiveSummaryNote.date}"
                )

                projectList += f"""<div style="font-size:small; margin-left: 6em;">\n\n{executiveSummaryNote.noteBody.replace("# ", "## ")}\n\n</div>\n\n"""

                projectList += addLine("")

            if lastProgressNote:
                projectList += addLine(
                    f"Last progress note is from {lastProgressNote.date}."
                )

                projectList += f"""<div style="font-size:small; margin-left: 6em;">\n\n{lastProgressNote.noteBody.replace("# ", "## ")}\n\n</div>\n\n"""

                projectList += addLine("")

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
