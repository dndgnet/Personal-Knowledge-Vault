#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences, Tools as myTools, Inputs as myInputs, Terminal as myTerminal
 

selectedNoteId, note = myInputs.select_recent_note("meeting")

myTerminal.clearTerminal()
print(f"""{myTerminal.YELLOW}Processing meeting note - {note.title} from {note.date}{myTerminal.RESET}""")
noteBody = note.noteBody
newNoteBody = noteBody

if noteBody == "":
    print(f"{myTerminal.WARNING}No meeting notes found in the selected note.{myTerminal.RESET}")
    exit(1)

atomicNoteTemplateBody = myTools.read_templateBody(os.path.join(myPreferences.root_templates(), "atomic_template.markdown"))
h2 = ""
h3 = ""
atomicBody = ""

atomicThoughtsAreaFound = False

for line in noteBody.splitlines():    
    if not atomicThoughtsAreaFound:
        #get to the noteBody part where atomic thoughts 
        #might be created
        if (line.startswith("## Discussion Summary") or line.startswith("## Summary")
            ) or (line.startswith("# Discussion Summary") or line.startswith("# Summary")):
            atomicThoughtsAreaFound = True   
        continue
    
    elif atomicThoughtsAreaFound:
        if line.startswith("## "):
            h2 = line[3:].strip()
            #ask if body should be a note 
        elif line.startswith("### "):
            if atomicBody != "" and h3 != "":
                print (f"\n{myTerminal.SUCCESS}{h3}{myTerminal.RESET}")
                print(atomicBody)
                makeAtomicNote = input("Should this be an atomic thought note? (y/n) ").upper().strip()
                
                if makeAtomicNote == "Y":
                    if note.project != "":
                        selectedProjectName = note.project
                    else:
                        print("\nIf appropriate, select a project for the atomic thought note.")
                        selectedProjectName = myInputs.select_project_name(showNewProjectOption=False)

                    timestamp_id = note.id 
                    timestamp_full = note.date 
                    
                    #add a backlink to the original note
                    atomicBodyWithLink = atomicBody +  f"""\n\n[[{note.id}]] \n\n """

                    atomicNoteData = {"title": h3,
                                    "project": selectedProjectName,
                                    "author": note.author,
                                    "tags": "",
                                    "body": atomicBodyWithLink,
                                }
                    
                    atomicNoteIdentifier = myTools.merge_template_with_values (timestamp_id, timestamp_full, selectedProjectName, atomicNoteTemplateBody, atomicNoteData)
        
                    newNoteBody = newNoteBody.replace(atomicBody, f"\n[[{atomicNoteIdentifier}]]\n\n")
                    # Save the fleeting note with the new atomic thought link
                    with open(note.filePath, 'w', encoding='utf-8') as f:
                        f.write(f"""---\n{note.frontMatter}\n---\n\n {newNoteBody}""")

            h3 = line[4:].strip()
            atomicBody = ""
        else:
            atomicBody += line + "\n"


if not atomicThoughtsAreaFound:
    print(f"{myTerminal.WARNING}No atomic thoughts area found in the selected note, no changes made.{myTerminal.RESET}")
    print("\t atomic thoughts area stars with '## Discussion Summary' or '## Summary'.\n")
else:
    #open the fleeting note 
    os.system(f'{myPreferences.default_editor()} "{note.filePath}"')
