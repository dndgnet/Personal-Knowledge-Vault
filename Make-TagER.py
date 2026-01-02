#!/usr/bin/env python3

import os 
import datetime

from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 
from _library import HTML as myHTML
import re

print(f"{myTerminal.INFORMATION}Diagram a tag...{myTerminal.RESET}\n")

print("Available tags:") 
selectedTag = myInputs.select_tag()

allNotes = myTools.get_Notes_as_list(myPreferences.root_pkv())

projects = {}
#make an allowance for our special project tag 'p_' that
#indicates a hash tag for a project
if selectedTag.startswith("p_"):
    projects[selectedTag[:2]] = 1

linkedNotes = []
for note in allNotes:
    if selectedTag in note.tags:
        projects[note.project] = projects.get(note.project, 0)  + 1
        linkedNotes.append(note)

#i = indent
i = "\t"

markdown = f"""# Relationships for {selectedTag} tag
"""
mermaid = f"""
```mermaid
---
title: {selectedTag} Relationships
---
erDiagram

"""

for project in projects:
    #add project node
    mermaid += f"""
{i*1}{selectedTag}||--||{project.replace(" ","-") if project != "" else "Personal-Knowledge-Vault"} : pkv
"""
    if project == "":
        markdown += "- **Personal Knowledge Vault**\n"
    else:
        markdown += f"- Project: {project}\n"

    #add links to project node
    for note in linkedNotes:
        safeNoteName = re.sub(r'[^a-zA-Z0-9\s]', '', note.title).replace(' ', '_')
        safeProjectName = re.sub(r'[^a-zA-Z0-9\s]', '', project).replace(' ', '_')
        if safeProjectName == "":
            safeProjectName = "Personal_Knowledge_Vault"

        if note.project == project:
            mermaid += f"""{i*2}{safeProjectName if safeProjectName != "" else "Personal-Knowledge-Vault"}||--||{safeNoteName} : project\n"""
            markdown += f"  - Note: {note.title} *{note.date}* [[{note.id}]]\n"
            
            for tag in note.tags:
                safeTag = re.sub(r'[^a-zA-Z0-9\s]', '', tag).replace(' ', '_')

                if tag != selectedTag and not tag.startswith("p_") and tag.strip() != "" and tag != "p_" and safeTag != "_":
                    if tag != selectedTag:
                        #add tags below the note
                        mermaid += f"""{i*3}{safeNoteName}||--||{safeTag.strip()} : pageTag\n"""
                        markdown += f"    - Tag: {safeTag}\n"    

#finish the mermaid diagram
mermaid += """
```
"""


body = f"""
{markdown}

{mermaid}


prepared {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""


# use the dot prefix to hide the file in the project directory (at least in civilized file managers)
output_path = os.path.join(myPreferences.root_pkv(),".TagERDiagram.md")

if os.path.exists(output_path):
    print(f"{myTerminal.WARNING}Tag diagram already exists: {output_path}{myTerminal.RESET}")
    if not myInputs.ask_yes_no_from_user("Do you want to overwrite it?", default=True):
        print(f"{myTerminal.INFORMATION}Exiting without changes.{myTerminal.RESET}")
        exit(0)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(body)
    
os.system(f'{myPreferences.default_editor()} "{output_path}"')    
myHTML.openMarkDownFileInBrowser(output_path)