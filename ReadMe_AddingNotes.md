# Adding Notes to Personal Knowledge Vault

## Overview

The Personal Knowledge Vault (PKV) provides multiple scripts and workflows for creating and managing different types of notes. This document explains how to add notes, work with templates, attach files, and leverage the atomic note-taking methodology.

## Table of Contents

- [Quick Start](#quick-start)
- [Core Note-Adding Scripts](#core-note-adding-scripts)
- [Note Types and Templates](#note-types-and-templates)
- [Front Matter Structure](#front-matter-structure)
- [Working with Attachments](#working-with-attachments)
- [Atomic Notes Workflow](#atomic-notes-workflow)
- [Daily Journal](#daily-journal)
- [Project Notes](#project-notes)
- [Best Practices](#best-practices)

---

## Quick Start

The primary script for adding notes is `add-note.py`:

```bash
./add-note.py
```

This script will:
1. Prompt you to select a project (or create a general note)
2. Show available templates based on your selection
3. Collect metadata (title, date, tags, etc.)
4. Create the note with a unique identifier
5. Optionally open the note in your default editor

---

## Core Note-Adding Scripts

### `add-note.py` - Universal Note Creator

The main script for creating any type of note in your vault.

**Features:**
- Template selection for different note types
- Automatic unique identifier generation using timestamp format
- Project association (optional)
- Front matter population
- Attachment linking during creation
- Version control integration
- Duplicate detection for single-instance note types
- Journal integration option

**Usage Flow:**
1. Select a project (optional)
2. Choose a template (PKV templates for general notes, project templates for project notes)
3. Enter date/time (or press Enter for current date/time)
4. Provide a title
5. Fill in template merge tags as prompted
6. Optionally add attachments
7. Note is created and optionally opened in your editor

**Single-Instance Note Types:**
Some note types should only exist once per project (e.g., "hub", budget, schedule). If you try to create a duplicate, the existing note will be opened instead.

### `add-projectProgressNote.py` - Project Progress Notes

Creates structured progress notes for project management.

**Features:**
- Template-based creation with progress note structure
- Clone mode: Copy and update the most recent progress note
- Automatic inclusion of previous progress data:
  - Last summary
  - Last issues/impediments
  - Last next steps
- Timestamp management
- Automatic version control commits

**Usage:**
```bash
./add-projectProgressNote.py
```

Or with a project name:
```bash
./add-projectProgressNote.py "ProjectName"
```

### `pm-add_weekly_progress_notes.py` - Bulk Progress Notes

Iterates through all active projects and creates weekly progress notes for those configured to need them.

**Features:**
- Reads `.ProjectConfig.json` files in each project
- Filters projects marked as needing weekly updates
- Interactive prompt for each qualifying project
- Calls `add-projectProgressNote.py` for each selected project

**Usage:**
```bash
./pm-add_weekly_progress_notes.py
```

### `open-journal.py` - Daily Journal

Opens today's journal entry or creates one if it doesn't exist.

**Features:**
- Automatic journal creation for current date
- Uses `pkv_journal_template.markdown` template
- Opens existing journal if one exists for today
- Integrated with note-adding workflow (can link new notes to journal)

**Usage:**
```bash
./open-journal.py
```

---

## Note Types and Templates

Templates are stored in the `_templates/` folder and follow naming conventions:

### PKV Templates (General Notes)
- `pkv_chat_template.markdown` - Chat conversations
- `pkv_email_template.markdown` - Email correspondences
- `pkv_event_template.markdown` - Events and occurrences
- `pkv_hub_template.markdown` - Hub notes for organizing topics
- `pkv_idea_template.markdown` - Ideas and inspirations
- `pkv_journal_template.markdown` - Daily journal entries
- `pkv_meeting_template.markdown` - Meeting notes

### Project Templates
- `project_assumption_template.markdown` - Project assumptions
- `project_budget_template.markdown` - Budget tracking
- `project_changerequest_template.markdown` - Change requests
- `project_chat_template.markdown` - Project-related chats
- `project_decision_template.markdown` - Decision records
- `project_decision_lite_template.markdown` - Lightweight decisions
- `project_dependency_template.markdown` - Dependencies
- `project_documentation_template.markdown` - Documentation
- `project_email_template.markdown` - Project emails
- `project_event_template.markdown` - Project events
- `project_executive_summary_template.markdown` - Executive summaries
- `project_hub_template.markdown` - Project hub/brief
- `project_idea_template.markdown` - Project ideas
- `project_introduction_template.markdown` - Project introductions
- `project_issue_template.markdown` - Issues and problems
- `project_meeting_template.markdown` - Project meetings
- `project_milestones_template.markdown` - Milestone tracking
- `project_progress_template.markdown` - Progress reports
- `project_report_template.markdown` - General reports
- `project_risk_template.markdown` - Risk register entries
- `project_roi_template.markdown` - ROI calculations
- `project_schedule_template.markdown` - Schedule management
- `project_scope_template.markdown` - Scope definition
- `project_task_template.markdown` - Tasks and action items
- `project_transition_plan_template.markdown` - Transition plans

### Atomic Template
- `atomic_template.markdown` - Atomic thought notes (single-concept notes)

### Template Merge Tags

Templates use merge tags that are replaced with actual values during note creation:

**Standard Tags:**
- `[YYYYMMDDHHMMSS]` or `[TIMESTAMP_ID]` - Unique timestamp ID
- `[YYYY-MM-DD HH:MM:SS]` or `[DATETIME]` - Full datetime
- `[YYYY-MM-DD]` or `[DATE]` - Date only
- `[Title]` - Note title
- `[Project Name]` or `[Project]` or `[ProjectName]` - Project name
- `[Current User]` or `[Author]` - Author name
- `[tags]` or `[Tags]` - Comma-separated tags
- `[CHECKBOX_UNCHECKED]` or `[CHECKBOX INCOMPLETE]` - Empty checkbox `- [ ]`
- `[CHECKBOX_CHECKED]` or `[CHECKBOX COMPLETE]` - Checked checkbox `- [x]`

**Custom Tags:**
Any tag in square brackets `[TagName]` can be used in templates and will prompt for user input during note creation.

---

## Front Matter Structure

Front matter is YAML-formatted metadata at the beginning of each note, enclosed in `---` markers.

### Standard Front Matter Fields

```yaml
---
title: Meeting Weekly Stakeholder Meeting
id: 20260803120000
sub id: 001
type: project-meeting
created: 2026-08-03 12:00:00
modified: 2026-08-03 12:00:00
start date: 2026-08-03 12:00:00
end date: 2026-08-03 13:00:00
retention: Long
tags: #p_ProjectName #meeting
keywords: stakeholders, review, status
project: ProjectName
author: username
private: No
---
```

### Field Descriptions

- **title**: Human-readable note title
- **id**: Unique identifier (timestamp in format defined in preferences)
- **sub id**: Optional sub-identifier for ordering related notes
- **type**: Note type (e.g., project-meeting, email, event, task)
- **created**: Creation timestamp
- **modified**: Last modification timestamp
- **start date**: Event/task start date
- **end date**: Event/task end date (used for Gantt charts)
- **retention**: Data retention policy (Long, Medium, Short)
- **tags**: Space-separated hashtags (project tags are auto-generated)
- **keywords**: Comma-separated search keywords
- **project**: Associated project name
- **author**: Note creator
- **private**: Whether note is private to vault owner

### Project Tags

Project tags are automatically generated from project names:
- Project name "UTC Project" becomes `#p_UTC_Project`
- Spaces are replaced with underscores
- Prefix `p_` indicates it's a project tag

---

## Working with Attachments

### `add-attachment.py` - Add File Attachments

Moves files from your downloads folder to the vault's attachment system and links them to notes.

**Features:**
- Scans attachment pickup folder (configurable in preferences)
- Shows 25 most recent files
- Links attachment to a recent note or project
- Automatic timestamp prefix for uniqueness
- Version control integration
- Automatically updates note with attachment link

**Usage:**
```bash
./add-attachment.py
```

**Workflow:**
1. Select a file from the attachment pickup folder
2. Choose a project (optional)
3. Select a recent note to attach to (optional)
4. File is moved to `_Attachments/` (or project's `_Attachments/`)
5. Link is added to the selected note

**Attachment Link Format:**
```markdown
### Attachments

[filename.pdf](./_Attachments/20260803120000_filename.pdf)
```

### `Add-ScreenCapture.py` - Add Screen Captures

Similar to `add-attachment.py` but specifically for screen captures.

**Features:**
- Scans screen capture folder (configurable in preferences)
- Shows 20 most recent captures
- Moves to project or vault root attachments
- Provides markdown link for embedding

**Usage:**
```bash
./Add-ScreenCapture.py
```

### Attachment Organization

**Vault-level attachments:**
```
root/
├── _Attachments/
│   ├── 20260803120000_document.pdf
│   └── 20260803120500_screenshot.png
```

**Project-level attachments:**
```
root/
├── _Projects/
    ├── ProjectName/
        ├── _Attachments/
        │   ├── 20260803120000_requirements.pdf
        │   └── 20260803120500_diagram.svg
```

---

## Atomic Notes Workflow

### `make-AtomicNotes.py` - Extract Atomic Thoughts

Converts sections of meeting or event notes into standalone atomic thought notes following the Zettelkasten methodology.

**What are Atomic Notes?**
Atomic notes are single-concept notes that capture one clear thought, idea, or piece of knowledge. They are highly reusable and form the foundation of a networked knowledge base.

**Features:**
- Processes meeting notes with discussion sections
- Extracts sections under "## Discussion Summary" or "## Summary" or "# Notes"
- Prompts for each subsection to create an atomic note
- Automatically creates backlinks to source note
- Replaces original content with transclusion links
- Maintains project association
- Version control integration

**Usage:**
```bash
./make-AtomicNotes.py
```

**Workflow:**
1. Select a recent note (typically a meeting or journal note)
2. Script identifies potential atomic thought sections (## or ### headings)
3. For each section, preview and decide whether to create atomic note
4. Select a project for the atomic note (can differ from source note)
5. Atomic note is created with backlink to source
6. Source note is updated with transclusion link

**Before:**
```markdown
## Discussion Summary

### API Design Patterns
We discussed using the repository pattern for data access...

### Performance Considerations
The team agreed that caching would be implemented...
```

**After:**
```markdown
## Discussion Summary

### API Design Patterns

![[./_Projects/ProjectName/20260803120000_atomic_APIDes.md]]

### Performance Considerations

![[./_Projects/ProjectName/20260803120100_atomic_Perfor.md]]
```

**Atomic Note Structure:**
```markdown
---
title: Atomic API Design Patterns
id: 20260803120000
type: project-idea
created: 2026-08-03 12:00:00
project: ProjectName
tags: #p_ProjectName #architecture
---

**API Design Patterns**

We discussed using the repository pattern for data access...

[[20260803115500_meeting_technical_review.md]]
```

---

## Daily Journal

The daily journal serves as a chronological log of activities and notes.

### Creating/Opening Journal

```bash
./open-journal.py
```

- If today's journal exists, it opens it
- If not, it creates a new journal from the template
- Journal titles follow format: "Daily Journal YYYY-MM-DD"

### Journal Integration

When creating notes via `add-note.py`, you can optionally add them to today's journal. The script will:
1. Check if a journal exists for the note's date
2. Prompt you to add the note to the journal
3. Insert a time-stamped link to the new note

**Journal Entry Format:**
```markdown
## 12:00

[[20260803120000_meeting_stakeholder_review.md]]
- Meeting with stakeholders about project status
```

### Journal Configuration

In preferences (`Personal-Knowledge-Vault.json`):
```json
"include_notes_in_DailyJournal": "True"
```

---

## Project Notes

### Project Selection

When creating project notes, you'll select from existing projects in `_Projects/`. The script will:
- List all project folders
- Show archived projects separately
- Allow creating new projects
- Associate the note with the selected project

### Project Hub Notes

Each project can have a "Project Brief.md" (hub note) that serves as the central reference point. This is created using the `project_hub_template.markdown`.

**Hub notes are single-instance**, meaning only one can exist per project. Attempting to create another will open the existing one.

### Project Note Organization

```
_Projects/
├── ProjectName/
    ├── Project Brief.md                          # Hub (single instance)
    ├── budget.md                                 # Budget (single instance)
    ├── schedule.md                               # Schedule (single instance)
    ├── milestones.md                             # Milestones (single instance)
    ├── 20260803120000_meeting_kickoff.md         # Meeting note
    ├── 20260803130000_progress_Progress.md       # Progress note
    ├── 20260804090000_task_APIImpl.md            # Task note
    ├── 20260804100000_risk_VendorDel.md          # Risk note
    └── _Attachments/
        ├── 20260803120000_requirements.pdf
        └── 20260803130000_diagram.svg
```

### Single-Instance Note Types

These note types can only exist once per project:
- `hub` - Project Brief
- `budget` - Budget
- `schedule` - Schedule
- `milestones` - Milestones
- `scope` - Scope
- `executive_summary` - Executive Summary
- `roi` - ROI Analysis
- `introduction` - Project Introduction
- `documentation` - Documentation
- `transition_plan` - Transition Plan

### Multi-Instance Note Types

These can have multiple instances:
- `event` - Events
- `email` - Emails
- `chat` - Chats
- `issue` - Issues
- `idea` - Ideas
- `task` - Tasks
- `risk` - Risks
- `decision` - Decisions
- `assumption` - Assumptions
- `dependency` - Dependencies
- `meeting` - Meetings
- `progress` - Progress notes
- `report` - Reports
- `changerequest` - Change requests

---

## Best Practices

### Naming and Organization

1. **Use Timestamps**: All notes get unique timestamp IDs automatically
2. **Meaningful Titles**: Keep titles concise but descriptive (they appear in filenames)
3. **Project Association**: Link notes to projects when relevant for better organization
4. **Tag Consistently**: Use tags for cross-cutting themes beyond project boundaries

### Template Customization

1. **Custom Templates**: Create your own templates in `_templates/`
2. **Naming Convention**: Use `pkv_` prefix for general notes, `project_` for project notes
3. **Template Suffix**: End with `_template.markdown` or `_template.md`
4. **Merge Tags**: Use `[TagName]` for custom merge tags

### Atomic Note-Taking

1. **One Concept Per Note**: Each atomic note should capture a single, complete thought
2. **Descriptive Titles**: Make atomic note titles self-explanatory
3. **Use Backlinks**: Always maintain connections to source material
4. **Regular Processing**: Process meeting notes into atomic notes regularly

### Version Control

All note operations are automatically committed to version control with descriptive messages:
- "Added new meeting note: Weekly Review on 2026-08-03 12:00:00"
- "moved 'API Design' section from fleeting note to atomic note"
- "Added attachment 'requirements.pdf' to 'Project Kickoff' note"

### Front Matter Hygiene

1. **Accurate Dates**: Use actual event dates, not creation dates
2. **Proper Retention**: Set appropriate retention policies
3. **Tag Discipline**: Use consistent tag naming
4. **Keywords**: Add searchable keywords for better discovery

### Journal Workflow

1. **Daily Ritual**: Open journal at start of day with `./open-journal.py`
2. **Link Notes**: Link important notes to journal for chronological reference
3. **Time Stamps**: Use time-based headings (## 09:00, ## 14:30) for activities
4. **Weekly Review**: Review past journals to extract atomic notes

### Attachment Management

1. **Timely Processing**: Process attachments shortly after saving to downloads
2. **Project Association**: Always link attachments to notes when possible
3. **Descriptive Names**: Original filenames are preserved, so name files meaningfully
4. **Cleanup**: Regularly archive old attachments not linked to active notes

### Note Lifecycle

1. **Creation**: Use appropriate templates via `add-note.py`
2. **Enhancement**: Add attachments, tags, and links as you work
3. **Atomization**: Extract atomic thoughts from meeting/event notes
4. **Linking**: Create backlinks to build your knowledge network
5. **Archiving**: Move completed project notes when projects are archived

---

## Preferences Configuration

Note-adding behavior is controlled by preferences in `Personal-Knowledge-Vault.json`:

```json
{
    "timestamp_id_format": "%Y%m%d%H%M%S",
    "date_format": "%Y-%m-%d",
    "datetime_format": "%Y-%m-%d %H:%M:%S",
    
    "pkv_root": "PKV",
    "attachments_root": "_Attachments",
    "projects_root": "_Projects",
    "template_path": "default",
    
    "default_editor": "code",
    "show_tag_prompt": "False",
    "automatically_open_event_notes": "False",
    "include_notes_in_DailyJournal": "True",
    
    "author_name": "default",
    "attachmentPickUp_path": "default",
    "screenCapture_path": "default"
}
```

### Key Settings for Note-Adding

- **timestamp_id_format**: Format for unique note identifiers (default ISO 8601)
- **show_tag_prompt**: Whether to prompt for tags during note creation
- **automatically_open_event_notes**: Auto-open event notes in editor after creation
- **include_notes_in_DailyJournal**: Offer to link new notes to today's journal
- **default_editor**: Command to open notes (`code`, `zed`, `nano`, etc.)
- **template_path**: Location of templates ("default" uses `_templates/`)

---

## Troubleshooting

### Template Not Found
**Problem**: "Template 'xxx' not found"  
**Solution**: Ensure template exists in `_templates/` folder with proper naming convention

### Duplicate Note Warning
**Problem**: "A note of type 'hub' already exists"  
**Solution**: This is expected behavior for single-instance note types. The existing note will be opened.

### Attachment Pickup Folder Empty
**Problem**: "No files found in attachment pick up folder"  
**Solution**: 
- Check preferences setting for `attachmentPickUp_path`
- Ensure files exist in your downloads folder
- Hidden files and `DESKTOP.INI` are automatically excluded

### Journal Not Linking Notes
**Problem**: Notes not being offered to link to journal  
**Solution**: 
- Check `include_notes_in_DailyJournal` preference setting
- Ensure journal note exists for the date
- Journal must match format "Daily Journal YYYY-MM-DD"

### Template Merge Tags Not Replaced
**Problem**: Merge tags like `[Title]` appear in final note  
**Solution**:
- Ensure you provided values when prompted
- Check for typos in custom template merge tags
- Use standard merge tag names for automatic replacement

---

## Related Documentation

- [ReadMe.md](ReadMe.md) - Main project overview and vault structure
- [ReadMe_ProjectManagement.md](ReadMe_ProjectManagement.md) - Project management workflows
- [ReadMe_SharingNotes.md](ReadMe_SharingNotes.md) - Sharing and exporting notes
- [ReadMe Journal.md](ReadMe%20Journal.md) - Daily journal workflows

---

## Command Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `add-note.py` | Create any type of note | `./add-note.py` |
| `add-projectProgressNote.py` | Create project progress note | `./add-projectProgressNote.py [ProjectName]` |
| `pm-add_weekly_progress_notes.py` | Bulk create weekly progress notes | `./pm-add_weekly_progress_notes.py` |
| `open-journal.py` | Open or create today's journal | `./open-journal.py` |
| `make-AtomicNotes.py` | Extract atomic thoughts from notes | `./make-AtomicNotes.py` |
| `add-attachment.py` | Add file attachment to note | `./add-attachment.py` |
| `Add-ScreenCapture.py` | Add screen capture to vault | `./Add-ScreenCapture.py` |

---

*Last Updated: 2026-08-03*
