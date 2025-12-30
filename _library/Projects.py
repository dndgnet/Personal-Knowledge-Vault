from . import Tools as myTools

from dataclasses import dataclass
from typing import List
from decimal import Decimal
from dataclasses import field

kanBanBoardColumns = {
    "To Do": "To Do",
    "In Progress": "In Progress",
    "Done": "Done",
    # "Backlog":"Backlog",
    # "Cancelled":"Cancelled"
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


def get_ProjectTasks(projectName: str) -> List[TaskData]:
    """Returns a list of TaskData objects for the specified project."""

    allTasks: List[TaskData] = []

    allNotes = myTools.get_TaskNotes_from_Project(projectName)

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
    elif stateString.lower() in ["todo", "to do", "pending"]:
        stateString = "Not Started"
    elif stateString.lower() in ["doing", "in progress", "ongoing"]:
        stateString = "In Progress"
    elif stateString.lower() in ["done", "completed", "finished"]:
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
        endDate=myTools.get_stringValue_from_noteBody("End Date", note.noteBody),
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

def kanban_diagram_by_state(project_name: str, ticketBaseUrl:str = "") -> str:
    """Generates a KanBan diagram data structure for tasks in a project, grouped by state.
    if ticketBaseUrl is provided, it will be used to create links for tickets in the diagram.
    """

    tasks = get_ProjectTasks(project_name)

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


def kanban_diagram_by_assigned(project_name: str, ticketBaseUrl:str = "") -> str:
    """Generates a KanBan diagram data structure for tasks in a project, grouped by assigned to.
    if ticketBaseUrl is provided, it will be used to create links for tickets in the diagram.
    """

    tasks = get_ProjectTasks(project_name)

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