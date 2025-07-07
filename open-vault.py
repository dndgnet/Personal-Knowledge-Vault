#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences


#open the preferences file in the default editor
os.system(f'{myPreferences.default_editor()} "{myPreferences.root_pkv()}"')
print(f"Vault '{myPreferences.root_pkv()}' opened in the default editor.")
