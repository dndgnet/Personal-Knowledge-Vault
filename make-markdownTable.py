#!/usr/bin/env python3
from _library import Preferences as myPreferences, Tools as myTools, Terminal as myTerminal, Notes as myNotes
import os 

csvPath = "table.csv"
markdownPath = "table.md"
if not os.path.exists(csvPath):
    print(f"{myTerminal.ERROR}CSV file not found:{myTerminal.RESET} {csvPath}")
    exit(1)

markdownTable = ""

# read csvPath into a dictionary 
tableData = {}
with open(csvPath, 'r', encoding='utf-8') as f:
    headers = f.readline().strip().split(',')
    for header in headers:
        tableData[header] = []
    for line in f:
        values = line.strip().split(',')
        for i, value in enumerate(values):
            tableData[headers[i]].append(value) 

# build table header 
markdownTable += "| " + " | ".join(headers) + " |\n"
markdownTable += "| " + " | ".join(["---"] * len(headers)) + "|\n"  

# build table rows
numRows = len(tableData[headers[0]])  # Assuming all columns have the same number of rows
for i in range(numRows):
    rowValues = [tableData[header][i] for header in headers]
    markdownTable += "| " + " | ".join(rowValues) + " |\n"  

# save markdownTable to markdownPath
with open(markdownPath, 'w', encoding='utf-8') as f:    
    f.write(markdownTable)  
print(f"{myTerminal.SUCCESS}Markdown table created:{myTerminal.RESET} {markdownPath}")

print("")

print(markdownTable)