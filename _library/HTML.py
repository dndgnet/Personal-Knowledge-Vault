
import re 
import os
import webbrowser

def fn_htmlDocumentStartingString (DocumentTitle = ""):
    """
    Returns the doc type and header of a new HTML page.

    Includes basic Bootstrap and Mermaid references

    """
    returnString = f"""
<!DOCTYPE html>
<html>

<head>
    <title>{DocumentTitle}</title>
"""

    returnString = returnString + """    
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-MrcW6ZMFYlzcLA8Nl+NtUVF0sA7MsXsP1UyJoMp4YLEuNSfAP+JcXn/tWtIaxVXM" crossorigin="anonymous"></script>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({ startOnLoad: true });
    </script>
</head>
"""
    return returnString

def convertMarkDownStringToHTML(markdownText: str, DocumentTitle: str) -> str:
    """
    Converts Markdown text to HTML.

    Args:
        markdownText (str): The Markdown text to convert.

    Returns:
        str: The converted HTML text.
    """

    html = fn_htmlDocumentStartingString(DocumentTitle)
    inMermaidBlock = False
    inCodeBlock = False

    for line in markdownText.splitlines():
        line = line.strip()
        if line.startswith("# "):
            html += f"<h1>{line[2:]}</h1>\n"
        elif line.startswith("## "):
            html += f"<h2>{line[3:]}</h2>\n"
        elif line.startswith("### "):
            html += f"<h3>{line[4:]}</h3>\n"
        elif line.startswith("- "):
            html += f"<li>{line[2:]}</li>\n"
        elif line.startswith("```mermaid"):
            html += """<pre class="mermaid">\n"""
            inMermaidBlock = True
        elif line == "```":
            if inCodeBlock:
                html += "</code>\n"
                inCodeBlock = False
            elif inMermaidBlock:
                html += "</pre>\n"
                inMermaidBlock = False
        else:
            if inCodeBlock:
                html += f"{line}\n"
            elif inMermaidBlock:
                html += f"{line}\n"
            else:
                # Convert Markdown to HTML paragraph
                if line:
                    # Escape HTML special characters
                    line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                    # Convert Markdown links
                    line = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', line)
                    # Convert Markdown bold and italic
                    line = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', line)
                    line = re.sub(r'\*(.*?)\*', r'<em>\1</em>', line)

                    # replace the task todo items with checkboxes
                    line = line.replace("[ ]", '<input type="checkbox" disabled> ')
                    line = line.replace("[x]", '<input type="checkbox" checked disabled> ')
                    

                html += f"<p>{line}</p>\n"

    #close out the html
    html += """</body>
</html>"""

    return html

def convertMarkDownFileToHTML (sourceFilePath: str) -> str:
    """
    Converts a Markdown file to HTML.

    Args:
        sourceFilePath (str): The path to the Markdown file.

    Returns:
        str: The converted HTML text.
    """

    targetFilePath = sourceFilePath.replace(".md", ".html")

    if not os.path.exists(sourceFilePath):
        raise FileNotFoundError(f"The file {sourceFilePath} does not exist.")

    with open(sourceFilePath, "r", encoding="utf-8") as input_file:
        markdownText = input_file.read()

    # Extract the document title from the first line of the Markdown file
    DocumentTitle = sourceFilePath.split(os.sep)[-1].replace(".md", "").replace("_", " ").title()
    
    html = convertMarkDownStringToHTML(markdownText, DocumentTitle)
    
    with open(targetFilePath, "w", encoding="utf-8", errors="xmlcharrefreplace") as output_file:
        output_file.write(html)

    return targetFilePath

def openMarkDownFileInBrowser(sourceFilePath: str):
    """
    Converts a Markdown file to HTML and opens it in the default web browser.

    Args:
        sourceFilePath (str): The path to the Markdown file.
    """
    targetFilePath = convertMarkDownFileToHTML(sourceFilePath)
    
    if os.path.exists(targetFilePath):
        # Open the HTML file in the default browser
        webbrowser.open(f"file://{targetFilePath}")
    else:
        print(f"Failed to create HTML file: {targetFilePath}")

def openHTMLFileInBrowser(filePath: str):
    """
    Opens an HTML file in the default web browser.

    Args:
        filePath (str): The path to the HTML file.
    """
    if os.path.exists(filePath):
        # Open the HTML file in the default browser
        webbrowser.open(f"file://{filePath}")
    else:
        print(f"File not found: {filePath}")