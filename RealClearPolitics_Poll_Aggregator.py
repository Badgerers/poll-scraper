from fuzzywuzzy import fuzz
from urllib.request import urlopen
import re

#This program will take HTML info from
#a RealClearPolitics webpage and make
#predictions as to the outcome of elections

#TO DO:
#Implement matches from specific to general, starting with exact matches, to checking for matches without common words (i.e. University),
#checking for abbrevations, to levenshtein distance last

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

#Creates the poll linkedlist
def createLinkedList(listName, init) -> PollTypeLinkedList:
    realClearWebpage = GetWebpageInfo(url)
    #Creates a list of all Strings with html, pdf, or com, and </a> on the ends
    #Change this to change everything that is gathered
    reducedHTML = re.findall("org.*</a>|html.*</a>|pdf.*</a>|com.*</a>|edu.*</a>|UMass Amherst", realClearWebpage.html, re.IGNORECASE)
    #Remove first object in the list
    del reducedHTML[0]
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
        #Assign node to the last node of the linked list
        new_node = PollTypeNode(reducedHTML[3 * x], reducedHTML[3 * x + 1], reducedHTML[3 * x + 2])
        if listName.head is None:
            listName.head = new_node
        else:
            last = listName.head
            while (last.next):
                last = last.next
            last.next = new_node
        #Print a list of poll races
        repeatedPollType = False
        if init == 1:
            for y in range(0, x):
                if (reducedHTML[3 * x] == reducedHTML[3 * y]):
                    repeatedPollType = True
            if (not repeatedPollType):
                print(reducedHTML[3 * x])
    return listName

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

#Helper method that weighs poll data, currently incomplete
#Takes a linked list object latestPollsWeighted
def weighPollData(latestPollsWeighted) -> PollTypeLinkedList:
    realClearWebpage = GetWebpageInfo(url)
    #Set up which races are partisan and to be adjusted
    #based on the HTML of RealClearPolitics
    democraticMarkingHTML = re.findall("class=\"dem\".*</span>", realClearWebpage.html, re.IGNORECASE)
    republicanMarkingHTML = re.findall("class=\"rep\".*</span>", realClearWebpage.html, re.IGNORECASE)
    #Removes extra HTML formatting and leaves just the name
    for x in range(0, len(democraticMarkingHTML)):
        democraticMarkingHTML[x] = democraticMarkingHTML[x].replace("class=\"dem\">", "")
        democraticMarkingHTML[x] = democraticMarkingHTML[x].replace("</span>", "")
        tempMarking = []
        tempMarking = democraticMarkingHTML[x].split(" ")
        democraticMarkingHTML[x] = tempMarking[0]
    for x in range(0, len(republicanMarkingHTML)):
        republicanMarkingHTML[x] = republicanMarkingHTML[x].replace("class=\"rep\">", "")
        republicanMarkingHTML[x] = republicanMarkingHTML[x].replace("</span>", "")
        tempMarking = []
        tempMarking = republicanMarkingHTML[x].split(" ")
        republicanMarkingHTML[x] = tempMarking[0]
    #Remove duplicates from lists
    democraticMarkingHTML = set(democraticMarkingHTML)
    democraticMarkingHTML = list(democraticMarkingHTML)
    republicanMarkingHTML = set(republicanMarkingHTML)
    republicanMarkingHTML = list(republicanMarkingHTML)
    print(democraticMarkingHTML)
    print(republicanMarkingHTML)
    #Iterate through linked list and match whether
    #the whole of one string in each set is
    #a substring in the other set for both
    #sets
    currentNode = latestPollsWeighted.head
    while (currentNode.next):
        print(currentNode.pollType)
        firmNames = biasFirmsToData.keys()
        alreadyAdjusted = False
        #Format currentNode.pollingFirm
        currentNode.pollingFirm = currentNode.pollingFirm.split(">")
        currentNode.pollingFirm = currentNode.pollingFirm[1]
        print(currentNode.pollingFirm)
        for name in firmNames:
            if name in currentNode.pollingFirm:
                democratSkew = biasFirmsToData[name].split("+")
                print("Bias of Poll:")
                print(democratSkew)
                print("Is the Name Matching?")
                print(name)
                print(" ")
                #For the case of No Data in bias, democratSkew[1] does not exist and causes an error
                #Also no need to adjust if there is no data on the firm
                if democratSkew[0] != "NO DATA":
                    democratSkew[1] = float(democratSkew[1])
                    if democratSkew[0] == "R":
                        democratSkew[1] *= -1
                    democratSkew[1] /= 2
                    democratSkew[1] = round(democratSkew[1], 1)
                    pollDataTemp = []
                    dataTemp = []
                    dataTemp1 = []
                    #Temporarily holds the split string of data
                    pollDataTemp = currentNode.pollData.split(", ")
                    #Holds the first data point
                    dataTemp = pollDataTemp[0].split(" ")
                    #Holds the second data point
                    dataTemp1 = pollDataTemp[1].split(" ")
                    #Looks if the name of the data point is democratic or republican and adjusts them both
                    for x in range(0, len(democraticMarkingHTML)):
                        if dataTemp[0] == democraticMarkingHTML[x]:
                            dataTemp[1] = float(dataTemp[1])
                            dataTemp1[1] = float(dataTemp1[1])
                            dataTemp[1] -= democratSkew[1]
                            dataTemp1[1] += democratSkew[1]
                            alreadyAdjusted = True
                            currentNode.data = dataTemp[0] + " " + str(dataTemp[1]) + ", " + dataTemp1[0] + " " + str(dataTemp1[1]) + "ADJUSTED"
                            print("adjusted")
                            print(dataTemp)
                            print(dataTemp1)
                            break
                        elif dataTemp1[0] == democraticMarkingHTML[x]:
                            dataTemp[1] = float(dataTemp[1])
                            dataTemp1[1] = float(dataTemp1[1])
                            dataTemp[1] += democratSkew[1]
                            dataTemp1[1] -= democratSkew[1]
                            alreadyAdjusted = True
                            currentNode.data = dataTemp[0] + " " + str(dataTemp[1]) + ", " + dataTemp1[0] + " " + str(dataTemp1[1]) + "ADJUSTED"
                            print("adjusted")
                            print(dataTemp)
                            print(dataTemp1)
                            break
                        #Here add more if statements based on checking if the pollType is something like congressional job approval or
                        #President Biden job approval and skew based on ruling party
                    if alreadyAdjusted:
                        break
                    for x in range(0, len(republicanMarkingHTML)):
                        if dataTemp[0] == republicanMarkingHTML[x]:
                            dataTemp[1] = float(dataTemp[1])
                            dataTemp1[1] = float(dataTemp1[1])
                            dataTemp[1] += democratSkew[1]
                            dataTemp1[1] -= democratSkew[1]
                            alreadyAdjusted = True
                            currentNode.data = dataTemp[0] + " " + str(dataTemp[1]) + ", " + dataTemp1[0] + " " + str(dataTemp1[1]) + "ADJUSTED"
                            print("adjusted")
                            print(dataTemp)
                            print(dataTemp1)
                            break
                        elif dataTemp1[0] == republicanMarkingHTML[x]:
                            dataTemp[1] = float(dataTemp[1])
                            dataTemp1[1] = float(dataTemp1[1])
                            dataTemp[1] -= democratSkew[1]
                            dataTemp1[1] += democratSkew[1]
                            alreadyAdjusted = True
                            currentNode.data = dataTemp[0] + " " + str(dataTemp[1]) + ", " + dataTemp1[0] + " " + str(dataTemp1[1]) + "ADJUSTED"
                            print("adjusted")
                            print(dataTemp)
                            print(dataTemp1)
                            break
                    if alreadyAdjusted:
                       break
        currentNode = currentNode.next
    return latestPollsWeighted
   
#MAIN CODE

#Create Linked List in which all poll data is stored
latestPolls = PollTypeLinkedList()
latestPolls = createLinkedList(latestPolls, 1)
#Iterate through the list to assign values to linked list
#and remove HTML formatting
#Copy and paste print(reducedHTML[x]) into the end of an if statement to check the results of web scraping

#Must be done before for loop so it does not repeat

print("Here are a list of poll races to choose from:")

#Creating a map of String to String to store polling firm bias according to fiveThirtyEight
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
#print(biasFirmsToData)

#USER INTERACTION AND COMMANDS
quit = True
while (quit):
    #Ask for poll type that is to be analyzed
    print("Input Poll Type from Above Options:")
    pollTypeInput = input()

    #Ask for how to analyze poll type
    #Function that weighs the poll data based on 538
    #Currently Does Nothing

    print("[1]Weighted or [2]Not Weighted")
    weightedOrNotWeighted = input()
    weighted = 0
    if (weightedOrNotWeighted == "1"):
        latestPollsWeighted = PollTypeLinkedList()
        latestPollsWeighted = createLinkedList(latestPollsWeighted, 1)
        latestPollsWeighted = weighPollData(latestPollsWeighted)
        weighted = 1
    print("[1]Print Average [2]Print Results")
    averageOrResults = input()
    #Work on error caused by returnPollAverage function when the length of linked list is 1
    if (averageOrResults == "1"):
        if weighted == 0:
            returnPollAverage(pollTypeInput, latestPolls)
        else:
            returnPollAverage(pollTypeInput, latestPollsWeighted)
    if (averageOrResults == "2"):
        if weighted == 0:
            returnPollResults(pollTypeInput, latestPolls)
        else:
            returnPollResults(pollTypeInput, latestPollsWeighted)

    #Prompts to quit or continue the program
    print("Type (Q)uit or (C)ontinue?")
    quitOrContinue = input()
    quitOrContinue = quitOrContinue.capitalize()
    if (quitOrContinue.startswith("Q")):
        quit = False


