#!/usr/bin/env python3
import datetime 
import os 
import json

from _library import Preferences as myPreferences, Tools as myTools, Terminal as myTerminal
from _library import Search as mySearch

# build a dictionary of all notes in the root_pkv directory
allNotes = myTools.get_NoteFiles_as_dict(myPreferences.root_pkv())
with open(os.path.join(myPreferences.root_pkv(),"AllNotes.json"), 'w') as file:
    json.dump(allNotes, file, indent=4)


#retrieve the dictionary of all notes from AllNotes.json
allNotes = {}
allNotesJsonPath = os.path.join(myPreferences.root_pkv(), "AllNotes.json")
if os.path.exists(allNotesJsonPath):
    with open(allNotesJsonPath, 'r') as file:
        allNotes = json.load(file)

print(f"{len(allNotes)} notes loaded, start providing search criteria.")
print("")
print("-"*40)

searchLog = "Search Log\n"
continueSearch = True
searchIndex = 0
searchHistory ={}
searchResult = allNotes.copy()
searchHistory[searchIndex] = allNotes.copy()  # Store the initial state of all notes


while continueSearch:
    print ("Search options:")
    print ("\tp) project - Search by project")
    print ("\tt) tags - Search by tags")
    print ("\td) date range - Search by note date")
    print ("\ti) title - Search by title")
    print ("\tb) body - Search by body text")
    print ("\t","-"*20)
    print ("Commands:")
    print ("\tu) undo - undo the last search")
    print ("\tl) list - list current search results")
    print ("\tx) export - export results to editor note")
    print ("\tq) quit - Quit the search")
    print ("\t","-"*20)
    
    inputChoice = input("Enter your choice: ").strip().lower()
    if inputChoice == 'q':
        searchLog += f"{datetime.datetime.now()}: quit search.\n"
        continueSearch = False
        
        # save searchLog to search.log in the root_pkv directory for potential troubleshooting
        searchLogPath = os.path.join(myPreferences.root_pkv(), "search.log")
        with open(searchLogPath, 'w') as log_file:
            log_file.write(searchLog)
        
        print("Exiting search.")
        break
    elif inputChoice =='p':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_project(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}\n"
        mySearch.describe_search_results(searchCriteria,searchResult)
    elif inputChoice =='t':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_tags(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}\n"
        mySearch.describe_search_results(searchCriteria,searchResult)
    elif inputChoice =='d':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_date(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}\n"
        mySearch.describe_search_results(searchCriteria,searchResult)
    elif inputChoice =='i':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_title(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}\n"
        mySearch.describe_search_results(searchCriteria,searchResult)
    elif inputChoice =='b':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_body(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}\n"
        mySearch.describe_search_results(searchCriteria,searchResult)
    
    elif inputChoice == 'u':
        if searchIndex > 0:
            searchIndex -= 1
            searchResult = searchHistory[searchIndex]
            mySearch.describe_search_results("Undo last search", searchResult)
            searchLog += f"{datetime.datetime.now()}: undo\n"
            print(f"{myTerminal.INFORMATION}Undo to search index {searchIndex}{myTerminal.RESET}")
        else:
            print(f"{myTerminal.WARNING}No previous search to undo.{myTerminal.RESET}")      
    
    elif inputChoice == 'l':
        print(f"\t{myTerminal.INFORMATION}{'Datetime':<20} {'Project':<31} {'Note Title':<31}{myTerminal.RESET}")
        print(f"\t{myTerminal.INFORMATION}{'________':<20} {'_______':<31} {'__________':<31}{myTerminal.RESET}")
        for note_id, note in searchResult.items():
            print(f"\t{myTerminal.INFORMATION}{note.get('date',""):<20} {note.get('project','')[:30]:<31} {note.get('title', 'No title')[:30]:<31}{myTerminal.RESET}")
    
    elif inputChoice == 'x':
        searchResultBody =f"""
        ---
        title: Search Results 
        date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        ---
        
# Search Results {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        """
        for note_id, note in searchResult.items():
            searchResultBody += f"\n## {note.get('title', 'No title')}\n"
            searchResultBody += f"**Project:** {note.get('project', 'No project')}\n"
            searchResultBody += f"**Date:** {note.get('date', 'No date')}\n"
            searchResultBody += f"**Tags:** {note.get('tags', 'No tags')}\n"
            searchResultBody += "\n\n"
            searchResultBody += f"{note.get('noteBody', 'No body text').replace("---","")}\n\n"
        
        searchResultFilePath = os.path.join(myPreferences.root_pkv(), ".SearchResults.md")
        with open(searchResultFilePath, 'w') as file:
            file.write(searchResultBody)
        
        continueSearch = False    
        print(f"{myTerminal.INFORMATION}Search results saved to {searchResultFilePath}{myTerminal.RESET}")
        os.system(f"{myPreferences.default_editor()} {searchResultFilePath}")
        break
    
    else:
        print(f"{myTerminal.WARNING}Invalid choice. Please try again.{myTerminal.RESET}")
        continue