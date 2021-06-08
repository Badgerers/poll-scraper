from fuzzywuzzy import fuzz
from urllib.request import urlopen
import re

#This program will take HTML info from
#a RealClearPolitics webpage and make
#predictions as to the outcome of elections

#Works as of 6/8/2021

#TO DO:
#Evaluate the bias of polling firms
#   In order to implement levenshtein distance, removing certain common words like "University" may be useful in order
#   to prevent false matches, either that or a different implementation will have to be done.
#Organizes more methods into classes

url = "https://www.realclearpolitics.com/epolls/latest_polls/#";

urlPollingFirms = "https://projects.fivethirtyeight.com/pollster-ratings/"

#CLASSES
#Gets raw HTML of the webpage and converts to string format
class GetWebpageInfo:
    def __init__(self, url):
        self.page = urlopen(url)
        self.html_bytes = self.page.read()
        self.html = self.html_bytes.decode("utf-8");

#Defines linked list and nodes
class PollTypeNode:
    def __init__(self, pollType, pollingFirm, pollData):
        self.pollType = pollType
        self.pollingFirm = pollingFirm
        self.pollData = pollData
        self.next = None

class PollTypeLinkedList:
    def __init__(self):
        self.head = None

class PollAggregate:
    def __init__(self, pollSection, specificPollInput):
        self.pollSection = pollSection
        self.specificPollInput = specificPollInput
    def printToConsole(self):
        print(self.pollSection)
        print(self.specificPollInput)

#FUNCTIONS
#Define a function that iterates through linked list and prints latest poll results
def returnPollResults(pollTypeInput, pollLinkedList):
    currentNode = pollLinkedList.head
    while (currentNode.next):
        if (currentNode.pollType == pollTypeInput):
            pollType = currentNode.pollingFirm.split('>')
            print(pollType[len(pollType) - 1])
            print(currentNode.pollData)
        currentNode = currentNode.next
    #Extra because while loop does not process last no
    if (currentNode.pollType == pollTypeInput):
            pollType = currentNode.pollingFirm.split('>')
            print(pollType[len(pollType) - 1])
            print(currentNode.pollData)

#Define a function that iterates through the linked list and aggregates poll
#pollTypeInput is a string that specifies what the poll is measuring
#pollLinkedList is a class object linked list that will be iterated through with the data from the web scraper
def returnPollAverage(pollTypeInput, pollLinkedList):
    firstPollDataDescriptor = ""
    secondPollDataDescriptor = ""
    firstPollDataArray = []
    secondPollDataArray = []
    currentNode = pollLinkedList.head
    while (currentNode.next):
        if (currentNode.pollType == pollTypeInput):
            dataString = currentNode.pollData.split(',')
            firstDataString = dataString[0].split()
            secondDataString = dataString[1].split()
            #Adds data to the array for averages
            firstPollDataArray.append(firstDataString[len(firstDataString) - 1])
            secondPollDataArray.append(secondDataString[len(secondDataString) - 1])
            #Stores the name of the metric (ex: Approve/Disapprove, Names of Candidates)
            firstPollDataDescriptor = ""
            for x in range(0, len(firstDataString) - 1):
                firstPollDataDescriptor += firstDataString[x]
                firstPollDataDescriptor += " "
            secondPollDataDescriptor = ""
            for x in range(0, len(secondDataString) - 1):
                secondPollDataDescriptor += secondDataString[x]
                secondPollDataDescriptor += " "
            firstPollDataDescriptor = firstPollDataDescriptor.strip()
            secondPollDataDescriptor = secondPollDataDescriptor.strip()
        currentNode = currentNode.next
    #Extra because the while loop does not process for last node
    if (currentNode.pollType == pollTypeInput):
            dataString = currentNode.pollData.split(',')
            firstDataString = dataString[0].split()
            secondDataString = dataString[1].split()
            #Adds data to the array for averages
            firstPollDataArray.append(firstDataString[len(firstDataString) - 1])
            secondPollDataArray.append(secondDataString[len(secondDataString) - 1])
            #Stores the name of the metric (ex: Approve/Disapprove, Names of Candidates)
            firstPollDataDescriptor = ""
            for x in range(0, len(firstDataString) - 1):
                firstPollDataDescriptor += firstDataString[x]
                firstPollDataDescriptor += " "
            secondPollDataDescriptor = ""
            for x in range(0, len(secondDataString) - 1):
                secondPollDataDescriptor += secondDataString[x]
                secondPollDataDescriptor += " "
            firstPollDataDescriptor = firstPollDataDescriptor.strip()
            secondPollDataDescriptor = secondPollDataDescriptor.strip()
    print(firstPollDataDescriptor + " " + returnAverageHelper(firstPollDataArray) + ", " + secondPollDataDescriptor + " " + returnAverageHelper(secondPollDataArray))

#Helper method to return average
def returnAverageHelper(dataArray):
    sum = 0
    for x in dataArray:
        sum += int(x)
    return str(round(sum / len(dataArray), 2))


   
#MAIN CODE
#Creates a list of all Strings with html, pdf, or com, and </a> on the ends
realClearWebpage = GetWebpageInfo("https://www.realclearpolitics.com/epolls/latest_polls/#")
#Change this to change everything that is gathered
reducedHTML = re.findall("org.*</a>|html.*</a>|pdf.*</a>|com.*</a>|edu.*</a>|UMass Amherst", realClearWebpage.html, re.IGNORECASE)

#Remove first object in the list
del reducedHTML[0]

#Define Linked List in which all poll data is stored
latestPolls = PollTypeLinkedList()
#Iterate through the list to assign values to linked list
#and remove HTML formatting
#Copy and paste print(reducedHTML[x]) into the end of an if statement to check the results of web scraping

#Must be done before for loop so it does not repeat
print("Here are a list of poll races to choose from:")

for x in range(0, int(len(reducedHTML) / 3)):
    #Deal with formatting and assignment of Poll Type
    reducedHTML[3 * x] = reducedHTML[3 * x].replace("</a>", "")
    reducedHTML[3 * x] = reducedHTML[3 * x].replace("html\">", "")
    #Removes special cases for Georgia Elections
    reducedHTML[3 * x] = re.sub("orgia.*73", "", reducedHTML[3 * x])
    if (reducedHTML[3 * x][0] == "3" or reducedHTML[3 * x][0] == "2"):
        reducedHTML[3 * x] = reducedHTML[3 * x][3:]
    #Removes Unnecessary Spaces
    while (reducedHTML[3 * x][0] == " "):
        reducedHTML[3 * x] = reducedHTML[3 * x][1:]
    #Deal with formatting and assignment of Poll Firms
    reducedHTML[3 * x + 1] = reducedHTML[3 * x + 1].replace("</a>", "")
    reducedHTML[3 * x + 1] = re.sub("org.*</a>|html.*</a>|pdf.*</a>|com.*</a>|edu.*</a>", "", reducedHTML[3 * x + 1])
    #Deal with formatting and assignment of Poll Data
    reducedHTML[3 * x + 2] = reducedHTML[3 * x + 2].replace("</a>", "")
    #Special formatting for Georgia Runoff
    reducedHTML[3 * x + 2] = reducedHTML[3 * x + 2].replace("html\">", "")
    reducedHTML[3 * x + 2] = reducedHTML[3 * x + 2].replace("orgia_senate_special_election_runoff_loeffler_vs_warnock-7318.", "")
    reducedHTML[3 * x + 2] = reducedHTML[3 * x + 2].replace("orgia_senate_runoff_election_perdue_vs_ossoff-7319.", "")
    #Assign value to head of linked list
    new_node = PollTypeNode(reducedHTML[3 * x], reducedHTML[3 * x + 1], reducedHTML[3 * x + 2])
    if latestPolls.head is None:
        latestPolls.head = new_node
    else:
        last = latestPolls.head
        while (last.next):
            last = last.next
        last.next = new_node
    #Print a list of poll races
    repeatedPollType = False
    for y in range(0, x):
        if (reducedHTML[3 * x] == reducedHTML[3 * y]):
            repeatedPollType = True
    if (not repeatedPollType):
        print(reducedHTML[3 * x])

#Creating a map of String to String to store polling firm bias according to fiveThirtyEight
#CURRENTLY NOT WORKING BECAUSE OF WEBPAGE CHANGE!
fiveThirtyEightBias = GetWebpageInfo("https://projects.fivethirtyeight.com/pollster-ratings/")
#Firms Names
reducedHTMLBiasFirms = re.findall("<a href=\"/pollster-ratings.*?<", fiveThirtyEightBias.html)
#Firm Bias Data
reducedHTMLBiasFirmsData = re.findall("meanrevertedbias\">.*?</td>", fiveThirtyEightBias.html)
reducedHTMLBiasFirmsData = reducedHTMLBiasFirmsData[1:]
#Formatting the lists
for x in range(0, len(reducedHTMLBiasFirmsData)):
    reducedHTMLBiasFirms[x] = reducedHTMLBiasFirms[x][27:]
    splitFirmName = reducedHTMLBiasFirms[x].split("\">")
    reducedHTMLBiasFirms[x] = splitFirmName[1][:len(splitFirmName[1]) - 1]
    reducedHTMLBiasFirmsData[x] = reducedHTMLBiasFirmsData[x][73:78]
biasFirmsToData = {}
#Assigning data from the lists into the dictionary
for x in range(0, len(reducedHTMLBiasFirmsData)):
    reducedHTMLBiasFirmsData[x] = reducedHTMLBiasFirmsData[x][0:5]
    if reducedHTMLBiasFirmsData[x].startswith("D") or reducedHTMLBiasFirmsData[x].startswith("R"):
        biasFirmsToData.update({reducedHTMLBiasFirms[x]:reducedHTMLBiasFirmsData[x]})
    else:
        biasFirmsToData.update({reducedHTMLBiasFirms[x]:"NO DATA"})

#USER INTERACTION AND COMMANDS
quit = True
while (quit):
    #Ask for poll type that is to be analyzed
    print("Input Poll Type from Above Options:")
    pollTypeInput = input()

    #Ask for how to analyze poll type
    #Function that weighs the poll data based on 538
    #Currently Does Nothing
    def weighPollData():
        currentNode = latestPolls.head

    print("[1]Weighted or [2]Not Weighted")
    weightedOrNotWeighted = input()
    if (weightedOrNotWeighted == "1"):
        weighPollData()

    print("[1]Print Average [2]Print Results")
    averageOrResults = input()
    if (averageOrResults == "1"):
        returnPollAverage(pollTypeInput, latestPolls)
    if (averageOrResults == "2"):
        returnPollResults(pollTypeInput, latestPolls)

    #Prompts to quit or continue the program
    print("Type (Q)uit or (C)ontinue?")
    quitOrContinue = input()
    quitOrContinue = quitOrContinue.capitalize()
    if (quitOrContinue.startswith("Q")):
        quit = False


