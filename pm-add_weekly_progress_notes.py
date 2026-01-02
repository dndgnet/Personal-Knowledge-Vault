import os 
import json
from _library import Tools as myTools, Inputs as myInputs

projects = myTools.get_pkv_projects()
projectThatNeedsWeeklyProgressNoteFound = False

for projectName in projects.keys():
    projectPath = projects[projectName]
    if os.path.exists(projectPath):
        print(f"Processing project: {projectName}")
        if os.path.exists(os.path.join(projectPath, ".ProjectConfig.json")):
            projectConfig = json.load(open(os.path.join(projectPath, ".ProjectConfig.json"), 'r'))
            archived = projectConfig.get("Archived", False)
            needsWeeklyUpdate = projectConfig.get("Needs Weekly Progress Update", False)
            if not projectConfig.get("Archived",False) and projectConfig.get("Needs Weekly Progress Update", False):
                projectThatNeedsWeeklyProgressNoteFound = True
                print(f"{projectName} is active and should get a weekly progress note.")
                if myInputs.ask_yes_no_from_user(f"Do you want to add a progress note for project '{projectName}'?", default = True):
                    #if windows use f'py add-projectProgressNote.py "{projectName}"'
                    if os.name == 'nt':
                        os.system(f'py add-projectProgressNote.py "{projectName}"')
                    else:
                        #if macOS or linux use:
                        os.system(f'./add-projectProgressNote.py "{projectName}"')
    else:
        print(f"Project path does not exist: {projectPath}")

if not projectThatNeedsWeeklyProgressNoteFound:
    print("No active projects found that need weekly progress updates.")