#!/usr/bin/env python3

import os
import re
from datetime import datetime

#my stuff
from _library import Preferences as myPreferences
from _library import Inputs as myInputs
from _library import Terminal as myTerminal

# Define the template and output paths
template_pathRoot = os.path.join(os.getcwd(),"_templates")


def main():
    projects, selectedProjectName, selectedProjectIndex = myInputs.get_project_name()
    templates, selectedTemplateName, selectedTemplateIndex = myInputs.get_template()

    #based on the selected template, figure out which ouptut folder to use
    selectedTemplatePath = os.path.join(template_pathRoot, selectedTemplateName)
    
    #get rid of unnecessary parts of the template name
    #templates should have a prefix that tells what group of template they belong to
    # and a suffix that shows they are a template
    noteType = selectedTemplateName 
    templateNamePartsToReplace = ["project_", "_template.markdown", "_template.md"]
    for part in templateNamePartsToReplace:
        noteType = noteType.replace(part, "")

    #originally all templates got their own subfolder, in practice this is messy
    #so now only some special templates get their own subfolder
    templatesThatNeedSubFolder = ["meeting","status"]
    if noteType not in templatesThatNeedSubFolder:    
        noteSubFolder = ""
    else:
        noteSubFolder = f"{noteType}s"
    
    #make sure the new note directory directory exists            
    newNote_directory = os.path.join(myPreferences.root_projects(), selectedProjectName, noteSubFolder)
    os.makedirs(newNote_directory, exist_ok=True)

    #collect information that should be seeded into the note fields
    selectedDateTime = myInputs.get_datetime_from_user("Enter the date and time for the note (or leave blank for system default):",datetime.now())
    timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
    timestamp_date = selectedDateTime.strftime(myPreferences.date_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())
    

    # Read the template content
    with open(selectedTemplatePath, 'r', encoding='utf-8') as f:
        templateBody  = f.read()
    
    note_Content = templateBody.strip()
    templateTags = re.findall(r"\[(.*?)\]", note_Content)
    templateTags = set(templateTags)  # remove duplicates
    for templateTag in templateTags:
        templateTagValue = ""
        if "[" in templateTag:
            pass  # skip malformed tags and images
        if templateTag.strip() == "":
            pass
        elif templateTag.upper() == "YYYYMMDDHHMMSS":
            templateTagValue = timestamp_id
        elif templateTag.upper() == "YYYY-MM-DD HH:MM:SS":
            templateTagValue = timestamp_full
        elif templateTag.upper() in ("YYYY-MM-DD","DATE"):
            templateTagValue = timestamp_date
        elif templateTag in ("Project Name","ProjectName","Project"):
            templateTagValue = selectedProjectName
        elif templateTag in ("Current User","User","Username"):
            templateTagValue = os.getlogin()
        elif templateTag in ["tags","Tags","TAGS"]:
            templateTagValue = input(f"{myTerminal.INPUTPROMPT}Enter tags (comma-separated) or leave blank for none: {myTerminal.RESET}").strip()
            tags = ""
            for tag in templateTagValue.split(","):
                tag = tag.strip()
                tags += f"#{tag} "
            templateTagValue = tags
        else:
            templateTagValue = input(f"{myTerminal.INPUTPROMPT}Enter value for [{templateTag}]: {myTerminal.RESET}").strip()

        note_Content = note_Content.replace(f"[{templateTag}]", templateTagValue)
    
    # Construct the output filename and path
    output_filename = f"{timestamp_id}_{noteType}.md"
    output_path = os.path.join(newNote_directory, output_filename)

    # Save the new note
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(note_Content)

    print(f"{myTerminal.SUCCESS}Note created:{myTerminal.RESET} {output_path}")
    os.system(f'{myPreferences.default_editor()} "{output_path}"')

if __name__ == "__main__":
    main()
    print(f"{myTerminal.SUCCESS}Done!{myTerminal.RESET}")