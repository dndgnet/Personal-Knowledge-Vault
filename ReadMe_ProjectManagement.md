# Workflow, Project and Task Management

## Action items 

Incomplete **action items**, any action that must be completed, are reflected in the note body as `- [ ] action item description`.  Complete action items are reflected in the note body as `- [x] action item description`.

Comments, modifiers and results can be associated with an action item using the `<comments>` tag.  For example - 

```markdown
Things to do 
- [ ] update the readme file
<comments>
    Remember first draft needed more detail about how to find action items.
</comments>
- [ ] 2026-02-03 approve time sheets before cut off
- [x] 2026-02-03 start release preparation
<comments>
Done, dev manager reports that the release manager is prepared and ready for Thursday's release
</comments>
```
In the above example, the feedback about the release manager will be associated with the "start release preparation" action item.


## Finding Incomplete action items 

Use the `get-actionItems` command to return incomplete action items.

## Tasks

Tasks can be imported and updated from remote sources such as DevOps, Jira, Trello, etc using the `project_tasks_from_CSV.py` command.

Our project tasks expects a CSV file containing 
- ID: task unique identifier
- Title: human readable task name
- Status: 
- Start Date: 
- Due Date: date that the work item is expected to be completed
- Closed Date: date that the work item was completed
- Assigned To:
- Task Detail: human readable description of the task.


The following synonyms will be accepted for column names.

``` 
"""Projects.py line 26, importTaskColumnTranslation

{"ID":["ID","Task Identifier","Task Identifier","Task ID","TaskID","Task Id","Task id","Task_Id","Ticket","Ticket Number"],
"Title":["Title","Task Name","Task","Task Title","Task_Title","Task_Name","Ticket Title","Ticket_Title"],
"Status":["State","Status","Task Status","Ticket Status","Ticket_Status"],
"Start Date":["Start Date","Task Start Date","Start_Date","Task_Start_Date","Ticket Start Date","Ticket_Start_Date"],
"Due Date":["Due Date","Task Due Date","Due_Date","Task_Due_Date","Ticket Due Date","Ticket_Due_Date"],
"Assigned To":["Assigned To","Task Assigned To","Assigned_To","Task_Assigned_To","Ticket Assigned To","Ticket_Assigned_To"],
"Closed Date":["Closed Date","Task Closed Date","Closed_Date","Task_Closed_Date","Ticket Closed Date","Ticket_Closed_Date"],
"Task Detail":["Task Detail","Task Details","Task_Detail","Task_Details","Ticket Detail","Ticket_Detail","Acceptance Criteria"],
}
```

On first import all of the columns are used to create a new task but on subsequent *update* events ID, Title and Task Detail will not be changed.


### Status and State

Status and state are highly dependant on the source system.  The following shows how states are translated to KanBan board columns.

```
"""Projects.py line 87, def KanBanColumn(self)

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