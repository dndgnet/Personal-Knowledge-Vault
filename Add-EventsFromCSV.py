#!/usr/bin/env python3

import os
import re
from datetime import datetime, timedelta
import csv 

#my stuff
from _library import Preferences as myPreferences
from _library import Inputs as myInputs
from _library import Terminal as myTerminal
from _library import Tools as myTools

# Define the template and output paths
template_pathRoot = myPreferences.root_templates()


def main():
    # projects, selectedProjectName, selectedProjectIndex = myInputs.select_project_name()
    # if selectedProjectName is None or selectedProjectName == "":
    #     templates, selectedTemplateName, selectedTemplateIndex = myInputs.select_template("pkv")
    # else:
    #     templates, selectedTemplateName, selectedTemplateIndex = myInputs.select_template("project")

    #based on the selected template, figure out which ouptut folder to use
    selectedTemplatePath = os.path.join(template_pathRoot, "project_event_template.markdown")
    with open(selectedTemplatePath, 'r', encoding='utf-8') as f:
        templateContent = f.read()
        
    #get rid of unnecessary parts of the template name
    #templates should have a prefix that tells what group of template they belong to
    # and a suffix that shows they are a template
    noteType = "project_event_template.markdown" 
    templateNamePartsToReplace = ["PKV_","project_", "_template.markdown", "_template.md"]
    for part in templateNamePartsToReplace:
        noteType = noteType.replace(part, "")


    csv_file_path = os.path.join(os.path.dirname(__file__), 'EventsExample.csv')
    events_dict = {}

    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as csvFile:
        reader = csv.DictReader(csvFile)
        for row in reader:
            key = len(events_dict)
            events_dict[key] = row
        
    requiredKeys = ["date","Project Name","Title","Event Description"]  

    for key in requiredKeys:
        if key not in events_dict[1]:
            print(f"{myTerminal.ERROR}Missing required key: {key} in the selected note.{myTerminal.RESET}")
            print("\tCSV must include the following keys:",requiredKeys)
            exit(1)
    
    for eventDict in events_dict.values():
        selectedProjectName = eventDict.get("Project Name", "").strip()
        
        #make sure the new note directory directory exists
        if selectedProjectName == "" or selectedProjectName is None:
            #project selected, save in the project folder
            newNote_directory = myPreferences.root_pkv()
        else:
            #project not selected, save in the root of the PKV            
            newNote_directory = os.path.join(myPreferences.root_projects(), selectedProjectName)
        
        os.makedirs(newNote_directory, exist_ok=True)

        timestamp_id, title, note_Content = myInputs.get_templateMerge_Values_From_ExistingData(eventDict,templateContent)
        
        titleLettersAndNumbers = re.sub(r'[^A-Za-z0-9_\-\s]', '', title)[:200]  # Limit to 200 characters and remove special characters
        uniqueIdentifier = myTools.generate_unique_identifier (timestamp_id,noteType,titleLettersAndNumbers)
     
        # Construct the output filename and path
        output_filename = f"{uniqueIdentifier}.md"
        output_path = os.path.join(newNote_directory, output_filename)

        # Save the new note
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(note_Content)

        print(f"{myTerminal.SUCCESS}Note created:{myTerminal.RESET} {output_path}")
        if noteType != "event" or myPreferences.automatically_open_event_notes():
            os.system(f'{myPreferences.default_editor()} "{output_path}"')

if __name__ == "__main__":
    main()
    print(f"{myTerminal.SUCCESS}Done!{myTerminal.RESET}")