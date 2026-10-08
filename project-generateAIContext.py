#!/usr/bin/env python3

import os
import sys 
import base64

from _library import Inputs as myInputs
from _library import Notes as myNotes
from _library import Preferences as myPreferences
from _library import Terminal as myTerminal
from _library import Tools as myTools

myTerminal.clearTerminal()

selectedProject = ""
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        selectedProject += arg + " "
    selectedProject = selectedProject.strip()
    print(f"Selected project from arguments: '{selectedProject}'")
    
    # Check if the provided project name exists in known projects
    known_projects = myTools.get_pkv_projects()
    if selectedProject not in known_projects:
        print(f"{myTerminal.WARNING}Project '{selectedProject}' not found in known projects.{myTerminal.RESET}")
        print("Will prompt user to select a valid project.")
        selectedProject = ""  # clear so code below prompts the user
    else:
        print(f"{myTerminal.SUCCESS}Valid known project: {selectedProject}{myTerminal.RESET}")

print(f"{myTerminal.INFORMATION}Generate AI Context File{myTerminal.RESET}\n")

# Use silent mode if project provided via argument; otherwise prompt once
if selectedProject == "":
    print("Available target projects:")
    selectedProject = myInputs.select_project_name(False, False)

if selectedProject is None or selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    sys.exit(1)

print(f"{myTerminal.SUCCESS}Selected project: {selectedProject}{myTerminal.RESET}")
print(f"Generating AI Context File for project: {selectedProject}")


def image_to_data_url(image_path: str) -> str:
    """Convert an image file to a data URL with base64 encoding."""
    if not os.path.exists(image_path):
        return f"[Image not found: {image_path}]"
    try:
        with open(image_path, "rb") as f:
            img_data = f.read()
        b64 = base64.b64encode(img_data).decode("utf-8")
        ext = image_path.lower().split(".")[-1]
        mime = {
            "png": "image/png",
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "gif": "image/gif",
            "webp": "image/webp",
            "bmp": "image/bmp",
            "svg": "image/svg+xml"
        }.get(ext, "image/png")
        return f"data:{mime};base64,{b64}"
    except Exception as e:
        return f"[Error embedding image {image_path}: {e}]"


def replace_images_with_data_urls(note_body: str, project_name: str) -> str:
    """Replace image links in the note body with embedded data URLs."""
    import re
    from _library import Preferences as myPrefs

    pkv_attachments = myPrefs.root_attachments()
    project_attachments = os.path.join(myPrefs.root_projects(), project_name, "_Attachments")
    if not os.path.exists(project_attachments):
        project_attachments = os.path.join(myPrefs.root_projects(), project_name, "attachments")  # fallback

    def replace_match(match):
        # Extract the image path (group 2 or 4 are the path groups in our patterns)
        img_ref = (match.group(2) or match.group(4) or "").strip()
        if not img_ref:
            img_ref = (match.group(1) or match.group(3) or "").strip()
        if not img_ref:
            return match.group(0)

        # Clean reference (remove display text after | and any trailing brackets)
        img_ref = img_ref.split("|")[0].strip().split("]")[0].strip()

        # Resolve full path - prefer project _Attachments, then root _Attachments
        possible_paths = []
        # The note uses relative path starting with ./
        if img_ref.startswith("./_Attachments/"):
            clean_name = img_ref.replace("./_Attachments/", "")
            possible_paths.append(os.path.join(project_attachments, clean_name))
        else:
            possible_paths.append(os.path.join(project_attachments, img_ref))
        possible_paths.append(os.path.join(pkv_attachments, img_ref))

        for path_candidate in possible_paths:
            if os.path.exists(path_candidate):
                data_url = image_to_data_url(path_candidate)
                # Return as markdown image with data URL
                return f"![{img_ref}]({data_url})"

        # If not found, leave original
        return match.group(0)

    # Match common image patterns including Obsidian-style with angle brackets:
    # ![alt](<path>), ![alt](path), ![[path]], [[path]]
    patterns = [
        r'!\[([^\]]*?)\]\(\s*<([^>]+)>\s*\)',   # ![alt](<path>)  -- this is the one used in the test note
        r'!\[([^\]]*?)\]\(([^)]+?)\)',           # ![alt](path)
        r'!\[\[([^\]]+)\]\]',                    # ![[path]]
        r'\[\[([^\]]+)\]\]'                      # [[path]]
    ]

    result = note_body
    for pattern in patterns:
        result = re.sub(pattern, replace_match, result, flags=re.IGNORECASE)

    return result


# Load all notes for the project (exclude private notes)
allNotes = myNotes.get_Notes_from_Project(selectedProject)

# Filter out private notes (note.private == True)
nonPrivateNotes = [note for note in allNotes if not note.private]

if not nonPrivateNotes:
    print(f"{myTerminal.WARNING}No non-private notes found for project '{selectedProject}'.{myTerminal.RESET}")
    sys.exit(1)

print(f"{myTerminal.SUCCESS}Loaded {len(nonPrivateNotes)} non-private note(s) (skipped {len(allNotes) - len(nonPrivateNotes)} private note(s)).{myTerminal.RESET}")

# Sort notes by date (oldest first)
sortedNotes = myNotes.sort_Notes_by_date(nonPrivateNotes, descending=False)

# Find executive summary if it exists (move to top). Executive summaries are typically not private.
executiveSummaryNote = None
regularNotes = []
for note in sortedNotes:
    if note.typeSimple.lower() == "executive_summary" or "executive_summary" in note.type.lower():
        executiveSummaryNote = note
    else:
        regularNotes.append(note)

# Reassemble list with executive summary at the top if present
orderedNotes = []
if executiveSummaryNote:
    orderedNotes.append(executiveSummaryNote)
    print(f"{myTerminal.SUCCESS}Found executive summary note - placing at top.{myTerminal.RESET}")
orderedNotes.extend(regularNotes)

# Build the AI Context File content
contextContent = f"""# AI Context File for {selectedProject}

**Generated**: {myTools.now_YYYY_MM_DD_HH_MM_SS() if hasattr(myTools, 'now_YYYY_MM_DD_HH_MM_SS') else 'now'}
**Total notes**: {len(orderedNotes)}
**Order**: Executive Summary (if present) first, then chronological by note.date

---

"""

for note in orderedNotes:
    note_date = note.date[:10] if len(note.date) >= 10 else note.date
    
    # Replace image links with embedded base64 data URLs
    processed_body = replace_images_with_data_urls(note.noteBody, selectedProject)
    
    contextContent += f"""## {note_date} - {note.title}

**Type**: {note.type}
**ID**: {note.id}

{processed_body.strip()}

---

"""
    
# Save to user's Downloads folder as "AI Context <Project Name>.md"
downloads_path = myPreferences.attachmentPickUp_path()
safe_project_name = "".join(c if c.isalnum() or c in " _-" else "_" for c in selectedProject).strip()
context_filename = f"AI Context {safe_project_name}.md"
contextFilePath = os.path.join(downloads_path, context_filename)

print(f"{myTerminal.INFORMATION}Saving to Downloads: {context_filename}{myTerminal.RESET}")

success = myTools.write_text_to_file(contextFilePath, contextContent)

if success:
    print(f"{myTerminal.SUCCESS}Successfully created: {contextFilePath}{myTerminal.RESET}")
    print(f"   - {len(orderedNotes)} notes included")
    if executiveSummaryNote:
        print(f"   - Executive summary placed at top")
    myTools.open_note_in_editor(contextFilePath)
else:
    print(f"{myTerminal.ERROR}Failed to write AI Context File.{myTerminal.RESET}")
    sys.exit(1)

print(f"\n{myTerminal.INFORMATION}AI Context File ready for use with LLMs or other tools.{myTerminal.RESET}")
