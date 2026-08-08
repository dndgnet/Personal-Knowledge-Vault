#!/usr/bin/env python3

import os
import csv
import shutil
import re
from datetime import datetime,date, timedelta

from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Projects as myProjects
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Notes import addLine

myTerminal.clearTerminal()
print(f"Preparing list of projects in {myPreferences.root_projects()}")

backlogListUpdates = []
progressUpdate = {}

# iterate through the project folder and find each project folder
for filename in sorted(os.listdir(myPreferences.root_projects())):
    if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
        projectConfig = myProjects.get_ProjectConfig_as_dict(filename)
        projectName = projectConfig.get("ProjectName", "")
        publicShareFolder = projectConfig.get("PublicShareFolder", "")
        PublicShareFolderURL = projectConfig.get("PublicShareFolderURL", "")
        NeedsWeeklyProgressUpdate = projectConfig.get("Needs Weekly Progress Update", False)

        TimeCode = projectConfig.get("TimeCode", "")

        ProjectManagementSoftwareURL = projectConfig.get("ProjectManagementSoftwareURL", "")
        ProgressReportGroup = projectConfig.get("ProgressReportGroup", "")
        TeamSharePointBackLogListRowID = projectConfig.get("TeamSharePointBackLogListRowID", 0)

        TeamSharePointSiteURL = projectConfig.get("TeamSharePointSiteURL", "")
        TeamSharePointBackLogListName = projectConfig.get("TeamSharePointBackLogListName", "")
        TeamSharePointBackLogListRowID = projectConfig.get("TeamSharePointBackLogListRowID", 0)

        archived = projectConfig.get("Archived", False)
        if archived:
            print(f"\t\tProject '{projectName}' is archived, skipping.")
            continue  # skip archived projects
        noteTypes = {}
        lastNote = None
        firstNote = None
        hubNote = None
        lastProgressNote = None
        executiveSummaryNote = None
        introductionNote = None
        line = ""

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

            if introductionNote is None and note.typeSimple == "introduction":
                introductionNote = note

            if (note.typeSimple == "progress"
                and (lastProgressNote is None
                    or note.date > lastProgressNote.date)):
                lastProgressNote = note

        if NeedsWeeklyProgressUpdate and TeamSharePointBackLogListRowID != 0 and lastProgressNote:
            print (f"\t\tProject '{projectName}' has a last progress note on {lastProgressNote.date}, preparing update for SharePoint Backlog List")
            cleanNoteBody = lastProgressNote.noteBody.replace("## Progress Statement", "").strip()
            cleanNoteBody = cleanNoteBody.replace("#", "").replace("*", "").strip()
            #Replace anything in between hidden tags <-- and -> with an empty string
            cleanNoteBody = re.sub(r'<!--.*?-->', '', cleanNoteBody, flags=re.DOTALL).strip()

            if len(cleanNoteBody)> 2000:
                cleanNoteBody = cleanNoteBody[:2000] + "..."
            
            progressUpdate = {"ID": TeamSharePointBackLogListRowID, 
                              "ProjectName": projectName, 
                              "LastProgressNoteDate": lastProgressNote.date,
                              "LastProgressNoteBody": cleanNoteBody}

            backlogListUpdates.append(progressUpdate)

if backlogListUpdates:
    print(f"\nPreparing SharePoint Backlog List CSV file with {len(backlogListUpdates)} updates")
    csvFilePath = os.path.join(myPreferences.root_pkv(),"BacklogListUpdates.csv")
    with open(csvFilePath, "w", newline="", encoding="utf-8") as f:
        fieldnames = progressUpdate.keys()  # get the keys from the first dictionary as fieldnames
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()          # writes the header row
        writer.writerows(backlogListUpdates)        # writes all rows

    myTools.open_note_in_editor(csvFilePath)