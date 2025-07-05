# Personal-Knowledge-Vault

## What and Why

todo: explain that this repository is a productivity hack for places where users are not allowed to buy and install software.  Somehow explain that the MS OneNote is not productive and just encourages vendor lock in 


In real life, tools like Obsidian, Roam Research, Notion, Zettlr, and many others either support or are designed specifically for Zettelkasten style note-taking. However, in many corporate environments, these tools are often unsupported or outright prohibited.

see [Zettelkasten choosing software](https://zettelkasten.de/introduction/#choosing-software)

While there are ways to bypass corporate IT restrictions to stay productive, one of the simplest approaches is to technically comply with the rules by using native text editors like Notepad, Notepad++, or VS Code. Most organizations are unlikely to restrict these widely accepted tools.  

This repository includes simply Python scripts that extend functionality of any common text editor and make note taking in a corporate environment less onerous.

Scripts in this repository rely on standard Python libraries available in Python 3.0 and later (though only tested with Python 3.9 and above).

Cloud storage and backup are achieved by leveraging existing corporate infrastructure. For example, by placing your vault in the Windows Documents folder, you can utilize corporate OneDrive for seamless integration.

>*Hint* Consider calling `git init` in your value to give yourself local backups and roll back points.



## Vault Structure
```zsh
root/
├── _Attachments/
├── _Projects/
    ├── Project One
    |   └── _Attachments/
    │       └── 20250601070742_screen capture image.svg
    │       └── 20250401030202_requirements.doc
    │   └── 20250601070742_meeting kickoff.md
    │   └── 20250401030202_meeting_review_draft_requirements.md     
    ├── Project Two
    |   └── attachments/
    │   └── 20250201020200_email_stakeholder_introduction.md
    │   └── 20250201030200_chat_budget_discussion.md 
├── 20250601070742_event_server_room_temperature_alarm.md
├── 20250601071003_email_feedback_from_accounting.md
├── 20250601141022_email_staff_vacation_request.md
└── 20250601141022_meeting_weekly_stakeholder_meeting.md
```

## Preferences
PVK preferences can be found in a file called `Personal-Knowledge-Vault.json`.

On macOS and Linux machines this file should be found in `~/Library/Preferences/` but on Windows this might be `\APPDATA\Preferences`.

Use the `Edit-Preferences` command to open the preferences command in a text editor.

An default preferences file should look like this
```python

#empty preferences file
_exampleEmptyPreferences = {

    "timestamp_id_format":"%Y%m%d%H%M%S", #format for note unique identifiers
    "date_format":"%Y-%m-%d", #format for displaying dates in notes
    "datetime_format":"%Y-%m-%d %H:%M:%S", #format for displaying date and time in notes
    
    "pkv_root":"PKV", #root folder name of the personal knowledge vault
    "attachments_root":"_Attachments", #name of the folder in the PKV where attachments are stored
    "projects_root":"_Projects", #name of the folder in the PKV where projects are stored
    "archive_root":".Archive", #name of where soft deleted projects will be sent
    
    "documents_path": "default", #where documents are stored, use 'default' to let the OS decide
    "attachmentPickUp_path": "default", #where we can look for new attachment, use 'default' to let the OS return the downloads folder
    "screenCapture_path": "default", #where we can look for new screen captures, use 'default' to let the OS return the screenshots folder
    "template_path": "default", #path to the templates, use 'default' to use the system templates, provide a different path if you have your own templates
    
    "default_editor": "code", #default editor to use for opening files, can be 'code' for VS Code, 'zed' for Zed, nano for Nano, or any other editor command
    "show_tag_prompt": "False", #set to true if the add new note commands should prompt for front matter tags when creating a new note, set to false if the author will provide front matter tags manually
    "automatically_open_event_notes": "False", #set to true if the add new note commands should automatically open the created note in the default editor, set to false if the author will open it manually
    
    "author_name": "default", #use default to use the system username, or provide a custom name to be used in notes

    }
```

>**WARNING**: consider backing up your preferences file before you make changes and make sure you understand your changes.  For example, if you provide a new `pkv_root` value you will essentially be creating a new vault and if you change the `timestamp_id_format` you will fundamentally alter how new unique ids are generated.


## Front Matter

TODO: talk about Zettelkasten basics
- emphasize the importance of a YYYYMMDD date format 
- explain tags vs. keywords
  - tags are bigger, keywords are just sensible things to help as future search criteria when you don't necessarily have the right words
- explain retention
  - Short, Medium, and Long: at some point we will need a command to delete notes based on the retention.  The logic is tbd so for now just record the author's intent.

## Projects

TODO: explain why projects get their own folders
- expect that a project might have to be exported or share with other users

TODO: explain the project summary


## Commands

Consider `chmod +x *.py` to make the Python scripts in the root folder executable if using Linux or mac OS.

| Command | Description |
| --- | --- |
| |<i><b>Vault Commands</b></i> |
| Open-PKV | Opens the personal knowledge vault in the default editor|
| Get-VaultDetails | Displays a summary of the vault preferences and vault details.|
| Edit-Preferences | Opens the personal knowledge vault preferences in the default editor|
| |<i><b>Follow-up Commands</b></i> |
|Get-INCOMPLETE| Returns a list of notes that contain an #INCOMPLETE tag|
|Get-TODO| Returns a list of notes that contain an #TODO tag|
|Get-ActionItems| Returns a list of notes that contain one or more action [ ] items|
| |<i><b>Add Content Commands</b></i> |
| Add-ScreenCapture  | Selects a recent screen capture to be moved to the PKV or Project attachment.  |
| Add-Attachment  | Selects a recent attachment to be moved to the PKV or Project attachment.  |
| Add-Note  | Asks for a project and attachments before preparing note based on the selected template. <br/> Note: if a project name is provided the note is saved in the note front matter and the note is created in the project sub directory.  |
| |<i><b>Helpers</b></i> |
| Make-Table  | Asks for the column headings and then produces a blank markdown table that can be copied and used in a note.  |
| Search-Notes  | Performs an iterative search by asking for search parameters such as project, tag, date and note body content.  |
| Build-ProjectSummary  | Selects a project and then prepares a summary putting the latest <i>progress</i> note at the top followed by a timeline of other notes.  |
| Convert-MeetingNotesToAtomic | Splits a meeting note into atomic notes based on level three summary headings.|

## Templates

### Template Naming
Template files carry a *type_* prefix and a *template.markdown* suffix.

Example

```zsh
project_email_template.markdown
project_meeting_template.markdown
pkv_event_template.markdown
```
The first two templates are used for project email and meetings.
The third template is used to record a event comment.

The `Add-Note` command will prompt for the project.  If you select a project, you will be presented with templates specifically intended for projects.  if you select 'no project', you will be presented with the generic PKV templates.

### Template Merge Values

When creating a new note from a template, a prompt will be given to provide values for each merge tag in a template.

Merge values are denoted as text surrounded by a square brackets in a template file front matter or body.

Example

```markdown
Project Name: [Project Name]
Note Subject: [Subject]
```
When adding a new note the user will automatically be prompted for *Project Name* and *Subject*.

Square brackets containing other square brackets or no text will be ignored.

#### Special Merge Values

`["YYYYMMDDHHMMSS]` and `[timestamp_id]` will be populated with the timestamp_id which is prepared using the note date time.

`["YYYY-MM-DD HH:MM:SS"]` and `[DateTime]` will be populated as the full date and time as provided when starting a note.

`[YYYY-MM-DD`] and `[DATE]` will be populated with the date collected when starting a note.

`[Project Name]`, `[ProjectName]` and `[Project]` will be populated with the project name collected when starting a note.

`[Current User]`,`[User`], `[Username`], and `[Author]` will be populated with user identity returned by the OS.

`[tags]`,`[Tags]` and `[TAGS]`: will be populated with the values collecting when starting a note **if** the preferences `show_tag_prompt` value is `True`.  If *show_tag_prompt* is False the tag value will be left for the user to manually provide when they edit the note.


#### Event Templates

Event templates are **super** short and designed to be used from the terminal without additional time spent in the text editor.  Event templates are intended to be a replacement for the things that you would scribble in the margins of your day book.


Consider 
```zsh
Available templates:
	1. email
	2. chat
	3. meeting
	4. event
Select a template (1-4): 4
Enter the date and time for the note (or leave blank for system default):
	Using default: 2025-06-23 19:24:09
Enter value for [Title]: alarm
Enter value for [Event Description]: Rec. alarm about server overheating
Enter tags (comma-separated) or leave blank for none:   
Note created: /Users/david/Documents/PKV/_Projects/250623192409_event.md
Done!
```

### Your own Templates

If you want to use your own templates, use the `Edit-Preferences` command to open your preferences and provide the location of your templates in the `template_path` property.


## Attachments and Screen Captures

Attachments and screen captures can be added to the PKV root or to the root of a specific project using the `Add-Attachment` and `Add-ScreenCapture` commands.

These commands will brows the default attachment and screen capture pick up locations and then move the selected file to the appropriate attachment folder.  You can then use the double square bracket `[[filename.txt]]` syntax in your note to include a link or web standard links `[display value](url)`



# Finding stuff

## Search-Notes
todo: 

```zsh
david@Davids-Laptop Personal-Knowledge-Vault % ./Search-Notes.py

40 notes found.

----------------------------------------
Search options:
	p) project - Search by project
	t) tags - Search by tags
	d) date range - Search by note date
	i) title - Search by title
	b) body - Search by body text
	 --------------------
Commands:
	u) undo - undo the last search
	l) list - list current search results
	x) export - export results to editor note
	q) quit - Quit the search
	 --------------------
Enter your choice: 

```



## OS native searches

### Simple Search

Find all files in the PKV that contain the word "banana"

Example mac OS or Linux
```zsh
grep -r "banana"
```

Example Windows
```powershell
Get-ChildItem -Recurse | Select-String "banana"
```

### Compound Search

Windows
```powershell
Get-ChildItem -Recurse -File |Where-Object { ($_ | Select-String "project: TMS") -and ($_ | Select-String "banana")} 
```
