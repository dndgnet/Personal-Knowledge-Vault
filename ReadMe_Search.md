# Searching Notes in Personal Knowledge Vault

## Overview

The Personal Knowledge Vault provides a powerful, iterative search system through the `search-notes.py` script. Unlike simple text search, this tool allows you to build complex search queries by progressively narrowing down results through multiple criteria, with the ability to undo searches and view search history.

## Table of Contents

- [Quick Start](#quick-start)
- [How Search Works](#how-search-works)
- [Interactive Search Mode](#interactive-search-mode)
- [Search Criteria](#search-criteria)
- [Search Commands](#search-commands)
- [Command-Line Mode](#command-line-mode)
- [Search Results Management](#search-results-management)
- [Export and Timeline Features](#export-and-timeline-features)
- [Best Practices](#best-practices)
- [Examples](#examples)

---

## Quick Start

### Basic Interactive Search

```bash
./search-notes.py
```

The script will:
1. Load all notes from your vault into memory
2. Create an `AllNotes.json` index file
3. Present an interactive search menu
4. Allow progressive filtering with multiple criteria
5. Let you view, open, or export results

### Quick Command-Line Search

```bash
# Search for notes in a specific project
./search-notes.py -p "ProjectName"

# Search for text in note bodies
./search-notes.py -b "API design"

# Search by note type
./search-notes.py -ty meeting

# Chain multiple criteria
./search-notes.py -p "ProjectName" -ty meeting -d 2026-01-01 2026-12-31
```

---

## How Search Works

### Initialization Phase

When you run `search-notes.py`, it performs the following steps:

1. **Note Collection**: Scans the entire PKV directory structure
   - Includes private notes
   - Includes archived projects
   - Parses front matter and note body

2. **Index Creation**: Creates `AllNotes.json` in the PKV root
   - Serialized NoteData objects
   - Enables fast search operations
   - Updated each time you run search

3. **Search State Management**: Maintains search history
   - Each search creates a snapshot
   - Allows undo operations
   - Tracks search criteria in log

### Progressive Filtering

Search operates on a **progressive refinement model**:
- Start with all notes
- Apply first filter → subset of notes
- Apply second filter → subset of subset
- Continue narrowing until you find what you need
- Use "undo" to step back if you filtered too much

### Search History

Each search operation:
- Records the criteria used
- Saves the resulting note set
- Timestamps the operation
- Allows rollback to any previous state

---

## Interactive Search Mode

### Search Menu

After loading notes, you'll see the interactive menu:

```
Search options:
   d)  date range - Search by note date
  ta)  tags - Search by tags
  ti)  title - Search by title
  ty)  type - Search by type
   b)  body - Search by body text

   p)  project - Search by project
  np)  No project - Search for notes not attached to project
 nap)  Not an archived project - Search for notes not attached to archived project

 npn)  No private notes - Search excluding private notes
 opn)  Only private notes - Search for only private notes
 --------------------
Commands:
   h)  history - show search history
   u)  undo - undo the last search
   l)  list - list current search results
   x)  export - export and open results in editor
   q)  quit - Quit the search
 --------------------
```

### Interactive Workflow

1. **Choose a search criterion** from the menu
2. **Provide search parameters** when prompted
3. **Review result count** displayed after each search
4. **Refine further** by applying additional criteria
5. **List results** when ready to view matches
6. **Open notes** or export timeline

---

## Search Criteria

### Date Range (`d`)

Search notes within a specific date range based on the note's date field.

**Interactive Mode:**
```
Enter your choice: d
Enter start date (YYYY-MM-DD) or leave blank for no start date: 2026-01-01
Enter end date (YYYY-MM-DD) or leave blank for no end date: 2026-06-30
```

**Features:**
- Blank start date = beginning of time (1899-01-01)
- Blank end date = current date/time
- Supports natural language (handled by datetime parser)
- Inclusive of both start and end dates

### Tags (`ta`)

Search notes containing specific tags from their front matter.

**Interactive Mode:**
```
Enter your choice: ta
[Displays list of all tags from current result set]
Select a tag: #p_ProjectName
```

**Features:**
- Shows only tags present in current result set
- Narrows progressively with each tag search
- Matches tags from front matter `tags:` field
- Case-sensitive matching

### Title (`ti`)

Search for text within note titles.

**Interactive Mode:**
```
Enter your choice: ti
Enter a part of the title to search for: meeting
```

**Features:**
- Case-insensitive substring matching
- Searches in note title field only
- Partial matches accepted

### Type (`ty`)

Search notes by their type (meeting, email, task, etc.).

**Interactive Mode:**
```
Enter your choice: ty
[Displays list of templates/types]
Select a type: meeting
```

**Features:**
- Based on note type from front matter
- Shows available templates
- Matches both `project-meeting` and `meeting` types
- Template names automatically cleaned (removes `_template.markdown`)

### Body (`b`)

Search for text anywhere within the note body content.

**Interactive Mode:**
```
Enter your choice: b
Enter a part of the body to search for: API design
```

**Features:**
- Case-insensitive full-text search
- Searches entire note body
- Most comprehensive but slowest search
- Good for finding specific terms or concepts

### Project (`p`)

Filter notes belonging to a specific project.

**Interactive Mode:**
```
Enter your choice: p
[Displays list of projects]
Select a project: ProjectName
```

**Features:**
- Matches project field in front matter
- Also matches project tags (e.g., `#p_ProjectName`)
- Essential for project-specific searches

### No Project (`np`)

Find notes that are not associated with any project.

**Features:**
- Filters notes with empty project field
- Useful for finding vault-level notes
- Good for discovering orphaned notes

### Not Archived Project (`nap`)

Exclude notes from archived projects.

**Features:**
- Filters out notes marked as archived
- Based on `archivedProject` flag
- Useful for focusing on active work

### No Private Notes (`npn`)

Exclude private notes from results.

**Features:**
- Filters notes with `private: Yes` in front matter
- Good for preparing shareable results
- Respects privacy settings

### Only Private Notes (`opn`)

Show only private notes.

**Features:**
- Opposite of `npn`
- Filters to notes with `private: Yes`
- Useful for personal review

---

## Search Commands

### History (`h`)

Display the complete search history for the current session.

**Output Example:**
```
Project = ProjectName  (42 records)
date range from 2026-01-01 00:00:00 to 2026-06-30 23:59:59  (28 records)
note type = meeting  (12 records)
```

**Features:**
- Shows all search steps chronologically
- Displays record count after each step
- Helps understand current filter state
- Does not change result set

### Undo (`u`)

Roll back the last search operation.

**Behavior:**
- Restores result set to previous state
- Decrements search index
- Can be used multiple times
- Cannot undo past the initial state (all notes)

**Example:**
```
Enter your choice: u
Undo to search index 2
Found 28 notes matching the search criteria.
```

### List (`l`)

Display current search results in a formatted table.

**Display Format:**
```
  id   Datetime              Project                          Note Title
____   ________              _______                          __________
   1)  2026-06-15 14:30:00   ProjectName                      Weekly Review Meeting
   2)  2026-06-08 14:30:00   ProjectName                      Weekly Review Meeting
   3)  2026-06-01 14:30:00   ProjectName                      Weekly Review Meeting
...

   a)  open All
   x)  eXport search result timeline

Enter the note id to open or enter to continue searching:
```

**Actions from List View:**
- **Enter a number**: Opens that specific note in your editor
- **Type 'a'**: Opens all search results in your editor
- **Type 'x'**: Exports search timeline (see below)
- **Press Enter**: Returns to search menu
- **Type 'q'**: Quits the search

**Features:**
- Color-coded alternating rows (white/grey)
- Sorted by date (most recent first)
- Auto-adjusts column widths based on terminal size
- Shows note ID, datetime, project, and title

### Export (`x`)

Export search results to a markdown file with metadata.

**Output File:** `.SearchResults.md` (in PKV root)

**Contents:**
```markdown
---
title: Search Results
date: 2026-08-03 14:30:00
---
# Search Steps

- Project = ProjectName  (42 records)
- date range from 2026-01-01 00:00:00 to 2026-06-30 23:59:59  (28 records)
- note type = meeting  (12 records)

# Search Results 2026-08-03 14:30:00

## Weekly Review Meeting
**Project:** ProjectName
**Date:** 2026-06-15 14:30:00
**Tags:** #p_ProjectName, #meeting
**Link:** [[20260615143000_meeting_WeeklyReview.md]]

## Weekly Review Meeting
**Project:** ProjectName
**Date:** 2026-06-08 14:30:00
**Tags:** #p_ProjectName, #meeting
**Link:** [[20260608143000_meeting_WeeklyReview.md]]
```

**Features:**
- Documents search steps taken
- Includes links to each note
- Opens automatically in default editor
- Overwrites previous search results

### Quit (`q`)

Exit the search script.

**Behavior:**
- Saves search log to `search.log` in PKV root
- Useful for troubleshooting
- Can be reviewed later if needed

---

## Command-Line Mode

For quick searches or scripting, use command-line parameters to skip the interactive menu.

### Command-Line Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `-b "text"` | Search body for text | `-b "API design"` |
| `-p "project"` | Search by project | `-p "ProjectName"` |
| `-ti "text"` | Search title for text | `-ti "meeting"` |
| `-ty "type"` | Search by note type | `-ty meeting` |
| `-d start end` | Date range (YYYY-MM-DD) | `-d 2026-01-01 2026-12-31` |
| `-np` | No project (vault-level notes) | `-np` |
| `-nap` | Not archived project | `-nap` |
| `-npn` | No private notes | `-npn` |
| `-opn` | Only private notes | `-opn` |
| `-today` | Today's notes | `-today` |
| `-yesterday` | Yesterday's notes | `-yesterday` |
| `-lastweek` | Last week's notes | `-lastweek` |
| `-lastmonth` | Last month's notes | `-lastmonth` |

### Chaining Parameters

Combine multiple parameters in a single command:

```bash
# Find all meeting notes in ProjectName from last month
./search-notes.py -p "ProjectName" -ty meeting -lastmonth

# Find non-private notes about "budget" in active projects
./search-notes.py -b "budget" -nap -npn

# Find today's notes with specific title text
./search-notes.py -today -ti "review"
```

### Date Shortcuts

Pre-configured date range shortcuts:

**`-today`**
```bash
./search-notes.py -today
# Searches notes from today only
```

**`-yesterday`**
```bash
./search-notes.py -yesterday
# Searches notes from yesterday
```

**`-lastweek`**
```bash
./search-notes.py -lastweek
# Searches notes from the previous week (Monday-Sunday)
```

**`-lastmonth`**
```bash
./search-notes.py -lastmonth
# Searches notes from the previous calendar month
```

---

## Search Results Management

### Opening Notes

**Single Note:**
From the list view, enter the note number to open it in your default editor.

**Multiple Notes:**
Type `a` in the list view to open all search results simultaneously.

**Behavior:**
- Uses default editor from preferences
- Opens each note in a new tab/window
- Returns to search after opening
- Allows continued refinement

### Result Count

After each search operation, the system displays:
```
Found 12 notes matching the search criteria.
```

This helps you understand:
- Whether your search is too broad (too many results)
- Whether your search is too narrow (zero or few results)
- When to refine further or undo

### Search State

The search maintains:
- **Current results**: Notes matching all applied filters
- **Search history**: Each previous result set
- **Search index**: Current position in history
- **Search log**: Timestamped list of operations

---

## Export and Timeline Features

### Timeline Export (`x` from list view)

Creates a rich timeline document with:

**File Generated:** `_Search Timeline.md` (in PKV root)

**Contents Include:**
1. **Search Description**: All search steps taken
2. **Timeline View**: Chronological list of notes
3. **Note Bodies**: Full content of each note
4. **Backlinks**: Links to related notes
5. **Gantt Chart**: Visual timeline (if applicable)

**Features:**
- Opens in default editor
- Opens as HTML in default browser
- Includes Mermaid diagrams for visualization
- Overwrites previous timeline (prevents clutter)
- Prompts before overwriting

**Timeline Structure:**
```markdown
# Search Timeline

## Search Criteria
- Project = ProjectName
- Note type = meeting
- Date range from 2026-01-01 to 2026-06-30

## Timeline

### 2026-06-15 14:30:00 - Weekly Review Meeting
[Full note content here]
**Backlinks:** [[related-note.md]]

### 2026-06-08 14:30:00 - Weekly Review Meeting
[Full note content here]

## Gantt Chart
```mermaid
gantt
    title Project Timeline
    dateFormat YYYY-MM-DD
    ...
```

### HTML Export

Timeline is automatically opened in browser with:
- Rendered markdown
- Interactive Mermaid diagrams
- Clickable links
- Print-friendly formatting

---

## Best Practices

### Search Strategy

1. **Start Broad, Narrow Down**
   - Begin with project or date range
   - Add type filter
   - Refine with body text last

2. **Use Progressive Filtering**
   ```
   All notes (500) 
   → Project filter (50) 
   → Date range (30) 
   → Type filter (12)
   → Body text (3)
   ```

3. **Check Count After Each Step**
   - If zero results, undo and try different criteria
   - If too many results, add another filter
   - Sweet spot: 5-50 results

4. **Use History to Understand**
   - Type `h` regularly to see your search path
   - Helps identify which filter eliminated results
   - Documents your search for future reference

### Efficient Searching

**For Recent Work:**
```bash
./search-notes.py -lastweek -nap
```

**For Project Review:**
```bash
./search-notes.py -p "ProjectName" -ty progress
```

**For Finding Specific Topics:**
```bash
./search-notes.py -b "keyword" -nap -npn
```

**For Privacy Check:**
```bash
./search-notes.py -opn
```

### Working with Results

1. **Export Before Major Actions**
   - Use `x` to save results before bulk operations
   - Creates documentation of what you found
   - Allows sharing search results

2. **Open All Sparingly**
   - Opening 50+ notes can overwhelm your editor
   - Consider exporting timeline instead
   - Or refine search further

3. **Use Timeline for Analysis**
   - Timeline export provides overview
   - Good for identifying patterns
   - Useful for reports and reviews

### Search Patterns

**Finding Orphaned Notes:**
```bash
./search-notes.py -np
```

**Active Work Only:**
```bash
./search-notes.py -nap -npn
```

**Project Deliverables:**
```bash
./search-notes.py -p "ProjectName" -ty "report,documentation,executive_summary"
```

**Communication Trail:**
```bash
./search-notes.py -p "ProjectName" -ty "email,meeting,chat"
```

**Action Items:**
```bash
./search-notes.py -b "- [ ]" -nap
```

---

## Examples

### Example 1: Finding All Meetings for a Project

**Scenario:** Find all meeting notes for "UTC Project" from this year.

**Command Line:**
```bash
./search-notes.py -p "UTC Project" -ty meeting -d 2026-01-01 2026-12-31
```

**Interactive:**
```
Enter your choice: p
Select a project: UTC Project
Found 45 notes matching the search criteria.

Enter your choice: ty
Select a type: meeting
Found 18 notes matching the search criteria.

Enter your choice: d
Enter start date (YYYY-MM-DD): 2026-01-01
Enter end date (YYYY-MM-DD): 2026-12-31
Found 12 notes matching the search criteria.

Enter your choice: l
[Lists 12 meeting notes]
```

### Example 2: Finding Notes About a Specific Topic

**Scenario:** Find all notes mentioning "API design" in active projects.

**Command Line:**
```bash
./search-notes.py -b "API design" -nap
```

**Interactive:**
```
Enter your choice: b
Enter a part of the body to search for: API design
Found 8 notes matching the search criteria.

Enter your choice: nap
Found 7 notes matching the search criteria.

Enter your choice: l
[Lists 7 notes about API design]
```

### Example 3: Last Week's Work Summary

**Scenario:** Review all non-private notes from last week to prepare status report.

**Command Line:**
```bash
./search-notes.py -lastweek -npn
```

Then in list view, type `x` to export timeline for review.

### Example 4: Finding Incomplete Tasks

**Scenario:** Find all incomplete task checkboxes in active projects.

**Command Line:**
```bash
./search-notes.py -b "- [ ]" -nap -ty task
```

### Example 5: Recovering from Over-Filtering

**Scenario:** You filtered too much and got zero results.

**Interactive:**
```
Enter your choice: b
Enter a part of the body to search for: very-specific-term
Found 0 notes matching the search criteria.

Enter your choice: u
Undo to search index 3
Found 15 notes matching the search criteria.

Enter your choice: ti
Enter a part of the title to search for: specific
Found 2 notes matching the search criteria.

Enter your choice: l
[Lists 2 notes with "specific" in title]
```

### Example 6: Privacy Audit

**Scenario:** Review all private notes to ensure proper marking.

**Command Line:**
```bash
./search-notes.py -opn
```

**Interactive:**
```
Enter your choice: opn
Found 23 notes matching the search criteria.

Enter your choice: l
[Review each private note to confirm privacy marking]
```

---

## Technical Details

### AllNotes.json Structure

The search creates an index file with serialized note data:

```json
[
  {
    "id": "20260803143000",
    "fileName": "20260803143000_meeting_WeeklyReview.md",
    "filePath": "/path/to/vault/20260803143000_meeting_WeeklyReview.md",
    "date": "2026-08-03 14:30:00",
    "type": "project-meeting",
    "title": "Weekly Review Meeting",
    "project": "ProjectName",
    "tags": ["#p_ProjectName", "#meeting"],
    "author": "username",
    "private": false,
    "noteBody": "...",
    "frontMatter": "...",
    ...
  }
]
```

### Search Log Format

The `search.log` file captures all operations:

```
Search Log
2026-08-03 14:30:15.123456: Project = ProjectName  (45 records)
2026-08-03 14:30:32.654321: note type = meeting  (18 records)
2026-08-03 14:30:45.987654: date range from 2026-01-01 00:00:00 to 2026-12-31 23:59:59  (12 records)
2026-08-03 14:31:02.456789: quit search.
```

### Performance Considerations

**Initial Load Time:**
- Depends on vault size
- Typical: 1-3 seconds for 500 notes
- Index creation happens once per search session

**Search Speed:**
- Most filters are instant (< 100ms)
- Body text search is slowest (full-text scan)
- Date range filtering is fast (indexed)

**Memory Usage:**
- All notes loaded into memory
- Typically 5-50 MB depending on vault size
- Multiple search state snapshots maintained

---

## Troubleshooting

### AllNotes.json Creation Failed

**Problem:** "Failed to create AllNotes.json"  
**Solution:**
- Check write permissions on PKV root
- Ensure PKV path is correctly set in preferences
- Verify no corrupted note files

### No Notes Found

**Problem:** "Found 0 notes matching the search criteria"  
**Solutions:**
- Use `u` to undo last search
- Use `h` to review search history
- Check if search criteria were too restrictive
- Verify notes exist with those attributes

### Search Too Slow

**Problem:** Body text search takes a long time  
**Solutions:**
- Use more specific search criteria first (project, date, type)
- Narrow down before using body text search
- Consider searching smaller date ranges

### Terminal Width Issues

**Problem:** Note titles truncated or display garbled  
**Solution:**
- Resize terminal window wider
- Script auto-adjusts but needs minimum width
- Use export feature for better viewing

---

## Related Documentation

- [ReadMe.md](ReadMe.md) - Main project overview
- [ReadMe_AddingNotes.md](ReadMe_AddingNotes.md) - How to create searchable notes
- [ReadMe_ProjectManagement.md](ReadMe_ProjectManagement.md) - Project workflows
- [ReadMe_SharingNotes.md](ReadMe_SharingNotes.md) - Exporting search results

---

## Command Reference

### Interactive Commands

| Command | Action | Notes |
|---------|--------|-------|
| `d` | Date range search | Prompts for start/end dates |
| `ta` | Tag search | Shows available tags |
| `ti` | Title search | Case-insensitive substring |
| `ty` | Type search | Shows available types |
| `b` | Body text search | Full-text search |
| `p` | Project search | Shows available projects |
| `np` | No project filter | Vault-level notes only |
| `nap` | Not archived filter | Active projects only |
| `npn` | No private notes | Public notes only |
| `opn` | Only private notes | Private notes only |
| `h` | Show history | Displays search steps |
| `u` | Undo last search | Rolls back one step |
| `l` | List results | Shows formatted table |
| `x` | Export results | Creates .SearchResults.md |
| `q` | Quit | Saves log and exits |

### Command-Line Parameters

| Parameter | Purpose | Example |
|-----------|---------|---------|
| `-b` | Body text | `-b "meeting notes"` |
| `-p` | Project | `-p "ProjectName"` |
| `-ti` | Title text | `-ti "review"` |
| `-ty` | Note type | `-ty meeting` |
| `-d` | Date range | `-d 2026-01-01 2026-12-31` |
| `-np` | No project | `-np` |
| `-nap` | Not archived | `-nap` |
| `-npn` | No private | `-npn` |
| `-opn` | Only private | `-opn` |
| `-today` | Today only | `-today` |
| `-yesterday` | Yesterday only | `-yesterday` |
| `-lastweek` | Last week | `-lastweek` |
| `-lastmonth` | Last month | `-lastmonth` |

---

*Last Updated: 2026-08-03*
