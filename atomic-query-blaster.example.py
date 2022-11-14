#!/usr/bin/python3
"""
# AUTHOR: Craig Ellrod, Cloud Security Architect
# This python3 script does the following.
# First provide your JupiterOne Account Id and User Level API Token
# It then reads a CSV file, you need to provide the filename, one line at a time.
# Each line of the CSV contains a J1QL Query, which can be copied and pasted from the ASKj1 list of prebuilt questions.
# The query is run against JupiterOne using the JupiterOneClient API.
# The results are returned in JSON format and written to an output file, with the Query in the filename, and a .json extension.
# If you decide to print the JSON output to the screen, you can use the pretty print and colored output routines.
# Do not use the colored output to a file, it won't be readable.
"""
import json
import csv
from pathlib import Path
from os.path import exists
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import TerminalFormatter
from jupiterone import JupiterOneClient

def main():
    # Provide your JupiterOne creds.
    j1 = JupiterOneClient(
        account='///redacted///',
        token='///redacted///'
    )

    # If the csv file doesn't exist, bounce. Might have to include the full path.
    file_exists = exists('j1queries-Sheet1.csv')
    print("file exists: ", file_exists)
    path_to_file = 'j1queries-Sheet1.csv'
    path = Path(path_to_file)
    if path.is_file():
        print(f'The file {path_to_file} exists')
    else:
        print(f'The file {path_to_file} does not exist')
        exit

    # Read through the csv file, process each query one at a time.
    with open('j1queries-Sheet1.csv', newline='') as csvfile:
        queryreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in queryreader:
            QUERY=', '.join(row)
            """
            # Uncomment this section of code if you want to debug the Query string being read from the file
            """
            #print("Row: ", row)
            #print("Row2: ", ', '.join(row))
            print("QUERY: ", '"{}"'.format(QUERY))

            query_result = j1.query_v1(QUERY)
            json_formatted_str = json.dumps(query_result, indent=2)

            """
            # Uncomment this section of code if you want to pretty print to the terminal for debugging
            """
            #print("j1: ", j1)
            #print("j1 type: ", type(j1))
            #print (json_formatted_str) 
            #colorful_json_formatted_str=(highlight(json_formatted_str, JsonLexer(), TerminalFormatter()))
            #print(highlight(json_formatted_str, JsonLexer(), TerminalFormatter()))

            """
            # Uncomment this section of code if you want to print the JSON output to a file
            """
            filename = "_j1queries_Output_" + QUERY + ".json"
            print("filename: ", filename)

            file = open(filename, "w+")
            fileout = file.write(json_formatted_str)

if __name__ == "__main__":
    main()