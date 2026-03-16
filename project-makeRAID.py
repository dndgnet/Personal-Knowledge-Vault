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

print(f"{myTerminal.INFORMATION}Prepare a RAID Log{myTerminal.RESET}\n")
print("")

#debug
#selectedProject = "Legal Services Request App 2026 Enhancements"

if selectedProject is None or selectedProject == "":
    print("Available target projects:") 
    selectedProject = myInputs.select_project_name(False,False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)


newNoteBody = f"""
# RAID Log

*updated: {myTools.now_YYYY_MM_DD_HH_MM_SS()}*

"""

#get all project notes 
allNotes = myNotes.get_Notes_as_list(os.path.join(myPreferences.root_projects(), selectedProject), 
                                     includePrivateNotes=False, includeArchivedProjects=False)

risks = []
issues = []
assumptions = []
dependencies = []
decisions = []

for note in allNotes:
    noteType = note.type
    if noteType.endswith("risk"):
        risks.append(note)
    elif noteType.endswith("issue"):
        issues.append(note)
    elif noteType.endswith("assumption"):
        assumptions.append(note)
    elif noteType.endswith("dependency"):
        dependencies.append(note)
    elif noteType.endswith("decision"):
        decisions.append(note)

risks = sorted(risks, key=lambda x: x.subId)
issues = sorted(issues, key=lambda x: x.subId)
assumptions = sorted(assumptions, key=lambda x: x.subId)
dependencies = sorted(dependencies, key=lambda x: x.subId)
decisions = sorted(decisions, key=lambda x: x.subId)    

if len(risks) == 0:
    newNoteBody += "## Risks\n\n *No documented risks at this time.*\n\n"
else:
    newNoteBody += "## Risks\n\n"

    if myInputs.ask_yes_no_from_user("Do you want display risks in a table?", default= True):
        newNoteBody += f"{myTools.divTagSmall}\n"
        newNoteBody += "|ID|Identified|Risk                  |Impact|Likelihood|Mitigation|Owner|\n"
        newNoteBody += "|--|----------|----------------------|------|----------|----------|-----|\n"

        for risk in risks:
            newNoteBody += "|"+risk.subId+"|" +myNotes.get_stringValue_from_noteBody("Risk Identified", risk.noteBody)
            newNoteBody += "|"+ risk.title+"|"+ myNotes.get_stringValue_from_noteBody("Impact", risk.noteBody)+"|"+ myNotes.get_stringValue_from_noteBody("Likelihood", risk.noteBody)
            newNoteBody += "|"+ myNotes.get_sectionValue_from_noteBody("Response Strategy", risk.noteBody).replace("\n", "<br>")
            newNoteBody += "|"+ myNotes.get_stringValue_from_noteBody("Risk Owner", risk.noteBody)+"|\n"
        newNoteBody += "\n"+myTools.divTagEnd+"\n\n"
    else:
        for risk in risks:
            newNoteBody += f"### {risk.subId} {risk.title}\n\n"
            newNoteBody += f"**Identified**: {myNotes.get_stringValue_from_noteBody('Risk Identified', risk.noteBody)}\n"
            newNoteBody += f"**Owner**: {myNotes.get_stringValue_from_noteBody('Risk Owner', risk.noteBody)}\n"
            newNoteBody += f"**Impact**: {myNotes.get_stringValue_from_noteBody('Impact', risk.noteBody)} \n**Likelihood**: {myNotes.get_stringValue_from_noteBody('Likelihood', risk.noteBody)}\n"
            newNoteBody += f"**Triggered**: {myNotes.get_stringValue_from_noteBody('Triggered', risk.noteBody)}\n"
            newNoteBody += f"**Description**: {myNotes.get_sectionValue_from_noteBody('Description', risk.noteBody)}\n"            
            newNoteBody += f"**Mitigation**: {myNotes.get_sectionValue_from_noteBody('Response Strategy', risk.noteBody)}\n\n"
            

if len(issues) == 0:
    newNoteBody += "## Issues\n\n *No documented issues at this time.*\n\n"
else:
    newNoteBody += "## Issues\n\n"

    if myInputs.ask_yes_no_from_user("Do you want display issues in a table?", default= True):
        newNoteBody += f"{myTools.divTagSmall}\n"
        newNoteBody += "|ID|Identified|Issue                  |Status|Owner|Description|\n"
        newNoteBody += "|--|----------|----------------------|------|-----|-----------|\n"

        for issue in issues:
            newNoteBody += "|"+issue.subId+"|" +myNotes.get_stringValue_from_noteBody("Identified", issue.noteBody)
            newNoteBody += "|"+ issue.title+"|"+ myNotes.get_stringValue_from_noteBody("Issue Status", issue.noteBody)
            newNoteBody += "|"+ myNotes.get_stringValue_from_noteBody("Issue Owner", issue.noteBody)+"|"+ myNotes.get_sectionValue_from_noteBody("Description", issue.noteBody).replace("\n", "<br>")+"|\n"
        newNoteBody += "\n"+myTools.divTagEnd+"\n\n"
    else:
        for issue in issues:
            newNoteBody += f"### {issue.subId} {issue.title}\n\n"
            newNoteBody += f"**Identified**: {myNotes.get_stringValue_from_noteBody('Identified', issue.noteBody)}\n"
            newNoteBody += f"**Owner**: {myNotes.get_stringValue_from_noteBody('Issue Owner', issue.noteBody)}\n"
            newNoteBody += f"**Status**: {myNotes.get_stringValue_from_noteBody('Issue Status', issue.noteBody)}\n"
            newNoteBody += f"**Description**: {myNotes.get_sectionValue_from_noteBody('Description', issue.noteBody)}\n"            
            newNoteBody += f"**Resolution**: {myNotes.get_sectionValue_from_noteBody('Resolution', issue.noteBody)}\n\n"        



if len(assumptions) == 0:
    newNoteBody += "## Assumptions\n\n *No documented assumptions at this time.*\n\n"
else:
    newNoteBody += "## Assumptions\n\n"

    if myInputs.ask_yes_no_from_user("Do you want display assumptions in a table?", default= True):
        newNoteBody += f"{myTools.divTagSmall}\n"
        newNoteBody += "|ID|Identified|Assumption            |Status|Owner|Description|\n"
        newNoteBody += "|--|----------|----------------------|------|-----|-----------|\n"
        for assumption in assumptions:
            newNoteBody += "|"+assumption.subId+"|" +myNotes.get_stringValue_from_noteBody("Identified", assumption.noteBody)
            newNoteBody += "|"+ assumption.title+"|"+ myNotes.get_stringValue_from_noteBody("Status", assumption.noteBody)
            newNoteBody += "|"+ myNotes.get_stringValue_from_noteBody("Identified by", assumption.noteBody)
            newNoteBody += "|"+ myNotes.get_sectionValue_from_noteBody("Description", assumption.noteBody).replace("\n", "<br>")+"|\n"
        newNoteBody += "\n"+myTools.divTagEnd+"\n\n"
    
    else:
        for assumption in assumptions:
            newNoteBody += f"### {assumption.subId} {assumption.title}\n\n"
            newNoteBody += f"**Identified**: {myNotes.get_stringValue_from_noteBody('Identified', assumption.noteBody)}\n"
            newNoteBody += f"**Status**: {myNotes.get_stringValue_from_noteBody('Status', assumption.noteBody)}\n"
            newNoteBody += f"**Impact**: {myNotes.get_stringValue_from_noteBody('Impact', assumption.noteBody)}\n"
            newNoteBody += f"**Owner**: {myNotes.get_stringValue_from_noteBody('Identified by', assumption.noteBody)}\n"
            newNoteBody += f"**Description**: {myNotes.get_sectionValue_from_noteBody('Description', assumption.noteBody).replace('\n', '<br>')}\n\n"            




# save RAID log note in the project folder as RAID Log.md
raidLogNotePath = os.path.join(myPreferences.root_projects(), selectedProject, "RAID Log.md")
with open(raidLogNotePath, 'w', encoding='utf-8') as f:
    f.write(newNoteBody)    
print(f"{myTerminal.SUCCESS}RAID Log created:{myTerminal.RESET} {raidLogNotePath}")

myNotes.open_note_in_editor(raidLogNotePath)



# deal with stakeholders 

# updatedPart = f"""
# {myTools.divTagSmall}
# |Name                   |Title                  |Role                           |
# |-----------------------|-----------------------|-------------------------------|
# """


# csvFileName = "data_stakeholders.csv"
# csvFilePath = os.path.join(myPreferences.root_projects(), selectedProject, csvFileName)

# if not os.path.exists(csvFilePath):
#     print(f"""{myTerminal.ERROR}CSV file not found at {csvFilePath}.{myTerminal.RESET}
#         \nUse the project-edit_data command to create or update the CSV file.{myTerminal.RESET}""")
# else:

#     # Read the CSV file into a burndown dictionary
#     csvData = {}
#     with open(csvFilePath, "r") as csvFile:
#         headers = csvFile.readline().strip().split(",")
#         for line in csvFile:
#             values = line.strip().split(",")
#             csvData[values[0]] = dict(zip(headers[1:],  values[1:]))

#     #get max budget for y-axis scaling
#     if len(csvData) == 0:
#         print(f"{myTerminal.WARNING}No data found in CSV file.{myTerminal.RESET}")

#     for key, value in csvData.items():
#         updatedPart += f"|{key}|{value['Title']}|{value['Role']}|\n"


#     updatedPart += "\n"+myTools.divTagEnd

#     success, newNoteBody = myNotes.replace_text_between_tags("Stakeholders", hubNote.noteBody, updatedPart)

#     # replace the content between the <!--StartStakeholders--> and <!--EndStakeholders--> tags in the hub note with the new stakeholders table
#     if success:
#         hubNote.noteBody = newNoteBody
#         myNotes.update_NoteBody(hubNote, newNoteBody)
#     else:
#         print(f"{myTerminal.WARNING}Stakeholders tags not found in hub note for project '{selectedProject}'.{myTerminal.RESET}")
#         exit(1)

# # deal with burn down 
# burnDownVisualization = myProjects.diagram_Burndown(selectedProject)

# success, newNoteBody = myNotes.replace_text_between_tags("BurnDown", hubNote.noteBody, burnDownVisualization)

# # replace the content between the <!--StartBurnDown--> and <!--EndBurnDown--> tags in the hub note with the new burn down visualization
# if success:
#     hubNote.noteBody = newNoteBody
#     myNotes.update_NoteBody(hubNote, newNoteBody)
# else:
#     print(f"{myTerminal.WARNING}BurnDown tags not found in hub note for project '{selectedProject}'.{myTerminal.RESET}")
 
# myTools.open_note_in_editor(hubNote.filePath)