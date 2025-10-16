#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences

if myPreferences.default_editor() != "obsidian":
    #open the preferences file in the default editor
    os.system(f'{myPreferences.default_editor()} "{myPreferences.root_pkv()}"')
    print(f"Vault '{myPreferences.root_pkv()}' opened in the default editor.")
else:
    # For Obsidian, open the vault and the specific note
    vaultName = myPreferences.root_pkv().split("/")[-1]
    openCmd = f"obsidian://advanced-uri?vault={vaultName}"
    os.system(f'open "{openCmd}"')
    

