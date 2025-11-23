#!/usr/bin/env python3

"""
This script creates project progress notes for a PKV project.

1. Select an existing project from available projects
2. Create a new progress note using a template or clone from the last progress note
3. Automatically populate note metadata (timestamps, project name, etc.)
4. Save the note with a unique identifier in the project's directory
5. Commit the new note to version control
6. Optionally open the note in the default editor

The script handles two modes:
- Template mode: Creates a new note from a progress template
- Clone mode: Copies the most recent progress note and updates it with new timestamps

"""


import os
import sys
from datetime import datetime

#my stuff
from _library import Preferences as myPreferences
from _library import Inputs as myInputs
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library import VersionControl as myVersionControl

# Define the template and output paths
template_pathRoot = myPreferences.root_templates()



def main(selectedProjectName=""):

    if selectedProjectName == "":
        projects, selectedProjectName, selectedProjectIndex = myInputs.select_project_name_withDict(showNewProjectOption=False)
    
    if selectedProjectName is None or selectedProjectName == "":
        print(f"{myTerminal.ERROR}No project selected. Please select a project first.{myTerminal.RESET}")
        return

    selectedTemplateName = "project_progress_template.markdown"
    
    #based on the selected template, figure out which output folder to use
    selectedTemplatePath = os.path.join(template_pathRoot, selectedTemplateName)
    
    #get rid of unnecessary parts of the template name
    #templates should have a prefix that tells what group of template they belong to
    # and a suffix that shows they are a template
    noteType = selectedTemplateName 
    templateNamePartsToReplace = ["PKV_","project_", "_template.markdown", "_template.md"]
    for part in templateNamePartsToReplace:
        noteType = noteType.replace(part, "")

    #make sure we the default project progress template exist
    if not os.path.exists(selectedTemplatePath):
        print(f"{myTerminal.ERROR}Template '{selectedTemplateName}' not found in {template_pathRoot}{myTerminal.RESET}")
        return

    newNote_directory = os.path.join(myPreferences.root_projects(), selectedProjectName)    
    os.makedirs(newNote_directory, exist_ok=True)


   #collect information that should be seeded into the note fields
    selectedDateTime, title = datetime.now(), "Progress" #myInputs.get_datetime_and_title_from_user("Enter the date and time for the note (or leave blank for system default):",datetime.now())
    timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
    timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    
    titleLettersAndNumbers = myTools.letters_and_numbers_only(title)  # Limit to 200 characters and remove special characters
    uniqueIdentifier = myTools.generate_unique_identifier(timestamp_id, noteType, titleLettersAndNumbers)

    #check for an existing progress note
    progressNoteExists, lastProgressNote = myTools.load_MostRecentProjectProgressNote(selectedProjectName)
    if (progressNoteExists and 
        myInputs.ask_yes_no(f"{myTerminal.INPUTPROMPT}'{selectedProjectName}' has a progress note from {lastProgressNote.date}. Do you want to clone the last note?{myTerminal.RESET}")):
    
        print(f"{myTerminal.BLUE}Cloning last progress note...{myTerminal.RESET}")
        
        #update frontMatter with new date and id
        lastProgressNoteCreateDate = myTools.get_stringValue_from_frontMatter("created", lastProgressNote.frontMatter)
        newFrontMatter = lastProgressNote.frontMatter 
        #replace datetimes 
        newFrontMatter = newFrontMatter.replace(lastProgressNoteCreateDate, timestamp_full)
        #replace dates
        newFrontMatter = newFrontMatter.replace(lastProgressNote.date, timestamp_date)
        #replace id
        newFrontMatter = newFrontMatter.replace(lastProgressNote.id, timestamp_id)

        #replace the date in the note body
        newNoteBody = lastProgressNote.noteBody.replace(f"**Date:** {lastProgressNote.date.split(" ")[0]}", f"**Date:** {timestamp_date}")

        #prepare new note content
        note_Content = newFrontMatter+ "\n\n" + newNoteBody
        
    else:
        # Read the template content
        templateBody = myTools.read_templateBody(selectedTemplatePath)
        
        note_Content = myInputs.get_templateMerge_Values_From_User(timestamp_id,timestamp_date,
                                                                timestamp_full,selectedProjectName,
                                                                title,
                                                                templateBody)
    # Construct the output filename and path
    output_filename = f"{uniqueIdentifier}.md"
    output_path = os.path.join(newNote_directory, output_filename)

    # Save the new note
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(note_Content)

    myVersionControl.add_and_commit(output_path, f"Added new {noteType} note: {title} on {timestamp_full}")

    print(f"{myTerminal.SUCCESS}Note created:{myTerminal.RESET} {output_path}")
    if noteType != "event" or myPreferences.automatically_open_event_notes():
        os.system(f'{myPreferences.default_editor()} "{output_path}"')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        #print ("debug args:",' '.join(sys.argv[1:]))
        args = sys.argv[1:]
        selectedProjectName = args[0].replace('"','')
        main(selectedProjectName)
    else:
        main("")

    print(f"{myTerminal.SUCCESS}Done{myTerminal.RESET}")