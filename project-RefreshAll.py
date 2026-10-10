#!/usr/bin/env python3

import os
import shutil
from datetime import datetime,date, timedelta
import re
from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Projects as myProjects
from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Notes import addLine

myTerminal.clearTerminal()
print(f"Preparing list of projects in {myPreferences.root_projects()}")

# iterate through the project folder and find each project folder
for filename in sorted(os.listdir(myPreferences.root_projects())):
    if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
        projectConfig = myProjects.get_ProjectConfig_as_dict(filename)
        projectName = projectConfig.get("ProjectName","")
        NeedsWeeklyProgressUpdate = projectConfig.get("Needs Weekly Progress Update", False)

        if NeedsWeeklyProgressUpdate:
            myTerminal.executePythonScript("""project-refreshHubnote.py""", projectName)

 
