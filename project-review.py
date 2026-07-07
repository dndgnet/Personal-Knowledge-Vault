#!/usr/bin/env python3

import os 
import json
import sys
from _library import Tools as myTools, Preferences as myPreferences, Inputs as myInputs
from _library import Notes as myNotes
import datetime 

#if input arguments include an integer, use that for days to go back
daysToGoBack = 8

if len(sys.argv) == 2:
    input_value = sys.argv[1]
    if input_value.isdigit():
        daysToGoBack = int(input_value)
    
projects = myTools.get_pkv_projects()
projectThatNeedsWeeklyProgressNoteFound = False

weeklyReview = f"# Last {daysToGoBack} Days Project Review \n\n *prepared on {datetime.datetime.now().strftime('%Y-%m-%d')}*\n\n"
filterDate = (datetime.datetime.now() - datetime.timedelta(days=daysToGoBack)).strftime('%Y-%m-%d')

for projectName in projects.keys():
    projectPath = projects[projectName]
    if os.path.exists(projectPath):
        print(f"Processing project: {projectName}")
        if os.path.exists(os.path.join(projectPath, ".ProjectConfig.json")):
            projectConfig = json.load(open(os.path.join(projectPath, ".ProjectConfig.json"), 'r'))
            archived = projectConfig.get("Archived", False)
            needsWeeklyUpdate = projectConfig.get("Needs Weekly Progress Update", False)
            if not archived and needsWeeklyUpdate:
                projectThatNeedsWeeklyProgressNoteFound = True
                print(f"{projectName} is active and should get a weekly review.")
                weeklyReview += f"## {projectName}\n\n"
                weeklyReview += "<div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px;'>\n\n"

                projectNotes = myNotes.get_Notes_from_Project(projectName)
                #Order notes by date, most recent first
                projectNotes.sort(key=lambda x: x.date, reverse=True)
                noRecentNotes = True
                for note in projectNotes:
                    if note.date >= filterDate:
                        noRecentNotes = False
                        weeklyReview += f"**{note.date} {note.title}**\n\n"
                        weeklyReview += f"{note.noteBody.replace("# ","## ")}\n\n"
                
                if noRecentNotes:
                    weeklyReview += "No recent notes.\n\n"
                
                weeklyReview += "</div>\n\n"
    else:
        
        print(f"Project path does not exist: {projectPath}")

summaryPath = os.path.join(myPreferences.root_pkv(), "WeeklyProjectReview.md")

myNotes.write_Note_to_path(summaryPath, weeklyReview)
myTools.open_note_in_editor(summaryPath)
