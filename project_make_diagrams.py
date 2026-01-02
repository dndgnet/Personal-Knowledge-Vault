#!/usr/bin/env python3

import os
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Preferences as myPreferences
from _library import Tools as myTools
from _library import Inputs as myInputs 

myTerminal.clearTerminal()
print(f"{myTerminal.INFORMATION}Import and Update Project Tasks{myTerminal.RESET}\n")
print("Select the target project then select the CSV file (exported from Jira, DevOps, Trello, etc.) from your downloads folder")

print("Available target projects:") 
selectedProject = myInputs.select_project_name(False,False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

diagramPage = f"""
# {selectedProject} - Diagrams 

prepared: {myTools.now_YYYY_MM_DD_HH_MM_SS()}

"""

# Generate and append the kanban by assigned diagram
diagramPage += f"""
## Tasks by state

{myProjects.diagram_kanban_by_state(selectedProject)}

"""

# Generate and append the kanban by assigned diagram
diagramPage += f"""
## Tasks by assigned to

{myProjects.diagram_kanban_by_assigned(selectedProject)} 

"""

# Generate and append the Gantt chart diagram for Tasks
diagramPage += f"""
## Gantt Chart of Tasks  

{myProjects.diagram_Gantt_tasks(selectedProject)}

"""

# Generate and append the Gantt chart diagram for Notes
diagramPage += f"""
## Gantt Chart of Notes and Events  

{myProjects.diagram_Gantt_notes(selectedProject, includePrivateNotes=False)}

"""

outputFilePath = os.path.join(myPreferences.root_projects(), selectedProject, ".Diagrams.md")
myTools.write_text_to_file(outputFilePath, diagramPage)
myTools.open_note_in_editor(outputFilePath)