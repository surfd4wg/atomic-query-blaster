#!/usr/bin/python3
"""
# AUTHOR: Craig Ellrod, Cloud Security Architect
# This python3 script does the following.
# First provide your JupiterOne Account Id and User Level API Token
# It then reads a CSV file one line at a time.
# Each line of the CSV contains a J1QL Query, which can be copied and pasted from the ASKj1 list of prebuilt questions.
# The query is run against JupiterOne using the JupiterOneClient API.
# The results are returned as a counter variable c
# If the results are 0, it is not written to the output CSV file, iow: The output CSV file will contain
# only queries that will return results, cvar > 0
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
    input_filename='j1queries-Sheet1.csv'
    output_filename='j1queries-with-Counts.csv'
    file = open(output_filename, "w+")
    file_exists = exists(input_filename)
    print("file exists: ", file_exists)
    path_to_file = input_filename
    path = Path(path_to_file)
    if path.is_file():
        print(f'The file {path_to_file} exists')
    else:
        print(f'The file {path_to_file} does not exist')
        exit

    # Read through the csv file, process each query one at a time.
    with open(input_filename, newline='') as csvfile:
        queryreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in queryreader:
            QUERY=', '.join(row)
            QUERYcount=QUERY + " return count(e) as c"
            """
            # Uncomment this section of code if you want to debug the Query string being read from the file
            """
            #print("Row: ", row)
            #print("Row2: ", ', '.join(row))
            #print("QUERY: ", '"{}"'.format(QUERY))
            #print("QUERYcount: ", '"{}"'.format(QUERYcount))
            query_result = j1.query_v1(QUERYcount)
            #print("query_result: ", query_result)
            #print("query_result type: ", type(query_result))

            cvar=query_result['data'][0]['c']
            #print("cvar: ", cvar)
            #print("cvar type: ", type(cvar))

            #for key, value in query_result.items():
            #    print("key, value: ", key, value)
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
            #output_json_filename = "_j1queries_Output_" + QUERY + ".json"
            #print("filename: ", output_json_filename)

            #file = open(output_json_filename, "w+", newline='\n')
            #fileout = file.write(json_formatted_str)

            """
            # Uncomment this section of code if you want to print the QUERY string to a different csv file
            # that contains only queries that return results, ex: return count >0
            # """
            file = open(output_filename, "a")
            QUERYnewline=QUERY + "\n"
            if cvar > 0:
                queryout = file.write(QUERYnewline)

            

if __name__ == "__main__":
    main()