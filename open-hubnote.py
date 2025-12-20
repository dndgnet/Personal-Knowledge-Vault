#!/usr/bin/env python3
import os
from _library import Preferences as myPreferences
from _library import Terminal as myTerminal
from _library import Inputs as myInputs


selectedNoteIndex, note = myInputs.select_recent_note(noteTypeContains="Hub",  showActionItems=True, DaysToGoBack=3000)

if selectedNoteIndex != 0:
    #open the preferences file in the default editor
    os.system(f'{myPreferences.default_editor()} "{note.filePath}"')
    print(f"Note '{note.title}' opened in the default editor.")
