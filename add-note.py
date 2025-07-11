#!/usr/bin/env python3

import os
import re
from datetime import datetime

#my stuff
from _library import Preferences as myPreferences
from _library import Inputs as myInputs
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library import VersionControl as myVersionControl

# Define the template and output paths
template_pathRoot = myPreferences.root_templates()


def main():
    projects, selectedProjectName, selectedProjectIndex = myInputs.select_project_name_withDict()
    if selectedProjectName is None or selectedProjectName == "":
        templates, selectedTemplateName, selectedTemplateIndex = myInputs.select_template("pkv")
    else:
        templates, selectedTemplateName, selectedTemplateIndex = myInputs.select_template("project")

    #based on the selected template, figure out which ouptut folder to use
    selectedTemplatePath = os.path.join(template_pathRoot, selectedTemplateName)
    
    #get rid of unnecessary parts of the template name
    #templates should have a prefix that tells what group of template they belong to
    # and a suffix that shows they are a template
    noteType = selectedTemplateName 
    templateNamePartsToReplace = ["PKV_","project_", "_template.markdown", "_template.md"]
    for part in templateNamePartsToReplace:
        noteType = noteType.replace(part, "")

    #make sure the new note directory directory exists
    if selectedProjectName == "" or selectedProjectName is None:
        #project selected, save in the project folder
        newNote_directory = myPreferences.root_pkv()
    else:
        #project not selected, save in the root of the PKV            
        newNote_directory = os.path.join(myPreferences.root_projects(), selectedProjectName)
        
    os.makedirs(newNote_directory, exist_ok=True)

   #collect information that should be seeded into the note fields
    selectedDateTime, title = myInputs.get_datetime_and_title_from_user("Enter the date and time for the note (or leave blank for system default):",datetime.now())
    timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
    timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    
    titleLettersAndNumbers = myTools.letters_and_numbers_only(title)  # Limit to 200 characters and remove special characters
    uniqueIdentifier = myTools.generate_unique_identifier(timestamp_id, noteType, titleLettersAndNumbers)

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
    main()
    print(f"{myTerminal.SUCCESS}Done!{myTerminal.RESET}")