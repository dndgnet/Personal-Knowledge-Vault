# Personal-Knowledge-Vault

Tools to help manage a Personal Knowledge Vault

## Directory Structure
```zsh
root/
├── Attachments/
├── Projects/
    ├── Project One
    |   └── Attachments/
    │       └── image1.svg
    │   └── file2.txt
    │   └── file3.txt     
    ├── Project Two
    |   └── attachments/
    │   └── file4.txt
    │   └── file5.txt       
├── file1.txt
├── file7.txt
├── file8.txt
└── file9.txt       
```

## Preferences
PVK preferences can be found in a file called `Personal-Knowledge-Vault.json`.

On macOS and Linux machines this file should be found in `~/Library/Preferences/` but on Windows this might be `\APPDATA\Preferences`.

Use the `Edit-Preferences` command to open the preferences command in a text editor.

An default preferences file should look like this
```python
#empty preferences file
_exampleEmptyPreferences = {
    "pkv_root":"PKV", #root folder name of the personal knowledge vault
    "attachments_root":"_Attachments", #name of the folder in the PKV where attachments are stored
    "projects_root":"_Projects", #name of the folder in the PKV where projects are stored
    "archive_root":".Archive", #name of where soft deleted projects will be sent
    "timestamp_id_format":"%Y%m%d%H%M%S", #format for note unique identifiers
    "date_format":"%Y-%m-%d", #format for displaying dates in notes
    "datetime_format":"%Y-%m-%d %H:%M:%S", #format for displaying date and time in notes
    "documents_path": "os default", #where documents are stored, use 'os default' to let the OS decide
    "attachmentPickUp_path": "os default", #where we can look for new attachment, use 'os default' to let the OS return the downloads folder
    "screenCapture_path": "os default", #where we can look for new screen captures, use 'os default' to let the OS return the screenshots folder
    "default_editor": "code", #default editor to use for opening files, can be 'code' for VS Code, 'zed' for Zed, or any other editor command
    "show_tag_prompt": false, #set to true if the add new note commands should prompt for front matter tags when creating a new note, set to false if the author will provide front matter tags manually
    }
```

>**WARNING**: consider backing up your preferences file before you make changes and make sure you understand your changes.  For example, if you provide a new `pkv_root` value you will essentially be creating a new vault and if you change the `timestamp_id_format` you will fundamentally alter how new unique ids are generated.



## Projects

TODO: explain why projects get their own folders
- expect that a project might have to be exported or share with other users

## Commands

Use `chmod +x *.py` to make the Python scripts in the root folder executable if using Linux or mac OS.

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
| Add-Project_Note  | Asks for a project and template before preparing a blank project note based on the selected template.  |
| Add-PKV_Note  | Asks for a project and template before preparing a blank note based on the selected template. If a project name is provided the name is saved in the note front matter, project name doe <b>not</b> change note location  |
| |<i><b>Helpers</b></i> |
| Make-Table  | Asks for the column headings and then produces a blank markdown table that can be copied and used in a note.  |
|   |   |

## Templates

### Template Naming
Template files carry a *type_* prefix and a *template.markdown* suffix.

Example

```zsh
project_email_template.markdown
project_meeting_template.markdown
wiki_comment_template.markdown
```
The first two templates are used for project email and meetings.
The third template is used to record a wiki comment.

### Template Merge Tags

When creating a new note from a template, a prompt will be given to provide values for each merge tag in a template.

Merge tags are denoted as text surrounded by a square brackets in a template file fore matter or body.

Example

```markdown
Project Name: [Project Name]
Note Subject: [Subject]
```
When adding a new note the user will automatically be prompted for *Project Name* and *Subject*.

Square brackets containing other square brackets or no text will be ignored.

### Event Templates

Event templates are **super** short and designed to be used from the terminal without additional time spent in the text editor.

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


## Attachments and Screen Captures

Attachments and screen captures can be added to the PKV root or to the root of a specific project using the `Add-Attachment` and `Add-ScreenCapture` commands.

These commands will brows the default attachment and screen capture pick up locations and then move the selected file to the appropriate attachment folder.  You can then use the double square bracket `[[filename.txt]]` syntax in your note to include a link or web standard links `[display value](url)`

