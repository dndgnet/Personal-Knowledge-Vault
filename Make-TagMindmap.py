#!/usr/bin/env python3

import os 
import datetime

from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 


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

markdown = f"""# Mindmap for {selectedTag} tag
"""
mermaid = f"""
```mermaid
mindmap
{i*1}root(({selectedTag}))
"""

for project in projects:
    #add project node
    mermaid += f"""
{i*2}{project}){project if project != "" else "Personal Knowledge Vault"}(
"""
    if project == "":
        markdown += "- **Personal Knowledge Vault**\n"
    else:
        markdown += f"- Project: {project}\n"

    #add links to project node
    for note in linkedNotes:
        if note.project == project:
            mermaid += f"""{i*3}{note.title}({note.title})\n"""
            markdown += f"  - Note: {note.title} *{note.date}* [[{note.id}]]\n"
            
            for tag in note.tags:
                if tag != selectedTag and not tag.startswith("p_"):
                    if tag != selectedTag:
                        #add tags below the note
                        mermaid += f"""{i*4}{tag}(({tag}))\n"""
                        markdown += f"    - Tag: {tag}\n"    

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
output_path = os.path.join(myPreferences.root_pkv(),".TagMindmapDiagram.md")

if os.path.exists(output_path):
    print(f"{myTerminal.WARNING}Tag diagram already exists: {output_path}{myTerminal.RESET}")
    if not myInputs.ask_yes_no("Do you want to overwrite it?", default=True):
        print(f"{myTerminal.INFORMATION}Exiting without changes.{myTerminal.RESET}")
        exit(0)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(body)
    
os.system(f'{myPreferences.default_editor()} "{output_path}"')    