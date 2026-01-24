#!/usr/bin/env python3
from _library import Preferences as myPreferences, Tools as myTools, Terminal as myTerminal
import os 
def main():
    
    print("PKV Root Directory:", myPreferences.root_pkv())
    print("Preferences Path:", myPreferences.preferences_Path)
    print("Preferences:")
    for key, value in myPreferences._preferences.items():
        print(f"\t{key}: {value}")
    myTerminal.print_separator()

    #get size on disk of the vault
    vault_size = 0
    for dirpath, dirnames, filenames in os.walk(myPreferences.root_pkv()):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                vault_size += os.path.getsize(filepath)
    vault_size_gb = vault_size / (1024**3)
    
    print(f"Vault Size: {vault_size_gb:.2f} GB")
    myTerminal.print_separator()

    _ = input("Press Enter to see project and attachment details...")

    projects = myTools.get_pkv_projects()
    print("Projects Directory:", myPreferences.root_projects())
    print("Number of Projects:", len(projects))
    for key, values in projects.items():
        myTerminal.printWithoutLineWrap("    ",f"{key}: {values}")
        print("")

    myTerminal.print_separator()
    attachments = myTools.get_pkv_attachments()
    print("Attachments Directory:", myPreferences.root_attachments())
    print("Number of Attachments:", len(attachments))
    for key, value in attachments.items():
        myTerminal.printWithoutLineWrap("    ",f"{key}")
        print("")


if __name__ == "__main__":
    main()
    