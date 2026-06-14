# Daily Journal

Each day starts with a new daily journal note.  The journal is meant to be a snapshot of the day and to capture content that does not gracefully fit into a project.

The command `open-journal.py` will either open the existing day's journal or start a new journal in the format 

```text
# Day: 2026-06-14

Start: 2026-06-14 07:23:03 

# Notes

```

Your journal is built either through in place notes where the time (HH:MM) and a descriptive title start a note or through atomic notes added to projects within the vault.  

The double hash (`##`) designates the beginning of a note block. 

## In place notes

Typically life moves faster than documentation.  For quick moving or inconsequential notes a new note can be created by simply typing `##` followed by the current date time and then proceeding with the note.

example

```
## 07:30 Review overnight traffic

Reviewed overnight usage logs, nothing unusual.

## 07:50 Escalated trouble ticket 

Received request from the service desk team - the accounting manager is is having trouble printing the quarterly report. They have attempted to print from their desktop computer, but the printer is not recognized and they are unable to complete the print job.

## 08:30 Team meeting
etc

```

![example](<./_ReadMeAttachments/example Daily Journal.png>)


## Atomic Project Notes

The `add-note.py` command will prompt `Do you want to add this meeting note to the YYYY-MM-DD journal? (Y/n enter for Y):` if the note you are adding occurs on a day, even a day in the past, where you had a journal note.

```text

Enter the date and time for the note (or leave blank for system default):10:20
enter note title: Weekly budget review
Enter value for [Attendees]: John, Fred, Sally 
Add attachment? (y/n): n

Do you want to add this meeting note to the 2026-06-14 journal? (Y/n enter for Y): 
```

Selecting `Y`es will result in a link added to the daily journal that joins to the atomic note.

example:
```text

## 10:20 meeting Weekly budget review

![[./_Projects/Project Two/260614102000_meeting_Weekly budget review.md]]

```

### Retroactive Project Notes

There are many cases where a short journal note evolves into something that should have been a full blown atomic project note.  Consider, a quick phone call transitions to become an in-depth project status discussion.  In this scenario the `make-AtomicNote.py` command can be used to lift a time block from the daily journal, create a new atomic project note, and insert a link from the daily journal to the project note.
