#!/usr/bin/env python3

import os
import re
from datetime import datetime
from urllib.parse import quote

#my stuff
from _library import Preferences as myPreferences
from _library import Inputs as myInputs
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library import VersionControl as myVersionControl

def main():
    """
    Rename a Project.

    """

    print(f"{myTerminal.CYAN}Rename Project Script{myTerminal.RESET}\n")
    print("Select the project to rename:")
    oldProjectName = myInputs.select_project_name(showNewProjectOption=False,showNoProjectOption=False)
    if oldProjectName == "":
        print(f"{myTerminal.ERROR}Cannot rename 'No Project'. Operation cancelled.{myTerminal.RESET}")
        exit(1)

    newProjectName = input(f"Enter the new name for the project '{oldProjectName}': ").strip()

    #if projectNameNew does exist, exit
    if os.path.exists(os.path.join(myPreferences.root_projects(),newProjectName)):
        print(f"{myTerminal.ERROR}Project folder '{newProjectName}' already exists. Cannot rename to an existing project name.{myTerminal.RESET}")
        exit(1)

    #dougle check    
    if input(f"Are you sure you want to rename project '{oldProjectName}' to '{newProjectName}'? (y/n): ").lower() != 'y':
        print(f"{myTerminal.WARNING}Operation cancelled by user.{myTerminal.RESET}")
        exit(0)
    
    for note in myTools.get_Notes_as_list(myPreferences.root_pkv()):
        newFrontMatter = note.frontMatter
        newBody = note.noteBody 

        #replace project name in front matter of all notes in the project folder
        newFrontMatter = re.sub(r'project:\s*.*(?=$|\s)', f'project: {newProjectName}', newFrontMatter)

        #replace project name tags in front matter
        oldTag = myTools.generate_tag_from_projectName(oldProjectName)
        newTag = myTools.generate_tag_from_projectName(newProjectName)

        #replace project tag in front matter when followed by space, comma, semicolon, or end of line
        #Front matter might have comma separated tags rather than the hashtag format
        newFrontMatter = re.sub(f'{oldTag.replace("#","")}(?=$|\\s|,|;)', f'{newTag.replace("#","")}', newFrontMatter)

        #replace tag in body when followed by space, comma, semicolon, or end of line
        newBody = re.sub(f'{oldTag}(?=$|\\s|,|;)', f'{newTag}', newBody)

        #replace backlinks [[]]
        oldProjectName_url = quote(oldProjectName)
        newProjectName_url = quote(newProjectName)
        
        newBody = re.sub(r'\[\[' + oldProjectName_url + r'(?=\]\])',
            f'[[{newProjectName_url}',
            newBody,
            flags=re.IGNORECASE
        )

        #replace Project: <progect name> pattern in body
        newBody = re.sub(r'Project:\s*' + re.escape(oldProjectName),
                        f'Project: {newProjectName}',
                        newBody,
                        flags=re.IGNORECASE
                        )

        #replace links ()[]
        newBody = re.sub(r'' + oldProjectName_url + r'/', 
                        f'{newProjectName_url}/', 
                        newBody,
                        flags=re.IGNORECASE
                        )
    
        if note.frontMatter != newFrontMatter or note.noteBody != newBody:
            #need a new note
            print(f"updating {note.fileName}")
            newNoteContent = f"---\n{newFrontMatter}\n---\n\n{newBody}"
            
            with open(note.filePath, 'w', encoding='utf-8') as f:
                f.write(newNoteContent)

            #for debugging
            #myTools.open_note_in_editor(note.filePath)
        
    #rename project folder
    newProjectPath = os.path.join(myPreferences.root_projects(),newProjectName)
    os.rename(os.path.join(myPreferences.root_projects(),oldProjectName),newProjectPath)

if __name__ == "__main__":
    main()
    print(f"{myTerminal.SUCCESS}Done!{myTerminal.RESET}")