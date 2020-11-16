#MIT License

#Copyright (c) 2020 Bastien Saidi

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.


from __future__ import print_function

#CONFIG PARAM. Are you onsite? (True or False). You can edit this. Must be True if you are at school.
onsite = False #⚠⚠⚠ Do not add any quotes around it, must be a boolean. ⚠⚠⚠

#Timer + Time Difference
import datetime
import dateutil.parser
import time
from time import sleep
from tqdm import tqdm

#Calendar Api
import pickle
import math
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

#Http Api Calls + Get & Parse Upcoming Class' Code.
import requests
import json
from bs4 import BeautifulSoup
import lxml

#Misc, like for example:
import sys #Nessecary for Google Api.
import os #Get terminal's size, creating folder & temp file.

#DO NOT EDIT. Declaring Variable for later use. Needed to make comparaison between ongoing and upcoming classes.
subjectDone = ""
ongoing = "first"



#Read-only access to calendar
# If modifying these scopes, delete the file token.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


#Draws a limit, to the lengh of the Terminal Screen.
def limit():
    rows, columns = os.popen('stty size', 'r').read().split()
    line=""
    for x in range(int(columns)):
       line += "―"
    print(line)

#Parse the HTML previously downloaded, and extracts the code from it.
def parseCode():
    with open('.tmp/index.html') as raw_resuls:
        soup = BeautifulSoup(raw_resuls, 'lxml')
    try:
        return soup.find_all("button", {"id": "save_button"})[0]['record_id']
    except:
        #print("[*] Node Code Right Now")
        return "N/A"

#Registers the ongoing class. (Only works for 15min into the beginning of the class)
def registerClass(classId,time,onsite):
    if not classId.isdigit():
        print("\n\033[91m%s\033[0m" % ("[*] No Code Available")) #Exits if there is no code.
        return                 

    print("\n"+classId,time) #Debug, shows the code and the current time

    if (onsite == True):   #Changes param to suit, whether the user is at home or not.
        obj = {'record_id': classId,'location':'1','topic':'1','t_cs_signed':'-1','time':time} 
    else:
        obj = {'record_id': classId,'location':'0','topic':'1','t_cs_signed':'-1','time':time}
    
    url = 'https://bookings.instituteofeducation.ie/assets/ajax/updateAttendance.php' #Api's Url
    
    print(obj)  #Debug, shows the parameters passed to the api.
    x = requests.post(url, data = obj) #Posts the api call.
    if json.loads(x.text)["status"] == 1 or json.loads(x.text)["status"] == "1": #Check if the Api returns an error message or not.
      print("\n\033[92m%s\033[0m" % ("[*] REGISTERED!"))
    else:
      print("\n\033[91m%s\033[0m" % ("[*] Something went wrong!"))





def checkNextStart():  #Checks when next class is starting with the Api
    creds = None
    # The file token stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('.token'):
        with open('.token', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.apicreds', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('.token', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    #print('Getting the upcoming 10 events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print("\n\033[91m%s\033[0m" % ('[*] No upcoming events found.'))
    for event in events:
        if "description" in event:
            #print(event['summary'],"-",event['description'])
            return event['start'].get('dateTime', event['start'].get('date'))
        elif "Lunch" in event['summary']:
            ok="ok"
        else:
            #print(event['summary'],"has no code")
            return event['start'].get('dateTime', event['start'].get('date'))


def checkNextCode():  #Checks current class' code. Only works 15min into the class.
    if not os.path.exists('.tmp'):
        os.makedirs('.tmp')
    user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
    headers = { 'User-Agent' : user_agent }
    url = 'https://bookings.instituteofeducation.ie/attendance.php?key=18C3FD9C-4223-0245-8BC2-10A1D393496A'
    r = requests.get(url, headers=headers)
    content = r.text
    file = open(".tmp/index.html", "w") 
    file.write(content) 
    file.close()
    code = parseCode()
    os.remove(".tmp/index.html")
    return code



def checkNextName(): #Checks next class' name
    creds = None

    if os.path.exists('.token'):
        with open('.token', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '.apicreds', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('.token', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)


    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time


    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=5, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:  #If there is no event, then it means the user must double check that everything is working on their side (Google Account)
        print("\n\033[91m%s\033[0m" % ('No upcoming events found. Check that you have connected your Google Calendar with your timetable on the right account, then try again.'))
    for event in events:  #Check event detail, from soonest, to tardliest
        if not "Lunch" in event['summary']:  #If the next even is "Lunch", skip to the next one.
            return event['summary'] #If not then return the event name


def getSeconds(event):   #Get time difference between current time and next class (in seconds). It should be a positive number
    a = datetime.datetime.now()
    return (event-a).total_seconds()

def getSecondsLate(event):  #Get time difference between current time and next class (in seconds), when the user is late. It should be a negative number
    a = datetime.datetime.now()
    return (a-event).total_seconds()


def infos(): #Output many information about next class such as the upcoming class, its time & date, its code, and in how long it is.
    code = True
    nextdate = checkNextStart()
    nextname = checkNextName()
    nextcode = checkNextCode()
    nextevent =  dateutil.parser.isoparse(nextdate).replace(tzinfo=None)

    if nextcode == "null" or nextcode == "N/A":
        print("\033[92m[*] Upcomming:\033[0m \033[94m",nextname,"\033[0mat\033[96m",str(nextevent)+"\033[0m. \033[91mThere is no code.\033[0m")
        code = False
    else:
        print("\033[92m[*] Upcomming:\033[0m \033[94m",nextname,"\033[0mat\033[96m",str(nextevent)+"\033[0m. Code is\033[94m",nextcode,"\033[0m")

    
    if nextevent > datetime.datetime.now():
        sec = str(datetime.timedelta(seconds=math.floor(getSeconds(nextevent))))
        print("\033[95m%s %s\033[0m" % ("[*] It is in",sec))
    else:
        sec = str(datetime.timedelta(seconds=math.floor(getSecondsLate(nextevent))))
        print("\033[95m%s %s %s\033[0m " % ("[*] It was",str(sec),"ago"))

    return getSeconds(nextevent)


def countdown(t, step=1, msg='sleeping'): #This will output filling bar countdown, to wait for an upcoming class, during the night/break.
    print("\n"+msg)
    for i in tqdm(range(t+60)): #The "t+60" adds 60sec to the countdown to account for any lateness from the service, just in case. #BetterBeSafeThanSorry! 
        sleep(1)


class bcolors:           #Color code reference for me, while I'm coding. (Helps a lot, I'm not a machine, I didnt pass the turing test, I dont know all terminal colors)
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


while True:      
    name = checkNextName().replace("/","_").replace(" ","_").replace("_(N_C)","") #Get name + remove spaces & debug values.
    if name != subjectDone:     #Check if it isnt the class that is still ongoing, and if it is next class
        if ongoing != "first":  #If the ongoing class just changed, it will print a limit bar (Terminal Width) and a new line
           limit()
           print()
        ongoing = True
        subjectDone = name      #Stores ongoing class' name
        countdown(int(infos()),step=1,msg="Waiting for class")  #If class hasn't started yet (we are early), we must add a countdown


        #This next bunch of code downloads the page, containing the code.
        import requests
        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
        headers = { 'User-Agent' : user_agent }
        url = 'https://bookings.instituteofeducation.ie/attendance.php?key=18C3FD9C-4223-0245-8BC2-10A1D393496A'
        r = requests.get(url, headers=headers)
        content = r.text
        title = name+"_"+datetime.datetime.now().now().strftime("%d/%m/%Y %H:%M:%S").replace("/","-").replace(" ","_")

        #Creates folders (grabbed_noodles & .tmp) if they do not exist.
        if not os.path.exists('grabbed_noodles'):
            os.makedirs('grabbed_noodles')
        if not os.path.exists('.tmp'):
            os.makedirs('.tmp')

        #Saves the page to two files. The last one is .tmp/index.html. This file is temporary only and will often get overwritten.
        file = open("grabbed_noodles/"+title, "w") 
        file.write(content) 
        file.close() 
        file = open(".tmp/index.html", "w") 
        file.write(content) 
        file.close() 

        #Now we have everything, we must parse the page that has the code, and register our attendance with that code + Current time.
        registerClass(parseCode(), datetime.datetime.now().strftime('%H:%M:%S'), onsite)

        #Let's delete our temporary file.
        os.remove(".tmp/index.html")

        print("\n\033[92m%s\033[0m\n" % ("[*] No Exeptions!")) #If we managed to get this far, then there must be no exceptions
        limit() #Draw a limit bar, terminal's width lengh.
    else:
        if ongoing:  #If last stored class name is equal to current class' name, we must assume it is still the same class and that it isnt over.
            print("\n\033[95m%s\033[0m\n" % ("[*] Waiting for class to end..."))
            ongoing = False
