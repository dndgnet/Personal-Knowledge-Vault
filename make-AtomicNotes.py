#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences, Inputs as myInputs, Terminal as myTerminal, VersionControl as myVersionControl, Notes as myNote
from _library.Templates import merge_template_with_values, read_Template
import re

'''
This script processes a meeting note, extracting sections that can be converted into atomic thought notes.
It identifies sections under "## Discussion Summary" or "## Summary", and for each subsection starting
with "###", it prompts the user to decide whether to create an atomic thought note. 


'''

def makeAtomicNote(newNoteBody, atomicBody, h2, note) -> tuple[bool, str]:
    
    atomicNoteCreated = False
    if atomicBody.strip().startswith("![[") and atomicBody.strip().endswith(".md]]"):
        #probably already converted this heading to an atomic note
        return atomicNoteCreated, newNoteBody
    

    print (f"\n{myTerminal.SUCCESS}{h2}{myTerminal.RESET}\n{atomicBody}\n")
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
        #atomicBodyWithLink = atomicBody +  f"""\n\n<!--hidden\n[[{note.fileName}]] \n-->\n\n """
        atomicBodyWithLink = atomicBody +  f"""\n\n[[{note.fileName}]]\n\n """

        atomicNoteData = {"title": h2,
                        "project": selectedProjectName,
                        "author": note.author,
                        "tags": "",
                        "body": atomicBodyWithLink,
                    }
        
        atomicNoteIdentifier,noteBody = merge_template_with_values (timestamp_id, timestamp_full, selectedProjectName, 
                                                           atomicNoteTemplateBody, atomicNoteData, 
                                                           runSilent=True, processUnPopulatedNoteBodyMergeTags = False)
        atomicNoteFileName = f"{atomicNoteIdentifier}.md"

        myNote.write_Note_to_path(os.path.join(myPreferences.root_projects(), selectedProjectName, atomicNoteFileName), noteBody)

        tempNote = newNoteBody
        atomicBody = atomicBody.strip()
        
        if selectedProjectName != "":
            newNoteBody = re.sub(
                rf"## {re.escape(h2)}\s*{re.escape(atomicBody)}", 
                f"## {h2}\n\n![[./_Projects/{selectedProjectName}/{atomicNoteFileName}]]\n\n",
                newNoteBody
            )
        else:
            newNoteBody = re.sub(
                rf"## {re.escape(h2)}\s*{re.escape(atomicBody)}", 
                f"## {h2}\n\n![[./_Projects/{atomicNoteFileName}]]\n\n",
                newNoteBody
            )

        if tempNote == newNoteBody:
            print(f"{myTerminal.WARNING}No changes made to the fleeting note body.{myTerminal.RESET}")
            return atomicNoteCreated, newNoteBody
        # Save the fleeting note with the new atomic thought link
        with open(note.filePath, 'w', encoding='utf-8') as f:
            f.write(f"""---\n{note.frontMatter}\n---\n\n {newNoteBody}""")
        myVersionControl.add_and_commit(note.filePath, f"moved '{h2}' section from fleeting note {note.title} to {atomicNoteFileName} on {timestamp_full}")
            
    h2 = line[4:].strip()
    atomicBody = ""
    return atomicNoteCreated,newNoteBody

selectedNoteId, note = myInputs.select_recent_note("journal",showActionItems=True, groupByProject=False, DaysToGoBack=8)

myTerminal.clearTerminal()
print(f"""{myTerminal.YELLOW}Processing meeting note - {note.title} from {note.date}{myTerminal.RESET}""")
noteBody = note.noteBody
newNoteBody = noteBody

if selectedNoteId == 0:
    print(f"{myTerminal.WARNING}No meeting notes found in the selected note.{myTerminal.RESET}")
    exit(1)

atomicNoteTemplateBody = read_Template(os.path.join(myPreferences.root_templates(), "atomic_template.markdown"))
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
            ) or (line.startswith("# Discussion Summary") or line.startswith("# Summary") or line.startswith("# Notes")):
            atomicThoughtsAreaFound = True   
        continue
    elif atomicThoughtsAreaFound:
        if line.startswith("## ") or line.startswith("### Attachments") or line.startswith("#### Attachments"):
            if h2 != "":
                #copy the atomic part to new note
                atomicNoteMade, newNoteBody = makeAtomicNote(newNoteBody, atomicBody, h2, note)

                if atomicNoteMade:
                    countFoundAtomicThoughtNotes += 1
                    #save the source note with the new links to atomic notes
                    myNote.write_Note_to_path(note.filePath, f"""---\n{note.frontMatter}\n---\n\n {newNoteBody}""")
                    
                #reset for next atomic thought
                atomicBody = ""
                h2 = line[3:].strip()
            
            else:
                #start an atomic thought
                h2 = line[3:].strip()
                atomicBody = ""
        else:
            atomicBody += line + "\n"

    
if atomicBody != "":
    atomicNoteMade, newNoteBody = makeAtomicNote(newNoteBody, atomicBody, h2, note)
    if atomicNoteMade:
        countFoundAtomicThoughtNotes += 1
        #save the source note with the new links to atomic notes
        myNote.write_Note_to_path(note.filePath, f"""---\n{note.frontMatter}\n---\n\n {newNoteBody}""")
        

if countFoundAtomicThoughtNotes == 0:
    if atomicThoughtsAreaFound:
        print(f"{myTerminal.WARNING}No atomic thoughts were moved to atomic notes, no changes made.{myTerminal.RESET}")
    else:
        print(f"{myTerminal.WARNING}No atomic thoughts area found in the selected note, no changes made.{myTerminal.RESET}")
        print("\t atomic thoughts area stars with '## Discussion Summary' or '## Summary' or '# Notes'.\n")
else:
    #open the fleeting note 
    os.system(f'{myPreferences.default_editor()} "{note.filePath}"')
