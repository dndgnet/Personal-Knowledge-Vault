#!/usr/bin/env python3
from _library import Preferences as myPreferences, Tools as myTools

def main():
    
    print("PKV Root Directory:", myPreferences.root_pkv())
    print("Preferences Path:", myPreferences.preferences_Path)
    print("Preferences:")
    for key, value in myPreferences._preferences.items():
        print(f"\t{key}: {value}")
    
    myTools.print_separator()
    projects = myTools.get_pkv_projects()
    print("Projects Directory:", myPreferences.root_projects())
    print("Number of Projects:", len(projects))
    for key, values in projects.items():
        print(f"\t{key}: {values}")

    myTools.print_separator()
    attachments = myTools.get_pkv_attachments()
    print("Attachments Directory:", myPreferences.root_attachments())
    print("Number of Attachments:", len(attachments))
    for key, value in attachments.items():
        print(f"\t{key}")


if __name__ == "__main__":
    main()
    