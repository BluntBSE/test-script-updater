""" for (test in data_frame):
        if(searchAsana(test) == true):
                updateAsana(test)
        if(searchAsana(test) == false:
                addToListOfNewTests(test)
        else:
            addtoListForHumanVerification(test)
            
        ##Afterwards....
        allCNumbersInAsana = getTestByFunctionalArea(area)
        for (CNumber in allCNumbersinAsana):
            if(not in data_frame['ID']):
                addtoListofMissingtestCases(CNumber)
"""


##MBTA Workspace GID: 15492006741476
##Test bed project GID : 1203186680032258

##Remember to add "Automatically Generated" tag GID = '1203191978331220'
##Remember to add "Automatically Updated" tag GID = ''
##Asana records consist of Test: [Area] and optionally, 
##Create a new CSV containing all test cases received for which we received a C number, but there are no C Numbers in our Asana records. These are new test cases
##Create a CSV containing all test cases where we had an Asana record, but did not receive a C number. These are potentially missing test cases.


##Reference Review Required Task GID = 1202894410931244
##Reference Approved Task GID = 1202632050244277
##Custom Field 'ID Number' GID = 515737795293097

#Step 1 - Check to see if a task exists in Asana with the defined C number.

import sys
import requests
import os
import pandas
import numpy
import asana
import re ##Regex -- used for matching name string

##Put your token in a 'credentials.py' in the same directory as this script
sys.path.append(os.path.relpath('.\credentials.py'))
from credentials import token

##SIMPLE ASANA AUTHENTICATION##
##Headers to log in as Robert

##Set token equal to a Personal Access Token

""" token = '1/1200584565016332:edc42f4e606085fcdbea52f76ad4e17a' """
client = asana.Client.access_token(token)
workspace = '15492006741476'

mytask = client.tasks.get_task('1203191978331226')
taskname = mytask
print(taskname) 


##SET UP FILE STRUCTUR
##GET FILE IN INPUT FOLDER. DO NOT ALLOW MORE THAN ONE FILE IN INPUT FOLDER.
contents = os.listdir('input')
if(len(contents)>1):
    print('!ERROR! More than one file in input')
else:
    filename = os.listdir('input')[0]
    filepath = os.path.dirname(os.path.abspath(__file__)) + '/input/'+ filename
    print(filepath)

input_xlsx=pandas.ExcelFile(filepath)
data_frame = pandas.read_excel(input_xlsx, "Cubic submittal",)

##Create a data frame that only contains test cases marked "Ready for Review" or "Ready"



 


##ASANA FUNCTIONS##
#1. Search Asana for a task with a name containing the C Number in question
#2. If multiples are found, try to narrow down results by finding a task with an ID Number matching the number.
#3. If one we get down to one result here, do the following:
#   -Update 'Test Review Status' to 'MBTA Ready to Review'
#   -Update Tags to include 'Automatically Updated'
#   -


##Just in case someone rearranged custom value order on the task, this makes sure we acess ID Number properly.
def getIndexofIDNumberField(arr):
    for ind, el in enumerate(arr):
        if el['gid'] == '515737795293097':
           return ind
    print('Not found')
    return None


##If for whatever reason there are multiple tasks that start with the C Number in question, try to narrow in on the one with a defined ID Number field.
def searchFieldForCNumber(arr, cnum):
    output = []
    for el in arr:
        id_num_index = (getIndexofIDNumberField(el['custom_fields']))
        if id_num_index != None:
            if ( (el['custom_fields'][id_num_index]['display_value']) == cnum):
                output.append(el)
    return output

##Search name for CNumber. If there are multiples, call SearchFieldforCNumber for further filtering.
def searchNameForCNumber(cnum):
    output = []
    result = client.tasks.search_tasks_for_workspace(workspace, {'text': cnum, 'opt_fields':{'name', 'custom_fields'}})
    for el in result:
        output.append(el)
    if(len(output) < 1):
        print('!!ERROR!! No results found for CNumber:' + str(cnum) + ' If this is the case, it is probably a new test case.')
        return None
    if len(output) < 2:
        return output
    else:
        filtered = searchFieldForCNumber(output, cnum)
        if (len(filtered) < 2 ):
            return filtered
        else:
            print('!!ERROR!! Cannot resolve single test case. Add to list for human verification')





##Search Asana for each ID contained in your data frame and start handling it

def UpdateTestScripts(data_frame):
    for el in data_frame['ID']:
        task = searchNameForCNumber(el)
        if task != None:
            print('Confirmed Asana Contains CNumber for ' + task[0]['name'])


