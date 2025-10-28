#!/usr/bin/env python3

"""
Build Project Summary Script

This script generates a comprehensive project summary report by analyzing notes and progress data 
for a selected project. It creates visualizations including actuals vs budget graphs, progress 
tracking charts, and optional Gantt charts, then outputs everything to a markdown file.

Main Features:
- Interactive project selection from available projects
- Extracts budget, actuals, and progress data from project notes
- Generates Mermaid charts for financial tracking and progress visualization
- Creates chronological timeline of project activities
- Optional Gantt chart generation for project scheduling
- Outputs formatted markdown report with embedded visualizations
- Automatically opens the generated report in default editor and browser

The script processes different types of notes:
- Hub/project-hub notes: Contains project governance and budget information
- Progress/project-progress notes: Contains completion percentage and actual expenses
- General project notes: Included in timeline for comprehensive project history

Output includes:
- Project governance section with budget vs actuals
- Visual charts (when sufficient data exists)
- Latest progress update
- Chronological timeline of all project activities
- Optional Gantt chart for project planning
The generated report is saved as '.ProjectSummary.md' in the project directory.
"""


import os 
import datetime
from decimal import Decimal

from _library import Terminal as myTerminal
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 
from _library import HTML as myHTML

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
    
#     graph += f"""
# x-axis [{x_axis.strip(', ')}]
# y-axis {y_axis}
# line [{line.strip(', ')}]
# bar [{bar.strip(', ')}]
# ```
# """

    return graph

print(f"{myTerminal.INFORMATION}Prepare a project summary...{myTerminal.RESET}\n")

print("Available projects:") 
selectedProject = myInputs.select_project_name(False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)
    
notesAll = myTools.get_Notes_as_list(myPreferences.root_pkv())
notes = []

for note in notesAll:
    if note.project == selectedProject:
        notes.append(note)
    elif f"p_{selectedProject}" in note.tags:
        notes.append(note)
        print("debug project is a note", note.title)

notes = myTools.sort_Notes_by_date(notes, descending=True)

includeBodyInTimeline = myInputs.ask_yes_no("Include body in timeline?", default=False)
includeBackLinkInTimeline = myInputs.ask_yes_no("Include backlinks in timeline?", default=False)
includeGannt = myInputs.ask_yes_no("Include Gantt chart?", default=False)
 
hubNote = ""
progressBody = ""
timeLine = ""
gantt = ""

budgetStr = ""
budgetDecimal = Decimal("0.00")

actualsStr = ""
actualsDecimal = Decimal("0.00")
dictActuals = {}

progressStr = ""
progressDecimal = Decimal("0.00")
dictProgress = {}


for note in notes:
    note: NoteData = note  # type hint for better IDE support
    
    # find the hub note status update note, put it at the top of the output
    if hubNote == "" and (note.type == "hub" or note.type == "project-hub"):
        budgetStr = myTools.get_stringValue_from_noteBody("**Budget Amount:**", note.noteBody)
        budgetDecimal = myTools.decimal_from_string(budgetStr)
        hubNote = myTools.remove_noteHeaders(note.noteBody)
        print(f"{myTerminal.SUCCESS}Found hub note: {note.title}{myTerminal.RESET}")
        continue 

    # find the latest status update note, put it at the top of the output
    if (note.type == "progress" or note.type == "project-progress"):

        progressDate = note.date[:10]  # Extract date part from datetime string
        progressActualsStr = myTools.get_stringValue_from_noteBody("**Actuals:**", note.noteBody)
        progressActualsDecimal = myTools.decimal_from_string(progressActualsStr)
        if progressActualsDecimal != Decimal("0.00"):
            dictActuals[progressDate] = progressActualsDecimal

        if progressBody == "":
            actualsStr = progressActualsStr
            actualsDecimal = progressActualsDecimal
            progressBody = myTools.remove_noteHeaders(note.noteBody)
            print(f"{myTerminal.SUCCESS}Found progress note: {note.title}{myTerminal.RESET}")

        progressStr = myTools.get_stringValue_from_noteBody("**Complete:**", note.noteBody)
        progressDecimal = myTools.decimal_from_string(progressStr)
        if progressDecimal != Decimal("0.00"):
            dictProgress[progressDate] = progressDecimal

    # for the rest of items build a timeline in descending order of date
    if not includeBackLinkInTimeline and not includeBodyInTimeline:
        timeLine += f"\n- {note.date[:10]} {note.type} {note.title}\n"
    else:
        timeLine += f"\n### {note.date[:10]} {note.type} {note.title}\n"
        
    if includeBodyInTimeline:
        timeLine += f"\n{myTools.remove_noteHeaders(note.noteBody)}\n"

    if includeBackLinkInTimeline:
        timeLine += f"\n[[{note.fileName}]]\n"
    
    if includeGannt: 
        gantt += f"{ myTools.letters_and_numbers_only(note.title)} : {note.date}, 1d\n"

    #debug
    #print(f"{myTerminal.INFORMATION}{note.date:<20} {note.project[:30]:<31} {note.title[:30]:<31}{myTerminal.RESET}")

if includeGannt:
    gantt = f"""
    

```mermaid

gantt
    title {selectedProject}
    dateFormat YYYY-MM-DD
    section Timeline

        {gantt}
    
```
"""


summary = f"""
# {selectedProject} Project Summary\n\n

prepared: {datetime.datetime.now().strftime(myPreferences.date_format())}

## Governance

**Budget Amount:** {budgetDecimal:.2f}
**Actuals:** {actualsDecimal:.2f}
"""

if len(dictActuals) > 0:
    actualsGraph = actuals_graph(dictActuals, budgetDecimal)
    summary += f"""
{actualsGraph}
"""
    
summary += f"""
{hubNote}

## Progress

"""

if len(dictProgress) > 5:
    #only show progress graph if there are more than 5 entries
    progressGraph = progress_graph(dictProgress)
    summary += f"""
{progressGraph}
"""

summary += f"""
{progressBody}

## Timeline
{timeLine}

{gantt}

"""

# use the dot prefix to hide the file in the project directory (at least in civilized file managers)
output_path = os.path.join(myPreferences.root_projects(), selectedProject, ".ProjectSummary.md")

if os.path.exists(output_path):
    print(f"{myTerminal.WARNING}Project summary already exists: {output_path}{myTerminal.RESET}")
    if not myInputs.ask_yes_no("Do you want to overwrite it?", default=True):
        print(f"{myTerminal.INFORMATION}Exiting without changes.{myTerminal.RESET}")
        exit(0)

with open(output_path, 'w', encoding='utf-8') as f:
    f.write(summary)
    
print("open project summary in default editor...")    
os.system(f'{myPreferences.default_editor()} "{output_path}"')    

print("open project summary as html in default browser...')")
myHTML.openMarkDownFileInBrowser(output_path)
