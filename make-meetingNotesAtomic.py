#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences, Tools as myTools, Inputs as myInputs, Terminal as myTerminal, VersionControl as myVersionControl

'''
This script processes a meeting note, extracting sections that can be converted into atomic thought notes.
It identifies sections under "## Discussion Summary" or "## Summary", and for each subsection starting
with "###", it prompts the user to decide whether to create an atomic thought note. 


'''

def makeAtomicNote(newNoteBody, atomicBody, h3, note) -> tuple[bool, str]:
    
    atomicNoteCreated = False

    print (f"\n{myTerminal.SUCCESS}{h3}{myTerminal.RESET}\n{atomicBody}\n")
    makeAtomicNote = input("Should this be an atomic thought note? (y/n) ").upper().strip()
    
    if makeAtomicNote == "Y":
        atomicNoteCreated = True

        if note.project != "":
            selectedProjectName = note.project
        else:
            print("\nIf appropriate, select a project for the atomic thought note.")
            selectedProjectName = myInputs.select_project_name(showNewProjectOption=False)

        timestamp_id = note.id 
        timestamp_full = note.date 
        
        #add a backlink to the original note
        atomicBodyWithLink = atomicBody +  f"""\n\n[[{note.fileName}]] \n\n """

        atomicNoteData = {"title": h3,
                        "project": selectedProjectName,
                        "author": note.author,
                        "tags": "",
                        "body": atomicBodyWithLink,
                    }
        
        atomicNoteIdentifier = myTools.merge_template_with_values (timestamp_id, timestamp_full, selectedProjectName, atomicNoteTemplateBody, atomicNoteData)
        tempNote = newNoteBody
        s = atomicBody[-1:]
        if atomicBody[-3:] == "\n\n":
            atomicBody = atomicBody[:-4]
        elif atomicBody[-1:] == "\n":
            atomicBody = atomicBody[:-2]

        newNoteBody = newNoteBody.replace(f"### {h3}\n{atomicBody}", f"### {h3}\n\n[[{atomicNoteIdentifier}]]\n\n")
        
        if tempNote == newNoteBody:
            print(f"{myTerminal.WARNING}No changes made to the fleeting note body.{myTerminal.RESET}")
            return atomicNoteCreated, newNoteBody
        # Save the fleeting note with the new atomic thought link
        with open(note.filePath, 'w', encoding='utf-8') as f:
            f.write(f"""---\n{note.frontMatter}\n---\n\n {newNoteBody}""")
        myVersionControl.add_and_commit(note.filePath, f"moved '{h3}' section from fleeting note {note.title} to {atomicNoteIdentifier} on {timestamp_full}")
            
    h3 = line[4:].strip()
    atomicBody = ""

    return atomicNoteCreated,newNoteBody



selectedNoteId, note = myInputs.select_recent_note("meeting")

myTerminal.clearTerminal()
print(f"""{myTerminal.YELLOW}Processing meeting note - {note.title} from {note.date}{myTerminal.RESET}""")
noteBody = note.noteBody
newNoteBody = noteBody

if selectedNoteId == 0:
    print(f"{myTerminal.WARNING}No meeting notes found in the selected note.{myTerminal.RESET}")
    exit(1)

atomicNoteTemplateBody = myTools.read_templateBody(os.path.join(myPreferences.root_templates(), "atomic_template.markdown"))
h2 = ""
h3 = ""
atomicBody = ""


atomicThoughtsAreaFound = False
countFoundAtomicThoughtNotes = 0
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
        elif line.startswith("### ") or line.startswith("#### Attachments"):
            if atomicBody != "" and h3 != "":
                atomicNoteMade, newNoteBody = makeAtomicNote(newNoteBody, atomicBody, h3, note)
                
                if atomicNoteMade:
                    countFoundAtomicThoughtNotes += 1
            atomicBody = ""
            h3 = line[4:].strip()
        else:
            atomicBody += line + "\n"

if atomicBody != "":
    atomicNoteMade, newNoteBody = makeAtomicNote(newNoteBody, atomicBody, h3, note)
    if atomicNoteMade:
        countFoundAtomicThoughtNotes += 1

if countFoundAtomicThoughtNotes == 0:
    if atomicThoughtsAreaFound:
        print(f"{myTerminal.WARNING}No atomic thoughts were moved to atomic notes, no changes made.{myTerminal.RESET}")
    else:
        print(f"{myTerminal.WARNING}No atomic thoughts area found in the selected note, no changes made.{myTerminal.RESET}")
        print("\t atomic thoughts area stars with '## Discussion Summary' or '## Summary'.\n")
else:
    #open the fleeting note 
    os.system(f'{myPreferences.default_editor()} "{note.filePath}"')
