#!/usr/bin/env python3

import os
import shutil
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
        noteTypes = {}
        lastNote = None
        firstNote = None
        hubNote = None
        lastProgressNote = None
        executiveSummaryNote = None
        introductionNote = None
        line = ""

        # if archived:
        #     print(f"\t\tProject '{projectName}' is archived, skipping.")
        #     continue  # skip archived projects
        # if not NeedsWeeklyProgressUpdate:
        #     #print(f"\t\tProject '{projectName}' does not need weekly progress updates, skipping.")
        #     continue  # skip projects that don't need weekly progress updates   

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

        print(myTerminal.addColourToLine(f"Project '{projectName}' ", "yellow"))
                    
        #display project information
        if archived:
            print(myTerminal.addColourToLine("\tarchived", "blue"))

        if NeedsWeeklyProgressUpdate:
            print(myTerminal.addColourToLine("\tneeds weekly progress updates", "green"))
        # else:
        #     print(myTerminal.addColourToLine("\tdoes not need weekly progress updates", "grey"))
        
        if ProjectManagementSoftwareURL:
            print("\tTracked by project management software")
            #print("\t\t",ProjectManagementSoftwareURL)

        if ProgressReportGroup:
            print(f"\tProgress Report Group: {ProgressReportGroup}")

        if TeamSharePointBackLogListRowID != 0:
            print(f"\tTeam SharePoint Backlog List Row ID: {TeamSharePointBackLogListRowID}")

        if PublicShareFolderURL:
            line = addLine(f"Public Share Folder: [link]({PublicShareFolderURL})")
          
        if TimeCode:
            line = addLine(f"Time Code: {TimeCode}")
          
        if ProjectManagementSoftwareURL:
            line = addLine(f"Project Management Software URL: [link]({ProjectManagementSoftwareURL})")
          
        # projectList += addLine("**Note and Event types:**")
        # for noteType, noteTypeCount in noteTypes.items():
        #     projectList += addLine(f"- {noteTypeCount:>3}: {noteType}")

        if firstNote:
            
            if firstNote != lastNote and lastNote:
                line = addLine(
                    f"First project event is '{firstNote.typeSimple}' from {firstNote.date}, last project event is '{lastNote.typeSimple}' from {lastNote.date}"
                )
                
            else:   
                line = addLine(
                    f"First project event is '{firstNote.typeSimple}' from {firstNote.date}"
                )
        
            # if hubNote:
            #     projectList += addLine(
            #         f"hub note is '{hubNote.title}' [[./_projects/{hubNote.project}/{hubNote.fileName}]]"
            #     )

            hasIntroductionNote = False
            if introductionNote:
                hasIntroductionNote = True
                line = addLine(
                    f"Project Introduction note is from {introductionNote.date}"
                )
                print(f"\t{line}")
                
            if executiveSummaryNote:
                line = addLine(
                    f"Executive summary note is from {executiveSummaryNote.date}"
                )
                print(f"\t{line}")
                
            if lastProgressNote:
                line = addLine(
                    f"Last progress note is from {lastProgressNote.date}."
                )
                print(f"\t{line}")   

                line = addLine(
                    f"{len(lastProgressNote.noteBody)} characters \n\t\t{lastProgressNote.noteBody[:100].replace('#', '').replace('\n','\n\t\t')}..."
                )              
                print(f"\t{line}")

            print (f"\t{len(projectNotes)} notes in project")
 
