from . import Tools as myTools, Preferences as myPreferences, Inputs as myInputs, Terminal as myTerminal, Notes as myNotes
from .Templates import read_Template, merge_template_with_values

from dataclasses import dataclass
from typing import List
from decimal import Decimal
from dataclasses import field

import os
import json 
from datetime import datetime, timedelta


# KanBan board columns that we recognize
kanBanBoardColumns = {
    "To Do": "To Do",
    "In Progress": "In Progress",
    "Done": "Done",
    # "Backlog":"Backlog",
    # "Cancelled":"Cancelled"
}

#Assume task import from DevOps, Jira, Trello, etc
#use importTaskColumnTranslation to translate imported column names to desired column names
#desiredColumn:[list of possible synonyms in import file]
importTaskColumnTranslation = {"ID":["ID","Task Identifier","Task Identifier","Task ID","TaskID","Task Id","Task id","Task_Id","Ticket","Ticket Number"],
    "Title":["Title","Task Name","Task","Task Title","Task_Title","Task_Name","Ticket Title","Ticket_Title"],
    "Status":["State","Status","Task Status","Ticket Status","Ticket_Status"],
    "Start Date":["Start Date","Task Start Date","Start_Date","Task_Start_Date","Ticket Start Date","Ticket_Start_Date"],
    "Due Date":["Due Date","Task Due Date","Due_Date","Task_Due_Date","Ticket Due Date","Ticket_Due_Date"],
    "Assigned To":["Assigned To","Task Assigned To","Assigned_To","Task_Assigned_To","Ticket Assigned To","Ticket_Assigned_To"],
    "Closed Date":["Closed Date","Task Closed Date","Closed_Date","Task_Closed_Date","Ticket Closed Date","Ticket_Closed_Date"],
    "Task Detail":["Task Detail","Task Details","Task_Detail","Task_Details","Ticket Detail","Ticket_Detail","Acceptance Criteria"],
    }

@dataclass
class TaskData:
    id: str  # Unique identifier for the note, typically a timestamp or unique string
    fileName: str
    filePath: str = field(
        metadata={
            "description": "os.path.join(notePath, noteFileName) full file name and path"
        }
    )
    date: str
    osFileDateTime: str
    title: str
    project: str
    plannedStart: str
    actualStart: str
    plannedEnd: str
    endDate: str
    estimatedEffort: str
    percentComplete: Decimal
    assignedTo: str
    state: str
    ticket: str
    dependantOn: List[str]

    def to_dict(self):
        return {
            "id": self.id,
            "fileName": self.fileName,
            "filePath": self.filePath,
            "date": self.date,
            "osFileDateTime": self.osFileDateTime,
            "title": self.title,
            "project": self.project,
            "plannedStart": self.plannedStart,
            "actualStart": self.actualStart,
            "plannedEnd": self.plannedEnd,
            "endDate": self.endDate,
            "estimatedEffort": self.estimatedEffort,
            "percentComplete": self.percentComplete,
            "assignedTo": self.assignedTo,
            "state": self.state,
            "ticket": self.ticket,
            "dependantOn": self.dependantOn,
        }

    def __str__(self):
        if self.project != "":
            return f"{self.title} ({self.date[:10]}) from {self.project}.  Assigned to: {self.assignedTo}. State: {self.state}."
        else:
            return f"{self.title} ({self.date[:10]})"

    def KanBanColumn(self) -> str:
        """Returns the KanBan column based on the task state and percent complete."""
        state = self.state.lower()
        if state in ["not started", "pending", "to do"]:
            return kanBanBoardColumns.get("To Do", "To Do")
        elif state in ["in progress", "ongoing", "doing"]:
            return kanBanBoardColumns.get("In Progress", "In Progress")
        elif state in [
            "completed",
            "done",
            "finished",
        ] or self.percentComplete >= Decimal("100"):
            return kanBanBoardColumns.get("Done", "Done")
        elif state in ["cancelled", "canceled", "abandoned"]:
            return kanBanBoardColumns.get("Cancelled", "Cancelled")
        else:
            return kanBanBoardColumns.get("Backlog", "Backlog")


# --- end dataclass ---


def load_ProjectTasks(projectName: str) -> List[TaskData]:
    """Returns a list of TaskData objects for the specified project."""

    allTasks: List[TaskData] = []

    allNotes = myNotes.get_TaskNotes_from_Project(projectName)

    for note in allNotes:
        if note.project == projectName:
            task = loadTaskFromNote(note)
            allTasks.append(task)

    return allTasks

def loadTaskFromNote(note) -> TaskData:
    """Loads a TaskData object from a Note object."""

    percentComplete: Decimal
    try:
        percentComplete = Decimal(
            myTools.get_stringValue_from_noteBody("Percent Complete", note.noteBody)
        )
    except:
        percentComplete = Decimal("0")

    assignedToString = myTools.get_stringValue_from_noteBody(
        "Assigned To", note.noteBody
    )
    if assignedToString == "":
        assignedToString = "Unassigned"

    stateString = myTools.get_stringValue_from_noteBody("State", note.noteBody)
    if stateString == "":
        stateString = "Not Started"
    elif stateString.lower() in ["todo", "to do", "pending","new"]:
        stateString = "Not Started"
    elif stateString.lower() in ["doing", "in progress", "ongoing","active"]:
        stateString = "In Progress"
    elif stateString.lower() in ["done", "completed", "finished","closed", "ready for stakeholder review", "resolved"]:
        stateString = "Completed"
    elif stateString.lower() in ["cancelled", "canceled", "abandoned"]:
        stateString = "Cancelled"

    task = TaskData(
        id=note.id,
        fileName=note.fileName,
        filePath=note.filePath,
        date=note.date,
        osFileDateTime=note.osFileDateTime,
        title=note.title,
        project=note.project,
        plannedStart=myTools.get_stringValue_from_noteBody(
            "Planned Start", note.noteBody
        ),
        actualStart=myTools.get_stringValue_from_noteBody(
            "Actual Start", note.noteBody
        ),
        plannedEnd=myTools.get_stringValue_from_noteBody("Planned End", note.noteBody),
        endDate=myTools.get_stringValue_from_noteBody("Actual End", note.noteBody),
        estimatedEffort=myTools.get_stringValue_from_noteBody(
            "Estimated Effort", note.noteBody
        ),
        percentComplete=percentComplete,
        assignedTo=assignedToString,
        state=stateString,
        ticket=myTools.get_stringValue_from_frontMatter("Ticket", note.frontMatter),
        dependantOn=myTools.get_stringValue_from_noteBody(
            "Dependant On", note.noteBody
        ).split(","),
    )

    return task

def sort_Tasks_by_date(tasks: list[TaskData], descending: bool = True) -> list[TaskData]:
    """
    Sorts a list of TaskData objects by date.
    
    Args:
        tasks (list[TaskData]): The list of TaskData objects to sort.
        reverse (bool): If True, sorts in descending order; if False, sorts in ascending order. Default is True.
        
    Returns:
        list[TaskData]: The sorted list of TaskData objects.
    """
    
    return sorted(tasks, key=lambda task: task.date, reverse=descending)

def diagram_kanban_by_state(project_name: str, ticketBaseUrl:str = "") -> str:
    """Generates a KanBan diagram data structure for tasks in a project, grouped by state.
    if ticketBaseUrl is provided, it will be used to create links for tickets in the diagram.
    """

    tasks = load_ProjectTasks(project_name)

    projectBoardBuckets = {}
    cardStart = "@{"
    cardEnd = "}"
    
    #build buckets
    for bucket in kanBanBoardColumns.keys():
        projectBoardBuckets[bucket] = ""

    for task in tasks:
        ticketStatement = ""
        if task.ticket != "":
            ticketStatement = f" ticket: '{task.ticket}', " 
        projectBoardBuckets[task.KanBanColumn()] = projectBoardBuckets.get(task.KanBanColumn(), "") + f"\t{task.id}[{task.title}]{cardStart}{ticketStatement} assigned: '{task.assignedTo}'{cardEnd}\n"

    #start diagram
    if ticketBaseUrl == "":
        board = """
```mermaid
kanban
"""
    else:
        board = """
```mermaid
---
config:
kanban:
    ticketBaseUrl: 'https://github.com/mermaid-js/mermaid/issues/#TICKET#'
---
kanban
"""


    #add cards to board
    for bucket, cardString in projectBoardBuckets.items():
        board += f"{bucket}\n{cardString}\n"
        
    #end diagram
    board += """
```
"""

    return board

def diagram_kanban_by_assigned(project_name: str, ticketBaseUrl:str = "") -> str:
    """Generates a KanBan diagram data structure for tasks in a project, grouped by assigned to.
    if ticketBaseUrl is provided, it will be used to create links for tickets in the diagram.
    """

    tasks = load_ProjectTasks(project_name)

    projectBoardBuckets = {}
    cardStart = "@{"
    cardEnd = "}"
    
    #build buckets
    for task in tasks:
        assignedToList = task.assignedTo if task.assignedTo != "" else "Unassigned"
        for assignedTo in assignedToList.split(","):
            projectBoardBuckets[assignedTo.strip()] = ""

    for task in tasks:
        ticketStatement = ""
        if task.ticket != "":
            ticketStatement = f" ticket: '{task.ticket}', " 
        for assignedTo in projectBoardBuckets.keys():
            if assignedTo.strip() in task.assignedTo:
                projectBoardBuckets[assignedTo] = projectBoardBuckets.get(assignedTo, "") + f"\t{task.id}[{task.title}]{cardStart}{ticketStatement} assigned: '{task.state}'{cardEnd}\n"

    #start diagram
    if ticketBaseUrl == "":
        board = """
```mermaid
kanban
"""
    else:
        board = """
```mermaid
---
config:
kanban:
    ticketBaseUrl: 'https://github.com/mermaid-js/mermaid/issues/#TICKET#'
---
kanban
"""
    #add cards to board
    for bucket, cardString in projectBoardBuckets.items():
        board += f"{bucket}\n{cardString}\n"
        
    #end diagram
    board += """
```
"""

    return board

def diagram_Gantt_tasks(project_name: str) -> str:    
    """Generates a Gantt diagram data structure for tasks in a project.
    """

    tasks = load_ProjectTasks(project_name)
    tasks = sort_Tasks_by_date(tasks, descending=False)

    gantt = f""" 
```mermaid      
gantt
    dateFormat  YYYY-MM-DD
    title {project_name} - Project Tasks Gantt Chart
    excludes    weekends
"""
    for task in tasks:
        startDate = (task.plannedStart if task.plannedStart != "" else task.actualStart)[:10]
        endDate = (task.plannedEnd if task.plannedEnd != "" else task.endDate)[:10]
        if endDate == "" and startDate != "":
            #endDate = (datetime.strptime(startDate, "%Y-%m-%d") + timedelta(days=15)).strftime("%Y-%m-%d")
            endDate = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")

        if task.state.lower() in ["completed", "done", "finished"] :
            state = "done"
        elif task.state.lower() in ["in progress", "ongoing", "doing"]:
            state = "active"
        else:
            state = "planned"        

        if startDate != "" and endDate != "":
            gantt += f"    {myTools.letters_and_numbers_only(task.title)} :{state}, {task.id}, {startDate}, {endDate}\n"

    gantt += """
```
""" 
    return gantt    

def diagram_Gantt_notes(project_name: str, includePrivateNotes: bool) -> str:    
    """Generates a Gantt diagram data structure for notes in a project.
    """

    notes = myNotes.get_Notes_from_Project(project_name)
    notes = myNotes.sort_Notes_by_date(notes, descending=False)

    gantt = f""" 
```mermaid      
gantt
    dateFormat  YYYY-MM-DD
    title {project_name} - Project Tasks Gantt Chart
    excludes    weekends
"""
    for note in notes:
        if includePrivateNotes or not note.private :
            startDate = note.date[:10]
            endDate = (note.endDate if (note.endDate != "" and note.endDate != note.date) else "1d")[:10]
            
            state = "done"
            
            if startDate != "" and endDate != "":
                gantt += f"    {myTools.letters_and_numbers_only(note.title)} :{state}, {note.id}, {startDate}, {endDate}\n"

    gantt += """
```
""" 
    return gantt   

def _translate_TaskImport_Columns(FullPath) -> list:
    """
    Translates imported column names to desired column names based on synonyms.
    Assumes, hopes that dates are provided in yyyy-mm-dd format.
    """
    importTasks = myTools.read_csv_to_dict_list(FullPath)

    translatedTasks = []
    for importTask in importTasks:
        translatedTask = {}
        for importedColumnName, value in importTask.items():
            for desiredColumn, synonyms in importTaskColumnTranslation.items():
                translatedTask[desiredColumn] = ""
                for synonym in synonyms:
                    if synonym.lower() in [key.lower() for key in importTask.keys()]:
                        if desiredColumn == "Assigned To":
                            # Special handling for "Assigned To" to extract name from email format 'David Gordon <dgordon@ispname.com>'
                            translatedTask[desiredColumn] = importTask[synonym].split('<')[0].strip()
                        else:
                            translatedTask[desiredColumn] = importTask[synonym]
                        break
        translatedTasks.append(translatedTask)
    

    return translatedTasks

def _make_task_note_content_from_imported_task(selectedProjectName: str, importedTask: dict) -> bool:
    """
    Creates the content for a task note from an imported task dictionary.
    """
    if selectedProjectName == "":
        projects, selectedProjectName, selectedProjectIndex = myInputs.select_project_name_withDict(showNewProjectOption=False)
    
    if selectedProjectName is None or selectedProjectName == "":
        print(f"{myTerminal.ERROR}No project selected. Please select a project first.{myTerminal.RESET}")
        return False

    selectedTemplateName = "project_task_template.markdown"
    
    #based on the selected template, figure out which output folder to use
    selectedTemplatePath = os.path.join(myPreferences.root_templates(), selectedTemplateName)
    
    #get rid of unnecessary parts of the template name
    #templates should have a prefix that tells what group of template they belong to
    # and a suffix that shows they are a template
    noteType = selectedTemplateName 
    templateNamePartsToReplace = ["PKV_","project_", "_template.markdown", "_template.md"]
    for part in templateNamePartsToReplace:
        noteType = noteType.replace(part, "")

    #make sure we the default project progress template exist
    if not os.path.exists(selectedTemplatePath):
        print(f"{myTerminal.ERROR}Template '{selectedTemplateName}' not found in {myPreferences.root_templates()}{myTerminal.RESET}")
        return False

    newNote_directory = os.path.join(myPreferences.root_projects(), selectedProjectName)    
    os.makedirs(newNote_directory, exist_ok=True)

    #collect information that should be seeded into the note fields
    selectedDateTime = datetime.now()
    timestamp_id = selectedDateTime.strftime(myPreferences.timestamp_id_format())
    timestamp_full = selectedDateTime.strftime(myPreferences.datetime_format())

    # Read the template content
    templateBody = read_Template(selectedTemplatePath)
    
    noteDict = {"Title": importedTask.get("Title","Untitled Task"),
                "tags": "",
                "Project Name": selectedProjectName,
                "State - Not Started, In-progress, Testing, Complete, Cancelled": importedTask.get("Status","Not Started"),
                "ticket number": importedTask.get("ID",""),
                "plannedStart": importedTask.get("Start Date","").replace("a.m.","").replace("p.m.",""),
                "actualStart": importedTask.get("Start Date","").replace("a.m.","").replace("p.m.",""),
                "plannedEnd": importedTask.get("Due Date","").replace("a.m.","").replace("p.m.",""),
                "actualEnd": importedTask.get("Closed Date","").replace("a.m.","").replace("p.m.",""),
                "Assigned To": importedTask.get("Assigned To","Unassigned"),
                "Task detail": importedTask.get("Task Detail",""),
                }

    uniqueIdentifier, note_Content = merge_template_with_values(timestamp_id, timestamp_full, selectedProjectName, 
                               template = templateBody, 
                               mergeData = noteDict,
                               runSilent = True)
    
    # Construct the output filename and path
    output_filename = f"{uniqueIdentifier}.md"
    output_path = os.path.join(newNote_directory, output_filename)

    # Save the new note
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(note_Content)

    print(f"\t{myTerminal.SUCCESS}Note created:{myTerminal.RESET}")
    return True

def _update_existing_task_from_csv_import(projectName:str,csvTaskDict: dict, pkvTask: TaskData) -> bool:
    """
    Updates an existing project task from an imported task dictionary.
    """
    containsChange = False
    print (f"Task: {csvTaskDict['Title']} ({csvTaskDict['ID']}) already exists.")
    if pkvTask.assignedTo.strip() != csvTaskDict['Assigned To'].strip():
        containsChange = True
        print("\tAssigned To changed:")
        print (f"\t\t{pkvTask.assignedTo} -> \n\t\t{csvTaskDict['Assigned To']}")
    
    if pkvTask.state.strip() != csvTaskDict['Status'].strip():
        containsChange = True
        print("\tStatus changed:")
        print (f"\t\t{pkvTask.state} -> \n\t\t{csvTaskDict['Status']}")
    
    if pkvTask.actualStart.strip() != csvTaskDict['Start Date'].replace('a.m.','').replace('p.m.','').strip():
        containsChange = True
        print("\tActual Start changed:")
        print (f"\t\t{pkvTask.actualStart} -> \n\t\t{csvTaskDict['Start Date'].replace('a.m.','').replace('p.m.','')}")
    
    if pkvTask.plannedEnd.strip() != csvTaskDict['Due Date'].replace('a.m.','').replace('p.m.','').strip():
        containsChange = True
        print("\tPlanned End changed:")
        print (f"\t\t{pkvTask.plannedEnd} -> \n\t\t{csvTaskDict['Due Date'].replace('a.m.','').replace('p.m.','')}")
    
    if pkvTask.endDate.strip() != csvTaskDict['Closed Date'].replace('a.m.','').replace('p.m.','').strip():
        containsChange = True
        print ("\tActual End changed:")
        print (f"\t\t{pkvTask.endDate} -> \n\t\t{csvTaskDict['Closed Date'].replace('a.m.','').replace('p.m.','')}")
    
    if not containsChange:
        print ("\tNo changes detected.")
        return True        
    proceed = myInputs.ask_yes_no_from_user("Update this task?", default=True)
    
    if proceed:
        noteBody = myNotes.read_Note_from_path(pkvTask.filePath)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("**Assigned To**:", csvTaskDict['Assigned To'], noteBody)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("**State**:", csvTaskDict['Status'], noteBody)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("**Planned Start**:", csvTaskDict['Start Date'].replace("a.m.","").replace("p.m.",""), noteBody)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("**Actual Start**:", csvTaskDict['Start Date'].replace("a.m.","").replace("p.m.",""), noteBody)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("**Planned End**:", csvTaskDict['Due Date'].replace("a.m.","").replace("p.m.",""), noteBody)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("**End Date**:", csvTaskDict['Closed Date'].replace("a.m.","").replace("p.m.",""), noteBody)
        noteBody = myNotes.replace_lineLabelValue_in_noteBody("modified:", myTools.now_YYYY_MM_DD_HH_MM_SS() , noteBody)

        if myNotes.write_Note_to_path(pkvTask.filePath, noteBody):
            print (f"Task '{csvTaskDict['Title']}' updated successfully.\n")
    return True

def import_or_update_tasks_from_CSV(FullPath, projectName: str) -> None:
    """
    Imports or updates tasks from a CSV file into the specified project.
    """
    #tasks from DevOps, Jira, Trello, etc
    csvTasks = _translate_TaskImport_Columns(FullPath)
    
    print (f"Importing or updating {len(csvTasks)} tasks into project: {projectName}")
    if len(csvTasks) == 0:
        print (f"{myTerminal.ERROR}No tasks found to import from {FullPath}{myTerminal.RESET}")
        return

    #existing PKV project tasks
    pkvTasks = load_ProjectTasks(projectName)

    for csvTask in csvTasks:
        taskExists = False
        for pkvTask in pkvTasks:
            if pkvTask.ticket.strip() == csvTask["ID"]:
              taskExists = True
              _update_existing_task_from_csv_import(projectName, csvTask, pkvTask)
        
        if not taskExists:
            print (f"New task found: {csvTask['Title']} ({csvTask['ID']}) assigned to '{csvTask['Assigned To']}'")
            proceed = myInputs.ask_yes_no_from_user("Import this task?", default=True)
            if proceed:
                if _make_task_note_content_from_imported_task(projectName, csvTask):
                    print (f"\tTask '{csvTask['Title']}' imported successfully\n")

#=== Project Methods From Tools

def get_pkv_projects() -> dict:
    """
    Returns a dictionary of projects with their names as keys and their paths as values.
    
    Returns:
        dict: A dictionary containing project names and their corresponding paths.
    """
    projects = {}
    for filename in sorted(os.listdir(myPreferences.root_projects())):
        projectPath = os.path.join(myPreferences.root_projects(), filename)
        if os.path.isdir(projectPath):
            projects[filename] = projectPath
    
    return projects

#global declaration for caching project configs
dictProjectConfigs = {}
def get_ProjectConfig_as_dict(projectName: str) -> dict:
    """
    Returns the project configuration for a given project name.
    
    Args:
        projectName (str): The name of the project.
    """
    global dictProjectConfigs
    if projectName in dictProjectConfigs:
        return dictProjectConfigs[projectName]
    
    projectPath = os.path.join(myPreferences.root_projects(), projectName)
    
    if not os.path.isdir(projectPath):
        print(f"{myTerminal.ERROR}Project '{projectName}' path does not exist.{myTerminal.RESET}")
        return {}

    if not os.path.exists(os.path.join(projectPath, ".ProjectConfig.json")):
        configBody = {
                    "ProjectFolderName": f"{projectName}",
                    "ProjectName": f"{projectName}",
                    "Programs": [],
                    "Archived": False,
                    "Sync": False,
                    "PublicShareFolder": "",
                    "Needs Weekly Progress Update": False,
                    "Needs Monthly Progress Update": False
                    }
        with open(os.path.join(projectPath, ".ProjectConfig.json"), 'w', encoding='utf-8') as f:
            json.dump(configBody, f, indent=4)
        
    configPath = os.path.join(projectPath, ".ProjectConfig.json")
    if not os.path.isfile(configPath):
        return {}
    
    with open(configPath, 'r', encoding='utf-8') as f:
        try:
            config = json.load(f)
            dictProjectConfigs[projectName] = config    
            return config
        except json.JSONDecodeError:
            print(f"{myTerminal.ERROR}Error decoding JSON from {configPath}{myTerminal.RESET}")
            return {}
