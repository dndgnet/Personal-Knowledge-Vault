#!/usr/bin/env python3

from _library import Terminal  as myTerminal

input_string = input(f"{myTerminal.BLUE}Enter comma-separated words for the table header:{myTerminal.RESET} ")
if not input_string:
    input_string = "Status, Name, Description, Date"
    
output_string = ""
header = "|"
separator = "|"
empty_row = "|"
number_of_blank_rows = 3

for word in input_string.split(","):
    word = word.strip()
    header += f" {word} |"
    separator += " --- |"
    empty_row += "   |"

output_string += header + "\n" + separator + "\n" 
for _ in range(number_of_blank_rows):
    output_string += empty_row + "\n"
    
print(output_string)