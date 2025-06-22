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

## Commands

Use `chmod +x *.py` to make the Python scripts in the root folder executable if using Linux or mac OS.

| Command | Description |
| --- | --- |
| Open-PKV | Opens the personal knowledge vault in the default editor|
| Get-VaultDetails | Displays a summary of the vault preferences and vault details.|
| Edit-Preferences | Opens the personal knowledge vault preferences in the default editor|
| Add-ScreenCapture  | Selects a recent screen capture to be moved to the PKV or Project attachment.  |
| Add-Attachment  | Selects a recent attachment to be moved to the PKV or Project attachment.  |
| Add-Project_Note  | Asks for a project and template before preparing a blank project note based on the selected template.  |
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


## Attachments and Screen Captures

Attachments and screen captures can be added to the PKV root or to the root of a specific project using the `Add-Attachment` and `Add-ScreenCapture` commands.

These commands will brows the default attachment and screen capture pick up locations and then move the selected file to the appropriate attachment folder.  You can then use the double square bracket `[[filename.txt]]` syntax in your note to include a link or web standard links `[display value](url)`

