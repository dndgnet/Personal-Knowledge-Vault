#!/usr/bin/env python3

import os 
import datetime

from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 


print(f"{myTerminal.INFORMATION}Diagram a tag...{myTerminal.RESET}\n")

print("Available tags:") 
selectedTag = myInputs.select_tag()

allNotes = myTools.get_Notes_as_list(myPreferences.root_pkv())