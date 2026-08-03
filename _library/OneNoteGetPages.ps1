

param(
    [string]$NotebookName = "notebook nmae",
    [string]$SectionName = "section name taken from the notebook",
    [string]$OutputFolder = "C:\Temp\OneNoteExport"
)

#Using the COM api for OneNote extract notes as markdown and PDf and move them into your vault.
# Only available on Windows and requires OneNote to be installed, running as a user with appropriate permissions, with the notebook OPEN.
# Also requires PowerShell 5.1 to work with the COM api.  
# Will NOT work with the core version of PowerShell (7.x) as the COM api is not supported in that version.
#

$PSVersionTable

$ErrorActionPreference = "Stop"

$oneNote = New-Object -ComObject OneNote.Application

if (!(Test-Path $OutputFolder)) {
    New-Item -ItemType Directory -Path $OutputFolder -Force | Out-Null
}

Write-Host "Loading OneNote hierarchy..."

$hierarchyXml = ""
$oneNote.GetHierarchy("", 4, [ref]$hierarchyXml)

[xml]$xml = $hierarchyXml

$ns = New-Object System.Xml.XmlNamespaceManager($xml.NameTable)
$ns.AddNamespace("one", "http://schemas.microsoft.com/office/onenote/2013/onenote")

# Locate notebook
$notebook = $xml.SelectSingleNode("//one:Notebook[@name='$NotebookName']", $ns)

if (-not $notebook) {
    throw "Notebook '$NotebookName' not found."
}

# Locate section
$section = $notebook.SelectSingleNode(".//one:Section[@name='$SectionName']", $ns)

if (-not $section) {
    throw "Section '$SectionName' not found."
}

Write-Host "Found section: $SectionName"

$sectionXml = ""
$oneNote.GetHierarchy($section.ID, 4, [ref]$sectionXml)

[xml]$sx = $sectionXml

$sectionFolder = Join-Path $OutputFolder $SectionName
New-Item -ItemType Directory -Force -Path $sectionFolder | Out-Null

$pages = $sx.SelectNodes("//one:Page", $ns)

Write-Host ""
Write-Host "Pages found: $($pages.Count)"
Write-Host ""

foreach ($page in $pages) {


    try {
        $pageName = $page.name
        # Create safe filename
        $safeName = $pageName
        [System.IO.Path]::GetInvalidFileNameChars() | ForEach-Object {
            $safeName = $safeName.Replace($_, "_")
        }
        
        #PKV Statement is title: $pagename \nid: Page.Id \nlast modified: $page.lastModifiedTime \ncreated: $page.dateTimeCreated 
        $pkvStatement = "title: $pageName`nid: $($page.ID)`nmodified: $($page.lastModifiedTime)`ncreated: $($page.dateTimeCreated)"
        

        #Print page id
        Write-Host "Page ID: $($page.ID); Page Title: $pageName"

        $pdfFile = Join-Path $sectionFolder "$safeName.pdf"

        try {
            $oneNote.Publish(
                $page.ID,
                $pdfFile,
                3  # PDF
            )
    
            Write-Host "- Saved PDF: $pdfFile"
        }
        catch {
            Write-Warning "Failed to export PDF for page: $pageName"
            Write-Warning "Export file name = $pdfFile"
            Write-Warning $_.Exception.Message
            Write-Warning $_.ScriptStackTrace

            try {
                $wordFile = Join-Path $sectionFolder "$safeName.docx"
                $oneNote.Publish(
                $page.ID,
                $wordFile,
                5  # Word
            )
    
            Write-Host "- Saved Word: $wordFile"
            }
            catch {
                Write-Warning "Failed to export word for page: $pageName"
                Write-Warning $_.Exception.Message
                Write-Warning $_.ScriptStackTrace

                
                try {
                    $mhtmlFile = Join-Path $sectionFolder "$safeName.mht"
                    
                    $oneNote.Publish(
                        $page.ID,
                        $mhtmlFile,
                        6  # MHTML
                    )
            
                    Write-Host "- Saved MHTML: $mhtmlFile"
                    }
                catch {
                        Write-Warning "Failed to export mhtml for page: $pageName"
                        Write-Warning $_.Exception.Message
                        Write-Warning $_.ScriptStackTrace

                        
                    }
            }

        }



        Write-Host "Exporting: $pageName"

        # Retrieve the page XML
        $pageXml = ""
        $oneNote.GetPageContent(
            $page.ID,
            [ref]$pageXml
        )

        # Save raw XML
        $xmlFile = Join-Path $sectionFolder "$safeName.xml"
        $pageXml | Set-Content $xmlFile -Encoding UTF8
        Write-Host "Saved XML: $xmlFile"
 
        # Load XML document
        [xml]$pageDoc = $pageXml

        $ns = New-Object System.Xml.XmlNamespaceManager($pageDoc.NameTable)
        $ns.AddNamespace(
            "one",
            "http://schemas.microsoft.com/office/onenote/2013/onenote"
        )

        $titleNode = $pageDoc.SelectSingleNode(
            "//one:Title//one:T",
            $ns
        )

        # $title = ""
        # if ($titleNode) {
        #     $title = $titleNode.InnerText
        # }
        # else {
        #     $title = $pageName
        # }

        $textNodes = $pageDoc.SelectNodes(
            "//one:T",
            $ns
        )

        $markdown = New-Object System.Collections.Generic.List[string]
        foreach ($node in $textNodes) {

            $text = [System.Net.WebUtility]::HtmlDecode(
                $node.InnerText
            ).Trim()

            if ($text.Trim()) {
                $markdown.Add($text)
                $markdown.Add("")
            }
        }

        #if "pkvfrontmatter" exists in the markdown, replace it with the pkvStatement if it does not exist, add the pkvStatement to the top of the markdown
        if (-not $markdown.Contains('pkvfrontmatter')) {
    $markdown = @"
---
$pkvStatement
---

$markdown
"@
}
        else {
            # Replace literal token with the statement
            $markdown = $markdown.Replace('pkvfrontmatter', $pkvStatement)
        }

        $mdFile = Join-Path $sectionFolder "$safeName.md"

        #$markdown | Set-Content $mdFile -Encoding UTF8

        $utf8Text = [System.Text.Encoding]::UTF8.GetString(
            [System.Text.Encoding]::UTF8.GetBytes($markdown)
        )

        $utf8Text | Set-Content $mdFile -Encoding UTF8


        Write-Host "Saved Markdown: $mdFile"
        Write-Host ""
        Write-Host "=========="



    }
    catch {
        Write-Warning "Failed: $pageName"
        Write-Warning $_.Exception.Message
        Write-Warning $_.ScriptStackTrace
    }
    



}

Write-Host ""
Write-Host "Completed."
Write-Host "Export location: $sectionFolder"