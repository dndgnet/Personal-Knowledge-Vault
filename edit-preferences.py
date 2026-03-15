#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences
from _library import Tools as myTool

examplePreferences = """
_exampleEmptyPreferences = {
    "pkv_root":"PKV", #root folder name of the personal knowledge vault
    "attachments_root":"_Attachments", #name of the folder in the PKV where attachments are stored
    "projects_root":"_Projects", #name of the folder in the PKV where projects are stored
    "archive_root":".Archive", #name of where soft deleted projects will be sent
    "timestamp_id_format":"%y%m%d%H%M%S", #format for note unique identifiers
    "date_format":"%Y-%m-%d", #format for displaying dates in notes
    "datetime_format":"%Y-%m-%d %H:%M:%S", #format for displaying date and time in notes
    "documents_path": "os default", #where documents are stored, use 'os default' to let the OS decide
    "attachmentPickUp_path": "os default", #where we can look for new attachment, use 'os default' to let the OS return the downloads folder
    "screenCapture_path": "os default", #where we can look for new screen captures, use 'os default' to let the OS return the screenshots folder
    "default_editor": "code" #default editor to use for opening files, can be 'code' for VS Code, 'zed' for Zed, or any other editor command
    }

"""

#open the preferences file in the default editor
if myPreferences.default_editor() == "obsidian":
    os.system(f'code "{myPreferences.preferences_File_Path}"')
else:
    os.system(f'{myPreferences.default_editor()} "{myPreferences.preferences_File_Path}"')    

print(examplePreferences)
