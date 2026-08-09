#!/usr/bin/env python3
import csv
from datetime import datetime
import os 
import shutil
import subprocess
import time
import re 
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 
from _library import HTML as myHTML
from _library import Notes as myNotes


print("Downloading SharePoint List Comments")
selectedProject = myInputs.select_project_name(showNewProjectOption=False, showNoProjectOption=False)

if selectedProject == "":
    print("No project selected, exiting.")
    exit()


temporarySharePointListCommentsPath = myPreferences.temporarySharePointListCommentsPath()

if temporarySharePointListCommentsPath == "":
    print("Temporary SharePoint List Comments Path is not set in preferences. Please set it and try again.")
    exit()

if not os.path.exists(temporarySharePointListCommentsPath):
    os.makedirs(temporarySharePointListCommentsPath)

projectConfig = myProjects.get_ProjectConfig_as_dict(selectedProject)

teamSharePointBackLogListRowID = int(projectConfig.get("TeamSharePointBackLogListRowID", 0))


if teamSharePointBackLogListRowID == 0:
    print(f"Project '{selectedProject}' does not have a valid TeamSharePointBackLogListRowID configured. Please update the project configuration.")
    exit()       

#read the sharepoint list comments into a dictionary 
dictSharePointListComments = {}

with open(temporarySharePointListCommentsPath, mode='r', newline='', encoding='utf-8') as csvFile:
    reader = csv.DictReader(csvFile)
    for row in reader:
        key = len(dictSharePointListComments)
        dictSharePointListComments[key] = row

templateName = "project_backlogcomment_template.markdown"

for key,value in dictSharePointListComments.items():
    #Value keys are "DownloadDate","ID","Title","CommentAuthor","CommentDate","CommentBody"
    if int(value.get("ID", 0)) == teamSharePointBackLogListRowID:
        id = value.get("CommentDate","") + "_BLComment_" + value.get("CommentAuthor","").split(" ")[0]
        CommentAuthor = value.get("CommentAuthor","")
        CommentDate = value.get("CommentDate","")
        CommentBody = value.get("CommentBody","")   
        mergeData = {
                "id": id,
                "CommentAuthor": CommentAuthor,
                "CommentBody": CommentBody,
                "Project Name": selectedProject,
                "isMilestone": "No"
            }

        isDate,suggestedDatetime = myTools.datetime_fromString(CommentDate)
        if isDate is False:
            suggestedDatetime = datetime.now()

        output_path, note_Content, uniqueIdentifier = myNotes.make_note_from_template(
            selectedProjectName=selectedProject,
            selectedTemplateName=templateName,
            suggestedDateTime=suggestedDatetime,
            mergeData=mergeData,
            suggestedTitle="Backlog Comment: " + CommentAuthor + " - " + CommentDate)

        print (f"\tCreated note for Backlog Comment by '{CommentAuthor}' on '{CommentDate}' at '{output_path}'.")

        # myTools.open_vault()
        # myTools.open_note_in_editor(output_path)
        