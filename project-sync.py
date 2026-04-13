#!/usr/bin/env python3

import os
import shutil
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Preferences as myPreferences
from _library import Tools as myTools
from _library import Inputs as myInputs 
from _library import Notes as myNotes

myTerminal.clearTerminal()
selectedProject: str = ""

print(f"{myTerminal.INFORMATION}Sync Project Content with a shared team folder{myTerminal.RESET}\n")
print("")

#debug
selectedProject = "Adaptive Project Management Software"

if selectedProject == "":
    print("Available target projects:")
    selectedProjectInput = myInputs.select_project_name(False, False)
    if selectedProjectInput is not None:
        selectedProject = selectedProjectInput

if selectedProject == "":
    print(f"{myTerminal.WARNING}No project selected.{myTerminal.RESET}")
    exit(1)

projectConfig = myProjects.get_ProjectConfig_as_dict(selectedProject)

if projectConfig is None:
    print(f"{myTerminal.WARNING}No project configuration found for project '{selectedProject}'.{myTerminal.RESET}")
    exit(1)

if not projectConfig.get("Sync", False):
    print(f"{myTerminal.WARNING}Project '{selectedProject}' is not configured for syncing.{myTerminal.RESET}\nEdit the project config if this project should be synced.")
    exit(1)

#get physical locations for the sync 
synchFolderPath = projectConfig.get("PublicShareFolder", "")
synchFolderAttachmentPath = os.path.join(synchFolderPath, "_Attachments") if synchFolderPath else ""
synchFolderLogFilePath = os.path.join(synchFolderPath, "sync_log.txt") if synchFolderPath else ""


def log_sync_action(action, details):
    if synchFolderLogFilePath:
        with open(synchFolderLogFilePath, "a") as logFile:
            logFile.write(f"{myTools.now_YYYY_MM_DD_HH_MM_SS()} - {action}: {details} {myPreferences.author_name()}\n")

def syncNoteAttachments(note):
    
    noteAttachments = myNotes.get_attachments_from_note(note)
    if not noteAttachments:
        return
    
    for attachment in noteAttachments:
        notePath = note.filePath.replace(note.fileName, "")

        #attachments can be found in the "_Attachments" folder or the the project root folder, check both places for the source attachment file

        if attachment.startswith("./"):
            sourceAttachmentPath = os.path.join(notePath, attachment[2:])
            targetAttachmentPath = os.path.join(synchFolderPath, attachment[2:])
        else:
            sourceAttachmentPath = os.path.join(notePath, attachment)
            targetAttachmentPath = os.path.join(synchFolderPath, attachment)
            

        if not os.path.exists(sourceAttachmentPath):
            print(f"{myTerminal.WARNING}Attachment '{attachment}' not found in expected location for note '{note.fileName}'.{myTerminal.RESET}")
            continue
            

        
        if not os.path.exists(targetAttachmentPath):
            try:
                shutil.copy2(sourceAttachmentPath, targetAttachmentPath)
                log_sync_action("COPY_ATTACHMENT", f"Copied attachment '{attachment}' for note '{note.fileName}'")
                print(f"{myTerminal.SUCCESS}Copied attachment '{attachment}' for note '{note.fileName}'.{myTerminal.RESET}")
            except Exception as e:
                print(f"{myTerminal.ERROR}Failed to copy attachment '{attachment}' for note '{note.fileName}': {e}{myTerminal.RESET}")
                log_sync_action("COPY_ATTACHMENT_FAILED", f"Failed to copy attachment '{attachment}' for note '{note.fileName}': {e}")
        else:
            if os.path.getmtime(sourceAttachmentPath) > os.path.getmtime(targetAttachmentPath):
                try:
                    shutil.copy2(sourceAttachmentPath, targetAttachmentPath)
                    log_sync_action("UPDATE_ATTACHMENT", f"Updated attachment '{attachment}' for note '{note.fileName}'")
                    print(f"{myTerminal.SUCCESS}Updated attachment '{attachment}' for note '{note.fileName}'.{myTerminal.RESET}")
                except Exception as e:
                    print(f"{myTerminal.ERROR}Failed to update attachment '{attachment}' for note '{note.fileName}': {e}{myTerminal.RESET}")
                    log_sync_action("UPDATE_ATTACHMENT_FAILED", f"Failed to update attachment '{attachment}' for note '{note.fileName}': {e}")

def syncRemoteNoteAttachments(note):
    
    remoteNoteAttachments = myNotes.get_attachments_from_note(note)
    if not remoteNoteAttachments:
        return
    
    remoteNoteFileAndPath = os.path.join(os.path.join(myPreferences.root_projects(), selectedProject), note.fileName).replace(".md", f"_{note.author}.md")
    remoteNoteContent = ""

    #Open the remotenote file and copy file content into variable
    with open(remoteNoteFileAndPath, "r") as remoteNoteFile:
        remoteNoteContent = remoteNoteFile.read()

    for remoteAttachment in remoteNoteAttachments:
        selectedProjectPath = os.path.join(myPreferences.root_projects(), selectedProject)
        
        newRemoteAttachmentLink = ""
        attachmentFileName = os.path.basename(remoteAttachment)

        if remoteAttachment.startswith("./"):
            sourceAttachmentPath = os.path.join(synchFolderPath, remoteAttachment[2:])
            newRemoteAttachmentLink = remoteAttachment[2:].replace(attachmentFileName, "R_" + note.fileName.replace(".md", "_").replace(" ", "_") + "_" + attachmentFileName)
            targetAttachmentPath = os.path.join(selectedProjectPath, newRemoteAttachmentLink)
        else:
            sourceAttachmentPath = os.path.join(synchFolderPath, remoteAttachment)
            newRemoteAttachmentLink = "R_" + note.fileName.replace(".md", "_").replace(" ", "_") + "_" + attachmentFileName
            targetAttachmentPath = os.path.join(selectedProjectPath, newRemoteAttachmentLink)
            
        if not os.path.exists(sourceAttachmentPath):
            print(f"{myTerminal.WARNING}Attachment '{remoteAttachment}' not found in expected location for note '{note.fileName}'.{myTerminal.RESET}")
            continue
        
        needsToBeRetrieved = False
        if not os.path.exists(targetAttachmentPath):
            needsToBeRetrieved = True
        else:
            if os.path.getmtime(sourceAttachmentPath) > os.path.getmtime(targetAttachmentPath):
                needsToBeRetrieved = True
        
        if needsToBeRetrieved:        
            try:
                shutil.copy2(sourceAttachmentPath, targetAttachmentPath)
                log_sync_action("COPY_ATTACHMENT", f"Copied attachment '{remoteAttachment}' for note '{note.fileName}'")
                #Update the attachment path in the remote note content to point to the new local attachment path
                remoteNoteContent = remoteNoteContent.replace(f"{remoteAttachment}]", f"{newRemoteAttachmentLink}]")
                remoteNoteContent = remoteNoteContent.replace(f"{remoteAttachment})", f"{newRemoteAttachmentLink})")
                print(f"{myTerminal.SUCCESS}Copied attachment '{remoteAttachment}' for note '{note.fileName}'.{myTerminal.RESET}")
            except Exception as e:
                print(f"{myTerminal.ERROR}Failed to copy attachment '{remoteAttachment}' for note '{note.fileName}': {e}{myTerminal.RESET}")
                log_sync_action("COPY_ATTACHMENT_FAILED", f"Failed to copy attachment '{remoteAttachment}' for note '{note.fileName}': {e}")
        
    #After processing all attachments, update the remote note file with the new content (with updated attachment links)
    with open(remoteNoteFileAndPath, "w") as remoteNoteFile:
        remoteNoteFile.write(remoteNoteContent)

if synchFolderPath is None or synchFolderPath == "":
    print(f"{myTerminal.WARNING}No sync folder path configured for project '{selectedProject}'.{myTerminal.RESET}\nEdit the project config to add the sync folder path.")
    exit(1)

if not os.path.exists(synchFolderPath):
    print(f"{myTerminal.WARNING}Sync folder path '{synchFolderPath}' does not exist for project '{selectedProject}'.{myTerminal.RESET}")
    if myInputs.ask_yes_no_from_user("Do you want to create the sync folder?"):
        try:
            os.makedirs(synchFolderPath)
            log_sync_action("CREATE_FOLDER", f"Sync folder created at '{synchFolderPath}'")
            print(f"{myTerminal.SUCCESS}Sync folder created at '{synchFolderPath}'.{myTerminal.RESET}")
            
        except Exception as e:
            print(f"{myTerminal.ERROR}Failed to create sync folder: {e}{myTerminal.RESET}")
            exit(1)

if not os.path.exists(synchFolderAttachmentPath):
    try:
        os.makedirs(synchFolderAttachmentPath)
        log_sync_action("CREATE_FOLDER", f"Sync attachments folder created at '{synchFolderAttachmentPath}'")
        print(f"{myTerminal.SUCCESS}Sync attachments folder created at '{synchFolderAttachmentPath}'.{myTerminal.RESET}")
    
    except Exception as e:
        print(f"{myTerminal.ERROR}Failed to create sync attachments folder: {e}{myTerminal.RESET}")
        exit(1)


projectNotes = myNotes.get_Notes_as_list(os.path.join(myPreferences.root_projects(), selectedProject), includePrivateNotes=False)

sendCount = 0
retrieveCount = 0
print ("Starting send process...")
for note in projectNotes:
    
    if note.author != myPreferences.author_name():
        #print(f"{myTerminal.INFORMATION}Skipping note '{note.fileName}' (authored by {note.author}){myTerminal.RESET}")
        continue
    
    targetNotePath = os.path.join(synchFolderPath, note.fileName)
    if not os.path.exists(targetNotePath):
        #copy note file to the target sync folder
        try:
            shutil.copy2(note.filePath, targetNotePath)
            syncNoteAttachments(note)
            log_sync_action("COPY_NOTE", f"Copied note '{note.fileName}' to sync folder")
            print(f"{myTerminal.SUCCESS}Copied note '{note.fileName}' to sync folder.{myTerminal.RESET}")
            sendCount += 1
        except Exception as e:
            print(f"{myTerminal.ERROR}Failed to copy note '{note.fileName}' to sync folder: {e}{myTerminal.RESET}")
            log_sync_action("COPY_NOTE_FAILED", f"Failed to copy note '{note.fileName}' to sync folder: {e}")
    else:
        if os.path.getmtime(note.filePath) > os.path.getmtime(targetNotePath):
            #source note is newer than target note, copy it
            try:
                shutil.copy2(note.filePath, targetNotePath)
                syncNoteAttachments(note)
                log_sync_action("UPDATE_NOTE", f"Updated note '{note.fileName}' in sync folder")
                print(f"{myTerminal.SUCCESS}Updated note '{note.fileName}' in sync folder.{myTerminal.RESET}")
                sendCount += 1
            except Exception as e:
                print(f"{myTerminal.ERROR}Failed to update note '{note.fileName}' in sync folder: {e}{myTerminal.RESET}")
                log_sync_action("UPDATE_NOTE_FAILED", f"Failed to update note '{note.fileName}' in sync folder: {e}")

print(f"Send process completed. {sendCount} notes sent to sync folder.")

if not myInputs.ask_yes_no_from_user("Do you want retrieve any files from the sync folder (for example, copy your team's notes locally)?"):
    print("Sync process finished.")
    exit(0)

# get notes from the sync folder and copy them to the local project folder if the 
#note is newer and the author is not the current user (to avoid copying back your own notes)

remoteNotes = myNotes.get_Notes_as_list(synchFolderPath, includePrivateNotes=False)

if len(remoteNotes) == 0:
    print(f"{myTerminal.INFORMATION}No notes found in sync folder to retrieve.{myTerminal.RESET}")
    exit(0)

print("Starting retrieve process...")
for remoteNote in remoteNotes:
    if remoteNote.author == myPreferences.author_name():
        #print(f"{myTerminal.INFORMATION}Skipping note '{remoteNote.fileName}' (authored by current user){myTerminal.RESET}")
        continue
    
    
    localNotePath = os.path.join(myPreferences.root_projects(), selectedProject, remoteNote.fileName.replace(".md", f"_{remoteNote.author}.md"))
    needsToBeRetrieved = False
    if not os.path.exists(localNotePath):
        needsToBeRetrieved = True
    else:
        if os.path.getmtime(os.path.join(synchFolderPath, remoteNote.fileName)) > os.path.getmtime(localNotePath):
            needsToBeRetrieved = True
    
    if needsToBeRetrieved:
        #remote note is newer than local note, copy it
        try:
            shutil.copy2(os.path.join(synchFolderPath, remoteNote.fileName), localNotePath)
            log_sync_action("UPDATE_REMOTE_NOTE", f"Updated local note '{remoteNote.fileName}' from sync folder")
            syncRemoteNoteAttachments(remoteNote)
            print(f"{myTerminal.SUCCESS}Updated local note '{remoteNote.fileName}' from sync folder.{myTerminal.RESET}")
            retrieveCount += 1
        except Exception as e:
            print(f"{myTerminal.ERROR}Failed to update local note '{remoteNote.fileName}' from sync folder: {e}{myTerminal.RESET}")
            log_sync_action("UPDATE_REMOTE_NOTE_FAILED", f"Failed to update local note '{remoteNote.fileName}' from sync folder: {e}")

print(f"Retrieve process completed. {retrieveCount} notes retrieved from sync folder.")
print("Sync process finished.")
