import datetime 
from typing import List, Tuple

from . import Preferences as myPreferences, Inputs as myInputs, Terminal as myTerminal, Tools as myTools
from .Tools import NoteData

def describe_search_results(searchCriteria: str, notes: List[NoteData]) -> None:
    """
    Print a description of the search results.

    Args:
        searchCriteria (str): The search criteria description.
        notes (List[NoteData]): List of NoteData objects.
    """
    print("")
    myTerminal.clearTerminal()
    if searchCriteria != "":
        print(f"{myTerminal.INFORMATION}Search {searchCriteria}{myTerminal.RESET}")
    
    if not notes:
        print(f"{myTerminal.WARNING}No notes found matching the search criteria.{myTerminal.RESET}")
        return

    print(f"\t\tFound {len(notes)} notes matching the search criteria.")
    print("")
    
def search_project(notes: List[NoteData]) -> Tuple[str, List[NoteData]]:
    """
    Search for notes in the given list that match the specified project.

    Args:
        notes (List[NoteData]): List of NoteData objects.

    Returns:
        Tuple[str, List[NoteData]]: A tuple containing the search description and filtered notes.
    """
    
    _, selectedProject, _ = myInputs.select_project_name_withDict(showNewProjectOption=False)
    results = []
    if selectedProject is None or selectedProject == "":
        return "none, no project selected", notes
    else:
        for note in notes:
            if note.project == selectedProject:
                results.append(note)
        return f"project = {selectedProject}", results

def search_no_project(notes: List[NoteData]) -> Tuple[str, List[NoteData]]:
    """
    Search for notes in the given list that are not assigned to any project.

    Args:
        notes (List[NoteData]): List of NoteData objects.

    Returns:
        Tuple[str, List[NoteData]]: A tuple containing the search description and filtered notes.
    """
    
    results = []
    for note in notes:
        if note.project == "":
            results.append(note)
    return "project = None", results

def search_date(notes: List[NoteData]) -> Tuple[str, List[NoteData]]:
    """
    Search for notes in the given list that match the specified date range.

    Args:
        notes (List[NoteData]): List of NoteData objects.

    Returns:
        Tuple[str, List[NoteData]]: A tuple containing the search description and filtered notes.
    """
    
    userInput = input("Enter start date (YYYY-MM-DD) or leave blank for no start date: ")
    isDate, startDate = myTools.datetime_fromString(userInput)
    if not isDate:
        startDate = datetime.datetime(year = 1899,month = 1, day =1)
        
    userInput = input("Enter end date (YYYY-MM-DD) or leave blank for no end date: ")
    isDate, endDate = myTools.datetime_fromString(userInput)
    if not isDate:
        endDate = datetime.datetime.now()
    
    # truncate startDate to the beginning of the day
    # and convert to a string
    startDate = startDate.replace(hour=0, minute=0, second=0, microsecond=0).strftime(myPreferences.datetime_format())  
    endDate = endDate.replace(hour=23, minute=59, second=59, microsecond=999999).strftime(myPreferences.datetime_format())
    
    results = []
    for note in notes:
        noteDate = note.date
        if startDate <= noteDate <= endDate:
            results.append(note)
            
    return f"date range from {startDate} to {endDate}", results

def search_title(notes: List[NoteData]) -> Tuple[str, List[NoteData]]:
    """
    Search for notes in the given list that match the specified title.

    Args:
        notes (List[NoteData]): List of NoteData objects.

    Returns:
        Tuple[str, List[NoteData]]: A tuple containing the search description and filtered notes.
    """
    
    titlePart = input("Enter a part of the title to search for (or leave blank for no title search): ").lower().strip()
    
    results = []
    if titlePart is None or titlePart == "":
        return "none, no title selected", notes
    else:
        for note in notes:
            if titlePart in note.title.lower():
                results.append(note)
        return f"title contains '{titlePart}'", results

def search_body(notes: List[NoteData]) -> Tuple[str, List[NoteData]]:
    """
    Search for notes in the given list that match the specified body content.

    Args:
        notes (List[NoteData]): List of NoteData objects.

    Returns:
        Tuple[str, List[NoteData]]: A tuple containing the search description and filtered notes.
    """
    
    searchPart = input("Enter a part of the body to search for (or leave blank for no body search): ").lower().strip()
    
    results = []
    if searchPart is None or searchPart == "":
        return "none, no search part provided", notes
    else:
        for note in notes:
            if searchPart in note.noteBody.lower():
                results.append(note)
        return f"body contains '{searchPart}'", results
    
def search_tags(notes: List[NoteData]) -> Tuple[str, List[NoteData]]:
    """
    Search for notes for a given tag.

    Args:
        notes (List[NoteData]): List of NoteData objects.

    Returns:
        Tuple[str, List[NoteData]]: A tuple containing the search description and filtered notes.
    """
     
    selectedTag = myInputs.select_tags_from_noteList(notes)
    
    if selectedTag is not None and selectedTag != "":
        results = []
        for note in notes:
            if note.tags and selectedTag in note.tags:
                results.append(note)
        return f"note tags include {selectedTag}", results
    else:
        return "none, no tag selected", notes
  