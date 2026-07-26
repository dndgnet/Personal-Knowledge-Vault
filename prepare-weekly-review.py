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

reportBody = addLine("# Team Project Summary")
reportBody += addLine(f"prepared *{datetime.now().strftime('%Y-%m-%d')}*")

groupReports = {}

# iterate through the project folder and find each project folder
for filename in sorted(os.listdir(myPreferences.root_projects())):
    if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
        projectConfig = myProjects.get_ProjectConfig_as_dict(filename)
        projectName = projectConfig.get("ProjectName", "")
        print(f"\tProcessing project '{projectName}'")
        publicShareFolder = projectConfig.get("PublicShareFolder", "")
        PublicShareFolderURL = projectConfig.get("PublicShareFolderURL", "")
        NeedsWeeklyProgressUpdate = projectConfig.get("Needs Weekly Progress Update", False)
        TimeCode = projectConfig.get("TimeCode", "")
        ProjectManagementSoftwareURL = projectConfig.get("ProjectManagementSoftwareURL", "")
        ProgressReportGroup = projectConfig.get("ProgressReportGroup", "")
        archived = projectConfig.get("Archived", False)
        noteTypes = {}
        lastNote = None
        firstNote = None
        hubNote = None
        lastProgressNote = None
        executiveSummaryNote = None
        introductionNote = None

        if archived:
            print(f"\t\tProject '{projectName}' is archived, skipping.")
            continue  # skip archived projects
        if not NeedsWeeklyProgressUpdate:
            print(f"\t\tProject '{projectName}' does not need weekly progress updates, skipping.")
            continue  # skip projects that don't need weekly progress updates   

        if groupReports.get(ProgressReportGroup) is None:
            #start the reportGroup
            groupReports[ProgressReportGroup] = f"# {ProgressReportGroup} Summary\n\n"
            groupReports[ProgressReportGroup] += addLine(f"prepared *{datetime.now().strftime('%Y-%m-%d')}*")


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

        #display project information
        if archived:
            reportBody += addLine(f"<div style='break-after: page;'></div>\n\n # Archived Project '{projectName}'")
        else:
            line = addLine(f"<div style='break-after: page;'></div>\n\n # Project '{projectName}'")
            reportBody += line
            groupReports[ProgressReportGroup] += line 
        
        if PublicShareFolderURL:
            line = addLine(f"Public Share Folder: [link]({PublicShareFolderURL})")
            reportBody += line
            groupReports[ProgressReportGroup] += line 

        if TimeCode:
            line = addLine(f"Time Code: {TimeCode}")
            reportBody += line
            groupReports[ProgressReportGroup] += line
        
        if ProjectManagementSoftwareURL:
            line = addLine(f"Project Management Software URL: [link]({ProjectManagementSoftwareURL})")
            reportBody += line
            groupReports[ProgressReportGroup] += line

        # projectList += addLine("**Note and Event types:**")
        # for noteType, noteTypeCount in noteTypes.items():
        #     projectList += addLine(f"- {noteTypeCount:>3}: {noteType}")

        if firstNote:
            if firstNote != lastNote and lastNote:
                line = addLine(
                    f"First project event is '{firstNote.typeSimple}' from {firstNote.date}, last project event is '{lastNote.typeSimple}' from {lastNote.date}"
                )
                reportBody += line
                groupReports[ProgressReportGroup] += line
                
            else:   
                line = addLine(
                    f"First project event is '{firstNote.typeSimple}' from {firstNote.date}"
                )
                reportBody += line
                groupReports[ProgressReportGroup] += line

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
                reportBody += line
                groupReports[ProgressReportGroup] += line
                line = addLine(
                    f"Project Introduction note is from {introductionNote.date}"
                )
                reportBody += line
                groupReports[ProgressReportGroup] += line
    
                line = addLine(f"""<div style="font-size:small; margin-left: 6em;">\n\n{introductionNote.noteBody.replace("# ", "## ")}\n\n</div>\n\n""")
                reportBody += line
                groupReports[ProgressReportGroup] += line

            if executiveSummaryNote and not hasIntroductionNote:
                line = addLine(
                    f"Executive summary note is from {executiveSummaryNote.date}"
                )
                reportBody += line
                groupReports[ProgressReportGroup] += line
                line = addLine(
                    f"Executive summary note is from {executiveSummaryNote.date}"
                )
                reportBody += line
                groupReports[ProgressReportGroup] += line
    
                line = addLine(f"""<div style="font-size:small; margin-left: 6em;">\n\n{executiveSummaryNote.noteBody.replace("# ", "## ")}\n\n</div>\n\n""")
                reportBody += line
                groupReports[ProgressReportGroup] += line
                

            if lastProgressNote:
                line = addLine(
                    f"Last progress note is from {lastProgressNote.date}."
                )
                reportBody += line
                groupReports[ProgressReportGroup] += line   
                
                line = addLine(f"""<div style="font-size:small; margin-left: 6em;">\n\n{lastProgressNote.noteBody.replace("# ", "## ")}\n\n</div>\n\n\n""")
                reportBody += line
                groupReports[ProgressReportGroup] += line
                
                 

            reportBody += addLine("")
            groupReports[ProgressReportGroup] += addLine("")

        else:
            reportBody += addLine("- has no notes\n\n")
            groupReports[ProgressReportGroup] += addLine("- has no notes\n\n")

today = date.today()
monday = today - timedelta(days=today.weekday())
saveFile=True 

filesToOpen = []

#save one big report for all groups
weeklySummaryFileAndPath = os.path.join(myPreferences.root_pkv(), f"{monday} Summary.md")
if os.path.exists(weeklySummaryFileAndPath):
    if not myInputs.ask_yes_no_from_user(f"Project list file '{weeklySummaryFileAndPath}' already exists. Do you want to overwrite it?: ",True):
        saveFile=False

if saveFile:
    myNotes.write_Note_to_path(
        notePathAndFile=weeklySummaryFileAndPath, noteContent=reportBody
    )
else:
    print(f"No changes, opening the existing file '{weeklySummaryFileAndPath}' file.")

filesToOpen.append(weeklySummaryFileAndPath)

#save one report for each group
for group, report in groupReports.items():
    if group == "":
        group = "Other"
    print (f"Preparing report for group '{group}' for '{monday}' with a length of {len(report)} characters.")

    groupReportFileAndPath = os.path.join(myPreferences.root_pkv(), f"{monday} {group} Summary.md")
    saveFile=True 
    if os.path.exists(groupReportFileAndPath) and not myInputs.ask_yes_no_from_user(f"Project list file '{groupReportFileAndPath}' already exists. Do you want to overwrite it?: ",True):
        saveFile=False

    if saveFile:
        myNotes.write_Note_to_path(
            notePathAndFile=groupReportFileAndPath, noteContent=report
        )
    else:
        print(f"No changes, opening the existing file '{groupReportFileAndPath}' file.")

    filesToOpen.append(groupReportFileAndPath)

myTerminal.executePythonScript("open-vault.py")
for filePath in filesToOpen:
    myNotes.open_note_in_editor(filePath)
