#!/usr/bin/env python3

"""
Valid tags are active, done, crit, and milestone

"""

from _library import Preferences as myPreferences, Tools as myTools, Terminal as myTerminal, Notes as myNotes
import os 

csvPath = "tablegantt.csv"
markdownPath = "gantt.md"
if not os.path.exists(csvPath):
    print(f"{myTerminal.ERROR}CSV file not found:{myTerminal.RESET} {csvPath}")
    exit(1)

ganttMarkdown = """
gantt
    dateFormat  YYYY-MM-DD
    title       Adding GANTT diagram functionality to mermaid
    excludes    weekends
    %% (`excludes` accepts specific dates in YYYY-MM-DD format, days of the week ("sunday") or "weekends", but not the word "weekdays".)
"""

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

print (tableData)

for key, values in tableData.items():
    myTerminal.printWithoutLineWrap(" ",f"{key}:")
    myTerminal.printWithoutLineWrap("    ",f"{values}")
    print("")