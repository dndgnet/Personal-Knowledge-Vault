#!/usr/bin/env python3
from datetime import datetime
import os
from _library import Terminal as myTerminal, Preferences as myPreferences, Notes as myNotes, Tools as myTools, Inputs as myInputs, Templates as myTemplates, VersionControl as myVersionControl

#call the open-vault.py script to make sure the vault is open before we try to access it
import subprocess
if os.name == 'nt':  # For Windows
    subprocess.run(["py", "open-vault.py"], check=True)
else:
    subprocess.run(["python3", "open-vault.py"], check=True)


#if today's journal exists, open it
# if today's journal does not exist, create it and then open it

notes = myNotes.get_Notes_as_list(myPreferences.root_pkv(), includePrivateNotes=True, includeArchivedProjects=False)
notes = sorted(notes, key=lambda x: x.date, reverse=True)
journalTitle = f"Daily Journal {myPreferences.os_user_name()} {datetime.now().strftime('%Y-%m-%d')}"
for note in notes:
    if note.title == journalTitle:
        myNotes.open_note_in_editor(note.filePath)
        exit(0)

selectedTemplatePath = os.path.join(myPreferences.root_templates(), myPreferences.journal_template_name)
noteType = myPreferences.journal_template_name 
templateNamePartsToReplace = ["PKV_","project_", "_template.markdown", "_template.md"]
for part in templateNamePartsToReplace:
    noteType = noteType.replace(part, "")

noteData = {"project": "",
            "author": myPreferences.author_name(),
        }
newNote_directory = myPreferences.root_pkv()
selectedDateTime =  datetime.now()
timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())

titleLettersAndNumbers = journalTitle  # Limit to 200 characters and remove special characters
uniqueIdentifier = myTools.generate_unique_identifier(timestamp_id, noteType, titleLettersAndNumbers)

# Read the template content
templateBody = myTemplates.read_Template(selectedTemplatePath)

note_Content = myInputs.get_templateMerge_Values_From_User(timestamp_id,timestamp_date,
                                                            timestamp_full,"",
                                                            journalTitle,
                                                            templateBody, promptForAttachments=False)
# Construct the output filename and path
output_filename = f"{uniqueIdentifier}.md"
output_path = os.path.join(newNote_directory, output_filename)

# Save the new note
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(note_Content)

myVersionControl.add_and_commit(output_path, f"Added new {noteType} on {timestamp_full}")

print(f"{myTerminal.SUCCESS}Note created:{myTerminal.RESET} {output_path}")
if noteType != "event" or myPreferences.automatically_open_event_notes():
    # os.system(f'{myPreferences.default_editor()} "{output_path}"')
    myTools.open_note_in_editor(output_path)
