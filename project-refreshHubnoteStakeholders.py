#!/usr/bin/env python3

import os
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Preferences as myPreferences
from _library import Tools as myTools
from _library import Inputs as myInputs 
from _library import Notes as myNotes

myTerminal.clearTerminal()
selectedProject = None

print(f"{myTerminal.INFORMATION}Build Project Stakeholder Table{myTerminal.RESET}\n")
print("")


#debug
#selectedProject = "Legal Services Request App 2026 Enhancements"

if selectedProject is None or selectedProject == "":
    print("Available target projects:") 
    selectedProject = myInputs.select_project_name(False,False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

#get the hub note for the selected project 
hubNoteFound, hubNote = myNotes.get_Note_Last_Project_Note_ByType(selectedProject, "project-hub")

if not hubNoteFound:
    print(f"{myTerminal.WARNING}No hub note found for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

"""
    Name,Title,Contact Info,Role,Expectations,Classification
"""

updatedPart = f"""
{myTools.divTagSmall}
|Name                   |Title                  |Role                           |
|-----------------------|-----------------------|-------------------------------|
"""


csvFileName = "data_stakeholders.csv"
csvFilePath = os.path.join(myPreferences.root_projects(), selectedProject, csvFileName)

if not os.path.exists(csvFilePath):
    print(f"""{myTerminal.ERROR}CSV file not found at {csvFilePath}.{myTerminal.RESET}
        \nUse the project-edit_data command to create or update the CSV file.{myTerminal.RESET}""")
    exit(1)

# Read the CSV file into a burndown dictionary
csvData = {}
with open(csvFilePath, "r") as csvFile:
    headers = csvFile.readline().strip().split(",")
    for line in csvFile:
        values = line.strip().split(",")
        csvData[values[0]] = dict(zip(headers[1:],  values[1:]))

#get max budget for y-axis scaling
if len(csvData) == 0:
    print(f"{myTerminal.WARNING}No data found in CSV file.{myTerminal.RESET}")

for key, value in csvData.items():
    updatedPart += f"|{key}|{value['Title']}|{value['Role']}|\n"


updatedPart += "\n"+myTools.divTagEnd

success, newNoteBody = myNotes.replace_text_between_tags("Stakeholders", hubNote.noteBody, updatedPart)

# replace the content between the <!--StartStakeholders--> and <!--EndStakeholders--> tags in the hub note with the new stakeholders table
if success:
    hubNote.noteBody = newNoteBody
    myNotes.update_NoteBody(hubNote, newNoteBody)
else:
    print(f"{myTerminal.WARNING}Stakeholders tags not found in hub note for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

 
myTools.open_note_in_editor(hubNote.filePath)