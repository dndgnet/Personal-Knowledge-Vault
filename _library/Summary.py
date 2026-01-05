import datetime
from decimal import Decimal

from . import Preferences as myPreferences, Tools as myTools, Projects as myProjects
from .Notes import NoteData, sort_Notes_by_date

def actuals_graph(actuals: dict, budget: Decimal) -> str:
    """
    Generate a string representation of actuals for graphing.
    """
    graph = """
```mermaid
    xychart-beta
    title "Actuals"
"""
 
    x_axis = ""
    bar = ""
    line = ""
    min_yValue = 0 # min(actuals.values(), default=0)
    max_yValue = max(actuals.values(), default=0)
    
    if budget > max_yValue:
        max_yValue = budget * Decimal("1.1")
    
    y_axis = f""" "Actual Expense (in $)" {min_yValue} --> {max_yValue}\n"""

    # x-axis [jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec]
    # y-axis "Revenue (in $)" 4000 --> 11000
    # bar [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
    # line [5000, 6000, 7500, 8200, 9500, 10500, 11000, 10200, 9200, 8500, 7000, 6000]
 
    for date, value in sorted(actuals.items()):
        x_axis += f'"{date}", '
        line += f"{budget:.2f}, "
        bar += f"{value:.2f}, "
    
    graph += f"""
x-axis [{x_axis.strip(', ')}]
y-axis {y_axis}
line [{line.strip(', ')}]
bar [{bar.strip(', ')}]
```
"""
    return graph

def progress_graph(dictProgress: dict) -> str:
    """
    Generate a string representation of progress for graphing.
    """
    graph = """
```mermaid
    xychart-beta
    title "Reported Progress"
"""
 
    x_axis = ""
    bar = ""
    line = ""
    min_yValue = 0 # min(actuals.values(), default=0)
    max_yValue = 100
    
    #todo
    #include linear projection for for the bar chart

    y_axis = f""" "Progress (in %)" {min_yValue} --> {max_yValue}\n"""
 
    for date, value in sorted(dictProgress.items()):
        x_axis += f'"{date}", '
        line += f"{value:.2f}, "
        #bar += f"{plannedValue:.2f}, "
    
    graph += f"""
x-axis [{x_axis.strip(', ')}]
y-axis {y_axis}
line [{line.strip(', ')}]

```
"""
    return graph


def generate_summary(summaryTitle: str, searchDescription: str, 
                     notes: list[NoteData],
                     includeBodyInTimeline: bool, 
                     includeBackLinkInTimeline: bool, includeGantt: bool, 
                     includeTimelineAsList: bool) -> str:
    """
    Generate a project summary for the selected project based on the provided notes.

    Args:
        selectedProject (str): The name of the selected project.
        notes (list[NoteData]): List of NoteData objects related to the project.
    """

    #make sure notes are sorted by date descending
    notes = sort_Notes_by_date(notes, descending=True)

    timeLine = ""
    gantt = ""
    timelineAsList = ""

    for note in notes:
        note: NoteData = note  # type hint for better IDE support
        if "task" in note.type.lower():
            task = myProjects.loadTaskFromNote(note)
            startDate = task.plannedStart if task.actualStart == "" else task.actualStart
            startDate = task.date[:10] if startDate == "" else startDate 
            endDate = myTools.now_YYYY_MM_DD() if task.endDate == "" else task.endDate
            
            # build a timeline in descending order of date
            if not includeBackLinkInTimeline and not includeBodyInTimeline:
                timeLine += f"\n- {startDate} {note.type} {note.title}\n"
            else:
                timeLine += f"\n### {startDate} {note.type} {note.title}\n"
                
            if includeBodyInTimeline:
                timeLine += f"\n{myTools.remove_noteHeaders(note.noteBody)}\n"

            if includeBackLinkInTimeline:
                timeLine += f"\n[[{note.fileName}]]\n"
            
            if includeGantt: 
                if startDate == endDate:
                    gantt += f"{ myTools.letters_and_numbers_only(note.title)} : {startDate}, 1d\n"
                else:
                    gantt += f"{ myTools.letters_and_numbers_only(note.title)} : {startDate}, {endDate}\n"

            if includeTimelineAsList:
                timelineAsList += f"\n{startDate} - {note.title}\n\n"   


        else:
            # build a timeline in descending order of date
            if not includeBackLinkInTimeline and not includeBodyInTimeline:
                timeLine += f"\n- {note.date[:10]} {note.type} {note.title}\n"
            else:
                timeLine += f"\n### {note.date[:10]} {note.type} {note.title}\n"
                
            if includeBodyInTimeline:
                timeLine += f"\n{myTools.remove_noteHeaders(note.noteBody)}\n"

            if includeBackLinkInTimeline:
                timeLine += f"\n[[{note.fileName}]]\n"
            
            if includeGantt: 
                gantt += f"{ myTools.letters_and_numbers_only(note.title)} : {note.date}, 1d\n"

            if includeTimelineAsList:
                timelineAsList += f"\n{note.date[:10]} - {note.title}\n\n"   

    if includeGantt:
        gantt = f"""
        
## Timeline

```mermaid

gantt
    title {summaryTitle}
    dateFormat YYYY-MM-DD
    section Timeline

        {gantt}
    
```
"""
        
    if includeTimelineAsList:
        timelineAsList = f"""
## Timeline as List 
{timelineAsList}
"""
        
    summary = f"""
# {summaryTitle} \n\n

**prepared**: {datetime.datetime.now().strftime(myPreferences.date_format())}

**search description**: {searchDescription}

{gantt}

{timelineAsList}

## Notes
{timeLine}

"""

    return summary
