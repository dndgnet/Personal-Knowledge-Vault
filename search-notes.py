#!/usr/bin/env python3
import datetime 
import os 

from _library import Preferences as myPreferences, Tools as myTools, Terminal as myTerminal, Inputs as myInputs, HTML as myHTML, Summary as mySummary
from _library import Search as mySearch
import sys

# build a dictionary of all notes in the root_pkv directory
allNotes = myTools.get_Notes_as_list(myPreferences.root_pkv())
if not myTools.dump_notes_to_json(notes=allNotes, file_path=os.path.join(myPreferences.root_pkv(), "AllNotes.json"), indent=4):
    print(f"{myTerminal.ERROR}Failed to create AllNotes.json.{myTerminal.RESET}")
    exit(-1)

#retrieve the dictionary of all notes from AllNotes.json
allNotes = []
allNotes = myTools.load_notes_from_json(file_path = os.path.join(myPreferences.root_pkv(), "AllNotes.json"))

print(f"{len(allNotes)} notes loaded, start providing search criteria.")
print("")
print("-"*40)

searchLog = "Search Log\n"
continueSearch = True
searchIndex = 0
searchHistory = {}
searchResult = allNotes.copy()
searchHistory[searchIndex] = allNotes.copy()  # Store the initial state of all notes


def selectSearchResultNote(searchResult) -> str:
    i = 0
    print(f"\t{myTerminal.BLUE}{' id ':>4}  {'Datetime':<20} {'Project':<31} {'Note Title':<31}{myTerminal.RESET}")
    print(f"\t{myTerminal.BLUE}{'____':>4}  {'________':<20} {'_______':<31} {'__________':<31}{myTerminal.RESET}")
    searchResult.sort(key=lambda note: note.date, reverse=True)
    for note in searchResult:
        i += 1
        print(f"\t{myTerminal.GREY}{i:>4}) {note.date:<20} {note.project[:30]:<31} {note.title[:30]:<31}{myTerminal.RESET}")
    print("")
    print(f"\t{myTerminal.GREY}{'a':>4}) open All {myTerminal.RESET}")
    print(f"\t{myTerminal.GREY}{'x':>4}) eXport search result timeline {myTerminal.RESET}")

    selectedNote = input(f"{myTerminal.WHITE}\tEnter the note id to open or enter to continue searching: {myTerminal.RESET}").strip()
    return selectedNote

def listSearchResults(searchResult, feedbackMessage=""):
    myTerminal.clearTerminal()
    if feedbackMessage != "":
        print(f"{myTerminal.INFORMATION}{feedbackMessage}{myTerminal.RESET}\n") 

    selectedNote = selectSearchResultNote(searchResult)

    if selectedNote.lower() == 'q':
        quitSearch(searchLog)
    elif selectedNote.lower() == 'a':
        for noteToOpen in searchResult:
            #os.system(f"""{myPreferences.default_editor()} "{noteToOpen.filePath}" """)
            myTools.open_note_in_editor(noteToOpen.filePath)
    elif selectedNote == 'x':
        
        searchLogTemp = searchLog.replace("Search Log \n","")
        resultsDescription = "" 
        for line in searchLogTemp.splitlines():
            resultsDescription += f"\t{line[len('2025-07-16 20:13:00.674325:'):]}\n\n"


        summary = mySummary.generate_summary(
            summaryTitle = "Search Timeline",
            searchDescription = resultsDescription,
            notes = searchResult,
            includeBodyInTimeline = True,
            includeBackLinkInTimeline = True,
            includeGannt = True
        )

        # use the dot prefix to hide the file in the project directory (at least in civilized file managers)
        output_path = os.path.join(myPreferences.root_pkv(), "_" + datetime.datetime.now().strftime("%Y-%m-%d") + " Search Timeline.md" )

        if os.path.exists(output_path):
            print(f"{myTerminal.WARNING}Search TimeLine already exists: {output_path}{myTerminal.RESET}")
            if not myInputs.ask_yes_no("Do you want to overwrite it?", default=True):
                print(f"{myTerminal.INFORMATION}Exiting without changes.{myTerminal.RESET}")
                exit(0)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(summary)
            
        print("open search timeline summary in default editor...")    
        myTools.open_note_in_editor(output_path)

        print("open search timeline summary as html in default browser...')")
        myHTML.openMarkDownFileInBrowser(output_path)


    elif selectedNote.isdigit() and 1 <= int(selectedNote) <= len(searchResult):
        selectedNote = int(selectedNote) - 1
        noteToOpen = searchResult[selectedNote]
        #os.system(f"""{myPreferences.default_editor()} "{noteToOpen.filePath}" """)
        myTools.open_note_in_editor(noteToOpen.filePath)
        listSearchResults(searchResult,feedbackMessage=f"Opened note: {noteToOpen.title}")

    mySearch.describe_search_results("list results",searchResult)
    
def quitSearch(searchLog):
    searchLog += f"{datetime.datetime.now()}: quit search.\n"
    
    # save searchLog to search.log in the root_pkv directory for potential troubleshooting
    searchLogPath = os.path.join(myPreferences.root_pkv(), "search.log")
    with open(searchLogPath, 'w') as log_file:
        log_file.write(searchLog)
    
    exit("Exiting search.")


# collect input parameters
if len(sys.argv) > 1:
    print ("debug args:",' '.join(sys.argv[1:]))
    args = sys.argv[1:]

    searchPart = ""
    for p in range(0,len(args)):
        if args[p] == "-b":
            searchPart = args[p+1] if p+1 < len(sys.argv) else ""
            searchCriteria, searchResult = mySearch.search_body(searchResult, searchPart)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
        elif args[p] == "-p":
            searchPart = args[p+1] if p+1 < len(sys.argv) else ""
            searchCriteria, searchResult = mySearch.search_project(searchResult, searchPart)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
        elif args[p] == "-np":
            searchCriteria, searchResult = mySearch.search_no_project(searchResult)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
        elif args[p] == "-d":
            startDate = args[p+1] if p+1 < len(sys.argv) else ""
            endDate = args[p+2] if p+2 < len(sys.argv) else ""
            searchCriteria, searchResult = mySearch.search_date(searchResult, startDate, endDate)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
        elif args[p] == "-lastweek":
            startDate = (datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 7)).strftime('%Y-%m-%d')
            endDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            searchCriteria, searchResult = mySearch.search_date(searchResult, startDate, endDate)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
        elif args[p] == "-lastmonth":
            startDate = datetime.date(datetime.datetime.now().year if datetime.datetime.now().month > 1 else datetime.datetime.now().year - 1, datetime.datetime.now().month - 1 if datetime.datetime.now().month > 1 else 12, 1).strftime('%Y-%m-%d')
            endDate = datetime.date(datetime.datetime.now().year, datetime.datetime.now().month, 1).strftime('%Y-%m-%d')
            searchCriteria, searchResult = mySearch.search_date(searchResult, startDate, endDate)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)

        elif args[p] == "-today":
            startDate = datetime.datetime.now().strftime('%Y-%m-%d')
            endDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            searchCriteria, searchResult = mySearch.search_date(searchResult, startDate, endDate)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
        elif args[p] == "-yesterday":
            startDate = (datetime.datetime.now() - datetime.timedelta(days=datetime.datetime.now().weekday() + 1)).strftime('%Y-%m-%d')
            endDate = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
            searchCriteria, searchResult = mySearch.search_date(searchResult, startDate, endDate)
            searchHistory[searchIndex] = searchResult.copy()
            searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
            mySearch.describe_search_results(searchCriteria,searchResult)
else:
    mySearch.describe_search_results("", searchResult)

while continueSearch:
    print ("\nSearch options:")
    print ("\t p)  project - Search by project")
    print ("\t np) No project - Search for notes not attached to  project")
    print ("\t d)  date range - Search by note date")
    print ("\t ta) tags - Search by tags")
    print ("\t ti) title - Search by title")
    print ("\t b)  body - Search by body text")
    print ("\t","-"*20)
    print ("Commands:")
    print ("\t h)  history - show search history")
    print ("\t u)  undo - undo the last search")
    print ("\t l)  list - list current search results")
    print ("\t x)  export - export and open results in editor")
    print ("\t q)  quit - Quit the search")
    print ("\t","-"*20)
    
    inputChoice = input("Enter your choice: ").strip().lower()
    
    if inputChoice == 'q':
        quitSearch(searchLog)

    elif inputChoice =='p':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_project(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
        mySearch.describe_search_results(searchCriteria,searchResult)

    elif inputChoice =='np':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_no_project(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
        mySearch.describe_search_results(searchCriteria,searchResult)
        
    elif inputChoice =='ta':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_tags(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
        mySearch.describe_search_results(searchCriteria,searchResult)

    elif inputChoice =='d':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_date(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
        mySearch.describe_search_results(searchCriteria,searchResult)

    elif inputChoice =='ti':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_title(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
        mySearch.describe_search_results(searchCriteria,searchResult)

    elif inputChoice =='b':
        searchIndex += 1
        searchCriteria, searchResult = mySearch.search_body(searchResult)
        searchHistory[searchIndex] = searchResult.copy()
        searchLog += f"{datetime.datetime.now()}: {searchCriteria}  ({len(searchResult)} records)\n"
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
    
    elif inputChoice == 'h':
        for line in searchLog.splitlines():
            print(f"{myTerminal.GREY}{line[len('2025-07-16 20:13:00.674325:'):]}{myTerminal.RESET}")
             
    elif inputChoice == 'l':
        listSearchResults(searchResult)

    elif inputChoice == 'x':
        searchResultBody = f"""---
title: Search Results 
date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
---

# Search Results {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        for note in searchResult:
            searchResultBody += f"\n## {note.title}\n"
            searchResultBody += f"**Project:** {note.project}\n"
            searchResultBody += f"**Date:** {note.date}\n"
            searchResultBody += f"**Tags:** {', '.join(note.tags) if note.tags else 'No tags'}\n"
            searchResultBody += f"**Link:** [[{note.id}]]\n"
            searchResultBody += "\n\n"
            searchResultBody += f"{note.noteBody.replace('---','')}\n\n"
        
        searchResultFilePath = os.path.join(myPreferences.root_pkv(), ".SearchResults.md")
        with open(searchResultFilePath, 'w',encoding='utf-8') as file:
            file.write(searchResultBody)
        
        continueSearch = False    
        print(f"{myTerminal.INFORMATION}Search results saved to {searchResultFilePath}{myTerminal.RESET}")
        os.system(f"""{myPreferences.default_editor()} "{searchResultFilePath}" """)

        break
    
    else:
        print(f"{myTerminal.WARNING}Invalid choice. Please try again.{myTerminal.RESET}")
        continue