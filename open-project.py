#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences
from _library import Inputs as myInputs

selectedProject = myInputs.select_project_name(False, False)

projectPath = os.path.join(myPreferences.root_projects(), selectedProject)

if myPreferences.default_editor() != "obsidian":
    #open the preferences file in the default editor
    os.system(f'{myPreferences.default_editor()} "{projectPath}"')
    print(f"Vault '{myPreferences.root_pkv()}' opened in the default editor.")
else:
    # For Obsidian, open the vault and the specific note
    vaultName = myPreferences.root_pkv().split("/")[-1]
    openCmd = f"obsidian://advanced-uri?vault={vaultName}"
    os.system(f'open "{openCmd}"')
    

