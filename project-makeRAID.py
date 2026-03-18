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

 
newNoteBody += "## Risks\n\n"
newNoteBody += myProjects.raid_Risks(selectedProject,allNotes, returnTableFormat=False)

newNoteBody += "## Issues\n\n"
newNoteBody += myProjects.raid_Issues(selectedProject,allNotes, returnTableFormat=False)
 
newNoteBody += "## Assumptions\n\n"
newNoteBody += myProjects.raid_Assumptions(selectedProject,allNotes, returnTableFormat=False)

newNoteBody += "## Decisions\n\n"
newNoteBody += myProjects.raid_Decisions(selectedProject,allNotes, returnTableFormat=False)


# save RAID log note in the project folder as RAID Log.md
raidLogNotePath = os.path.join(myPreferences.root_projects(), selectedProject, "RAID Log.md")
with open(raidLogNotePath, 'w', encoding='utf-8') as f:
    f.write(newNoteBody)    
print(f"{myTerminal.SUCCESS}RAID Log created:{myTerminal.RESET} {raidLogNotePath}")

myNotes.open_note_in_editor(raidLogNotePath)


