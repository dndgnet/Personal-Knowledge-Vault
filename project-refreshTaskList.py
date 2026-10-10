#!/usr/bin/env python3

import os
import sys
import datetime

from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Projects as myProjects
from _library import Terminal as myTerminal
from _library import Tools as myTools

myTerminal.clearTerminal()

selectedProject: str = ""
silentMode: bool = False

print(f"{myTerminal.INFORMATION}Generate Project Task List{myTerminal.RESET}\n")

#get selected project from command line argument if provided
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        selectedProject += arg + " "
    selectedProject = selectedProject.strip()
    print(f"Selected project from arguments: '{selectedProject}'")
    
    # Check if the provided project name exists in known projects
    known_projects = myTools.get_pkv_projects()
    if selectedProject not in known_projects:
        print(f"{myTerminal.WARNING}Project '{selectedProject}' not found in known projects.{myTerminal.RESET}")
        print("Will prompt user to select a valid project.")
        selectedProject = ""  # clear so code below prompts the user
    else:
        print(f"{myTerminal.SUCCESS}Valid known project: {selectedProject}{myTerminal.RESET}")
    silentMode = True

if selectedProject == "":
    print("Available target projects:")
    selectedProjectInput = myInputs.select_project_name(False, False)
    if selectedProjectInput is not None:
        selectedProject = selectedProjectInput

if selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

print(f"{myTerminal.SUCCESS}Generating task list for project: {selectedProject}{myTerminal.RESET}")

# Get all notes for the project and generate tasks using the new library function
projectNotes = myNotes.get_Notes_from_Project(selectedProject)
tasks = myProjects.get_tasks_from_project_notes(projectNotes)

if not tasks:
    print(f"{myTerminal.WARNING}No tasks found for project '{selectedProject}'.{myTerminal.RESET}")
    

print(f"{myTerminal.SUCCESS}Found {len(tasks)} task(s).{myTerminal.RESET}")

# Build the markdown content
now = datetime.datetime.now()
timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
author = myPreferences.author_name()

total_tasks = len(tasks)
outstanding = sum(1 for t in tasks if not t.get("complete", False))

content = f"""---
title: {selectedProject} Tasks
type: Task List
created: {timestamp}
start date: {timestamp}
retention: Short
project: {selectedProject}
author: {author}
private: No
shareWithStakeholders: Yes
---

# {selectedProject} Tasks

**Generated**: {timestamp}
**Total tasks**: {total_tasks} ({outstanding} outstanding)

"""

for t in tasks:
    if t.get("complete"):
        taskString = "- [x] "
    else:
        taskString = "- [ ] "

    taskString += t["task"]

    if t.get("AssignedTo"):
        taskString += f"\n\t- Assigned to: {t['AssignedTo']}"

    if t.get("estimatedEffort"):
        taskString += f"\n\t- Estimated Effort: {t['estimatedEffort']}"

    taskString += f"\n\t- [open](<{t.get('notefile', t.get('notepath', ''))}>)\n"

    content += taskString + "\n\n"

# Save to project folder
projectPath = os.path.join(myPreferences.root_projects(), selectedProject)
outputPath = os.path.join(projectPath, "ProjectTask.md")

os.makedirs(projectPath, exist_ok=True)

with open(outputPath, "w", encoding="utf-8") as f:
    f.write(content)

print(f"{myTerminal.SUCCESS}Task list saved to: {outputPath}{myTerminal.RESET}")

# Open the generated file
myTools.open_note_in_editor(outputPath)
