#!/usr/bin/env python3
import os 
import shutil
import subprocess
import time
import re 
from _library import Terminal as myTerminal
from _library import Projects as myProjects
from _library import Tools as myTools
from _library.Tools import NoteData
from _library import Preferences as myPreferences
from _library import Inputs as myInputs 
from _library import HTML as myHTML
from _library import Notes as myNotes


print("Downloading OneNote Project")
selectedProject = myInputs.select_project_name(showNewProjectOption=False, showNoProjectOption=False)


selectedProjects = []

if selectedProject == "":
    for filename in sorted(os.listdir(myPreferences.root_projects())):
        if os.path.isdir(os.path.join(myPreferences.root_projects(), filename)):
            projectConfig = myProjects.get_ProjectConfig_as_dict(filename)
            projectName = projectConfig.get("ProjectName", "")
            selectedProjects.append(projectName)
else:
    selectedProjects.append(selectedProject)


temporaryOneNoteExportFolder = myPreferences.temporaryOneNoteExportFolder()

if temporaryOneNoteExportFolder == "":
    print("Temporary OneNote Export Folder is not set in preferences. Please set it and try again.")
    exit()

if not os.path.exists(temporaryOneNoteExportFolder):
    os.makedirs(temporaryOneNoteExportFolder)
for selectedProject in selectedProjects:
    projectConfig = myProjects.get_ProjectConfig_as_dict(selectedProject)
    print(f"\t\tProcessing project '{selectedProject}' ---------------")
    configuredNotebookName = projectConfig.get("OneNote_noteBookName") or ""
    configuredSectionName = projectConfig.get("OneNote_sectionName") or ""

    if configuredNotebookName == "" or configuredSectionName == "":
        print(f"Project '{selectedProject}' does not have OneNote notebook or section configured. Please update the project configuration.")
        print(f"Skipping project '{selectedProject}'.")
        continue

    sectionName = configuredSectionName
    noteBookName = configuredNotebookName

    temporaryOneNoteExportFolder = r"C:\tempOneNoteExports"
    noteBookName = "IMTOGC Notebook"

    section_path = os.path.join(temporaryOneNoteExportFolder, sectionName)

    try:
        if os.path.exists(section_path):
            shutil.rmtree(section_path)
            time.sleep(2)

        print (f"\tRunning PowerShell script to export OneNote section '{sectionName}' from notebook '{noteBookName}' to '{temporaryOneNoteExportFolder}'")
        
        result = subprocess.run(
            [   "powershell",
                "-ExecutionPolicy","Bypass",
                "-File",".\\_library\\OneNoteGetPages.ps1",
                "-NotebookName", noteBookName,
                "-SectionName", sectionName,
                "-OutputFolder", temporaryOneNoteExportFolder,
            ],
            capture_output=True,
            check=True,
            shell=True  # often needed for .ps1 execution on Windows
        )

        # print(str(result.stdout.decode("utf-8")))
        # print(str(result.stderr.decode("utf-8")))

        if result.returncode != 0:
            print("Error occurred while running the PowerShell script.")
            continue  
        else:
            if len(selectedProjects) == 1:
                if input("PowerShell has imported the OneNote section. Do you want to continue processing the files? (y/n): ").strip().lower() != 'y':
                    print("Exiting without processing files.")
                    continue
    except subprocess.CalledProcessError as e:  
        
        print(f"An error occurred while executing the PowerShell script: {e}")
        print(f"Output: {e.output.decode('utf-8')}")
        print(f"Error: {e.stderr.decode('utf-8')}")
        continue

    #read a OneNoteFile
    oneNoteTempLocation = temporaryOneNoteExportFolder
    oneNoteSectionName = sectionName

    #for markdown files in the localExportPath\sectionName, read the front matter and body, and create a new note in the project folder
    for markDownFileName in os.listdir(os.path.join(oneNoteTempLocation,oneNoteSectionName)):
        if markDownFileName.endswith(".md"):
            fileAndPath = os.path.join(oneNoteTempLocation,oneNoteSectionName,markDownFileName)
            page = ""
            with open(fileAndPath, "r", encoding="utf-8") as f:
                page = f.read()

            frontMatter = myNotes.get_note_frontMatter(page)
            if frontMatter == "":
                print(f"File '{markDownFileName}' does not have front matter. Skipping.")
                continue
            frontMatter = frontMatter.replace("---","\n---")
            frontMatter = frontMatter.replace("date:","\ndate:")
            frontMatter = frontMatter.replace("author:","\nauthor:")
            frontMatter = frontMatter.replace("keywords:","\nkeywords:")
            frontMatter = frontMatter.replace("private:","\nprivate:")
            frontMatter = frontMatter.replace("shareWithStakeholders:","\nshareWithStakeholders:")



            body = page.replace(frontMatter,"")
            title = myNotes.get_stringValue_from_frontMatter("title",frontMatter)
            if title =="":
                title = markDownFileName.split("\\")[-1].replace(".md","") 
            id = myNotes.get_stringValue_from_frontMatter("id",frontMatter)
            noteType = myNotes.get_stringValue_from_frontMatter("type",frontMatter)
            keyWords = myNotes.get_stringValue_from_frontMatter("keywords",frontMatter)
            modified = myNotes.get_stringValue_from_frontMatter("modified",frontMatter)[:10]
            date = myNotes.get_stringValue_from_frontMatter("date",frontMatter)
            date = modified if date =="" else date 
            author = myNotes.get_stringValue_from_frontMatter("author",frontMatter).lower()
            private = myNotes.get_stringValue_from_frontMatter("private",frontMatter).lower()
            shareWithStakeholders = myNotes.get_stringValue_from_frontMatter("shareWithStakeholders",frontMatter).lower()

            if "{" in id:
                id=id.split("{")[-1].replace("}","")
    

            # print(title)
            # print(id)
            # print(id[-5:])
            # print(date)
            # print(modified)
            # print(author)
            # print(noteType)
            # print()
            # print(body[:200])


            import shutil
            pkvProjectName =selectedProject
            projectPath = os.path.join(myPreferences.root_projects(),pkvProjectName)
            projectAttachments = os.path.join(projectPath,"_Attachments")

            #copy the fileAnadPath to the projectAttachments folder
            source=fileAndPath.replace(".md",".pdf")
            destinationFileName = ""
            if os.path.exists(source):
                destinationFileName = markDownFileName.replace(".md",f"_OneNote_{id[-8:]}.pdf")
                if os.path.exists(projectAttachments) == False:
                    os.makedirs(projectAttachments
                                )
                destination=os.path.join(projectAttachments,destinationFileName)
                shutil.copy2(source, destination)
            else:
                print (f"\t'{source}' does not exist")
                
            newNote = f"""---
    title: {title}
    id: {id}
    type: {"project-event" if noteType =="" else noteType}
    created: {date} 
    modified: {modified}
    start date: {date}
    end date: {date}  
    retention: Long
    tags:  
    keywords: {keyWords} 
    project: {pkvProjectName}
    author: {author if author != "" else "OneNote"}
    private: No
    ---

    # {title}

        """

            if destinationFileName != "":
                newNote += f"""
    [OneNote Page PDF](<./_Attachments/{destinationFileName}>)

    {body}

        """
            else:
                newNote += f"""

    {body}

        """

            newNoteFileNameAndPath = os.path.join(projectPath,f"OneNote_{date}_{title}.md")
            myNotes.write_Note_to_path(newNoteFileNameAndPath,newNote)



