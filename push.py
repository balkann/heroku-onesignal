from ctypes.wintypes import LANGID
from email import message
from urllib.request import HTTPBasicAuthHandler
from dotenv import load_dotenv
import requests
import sys
import os
from os.path import join, dirname
import csv
#import getpass
from collections import defaultdict

#7 first language
# example calling python3 push.py 5--DayStart 15--DayEnd



dotenv_path = join(dirname(__file__),".env")
load_dotenv(dotenv_path)
def EnvGet(key):
    return os.environ.get(key)


pnMonth = "December"
rest_api_key = EnvGet("REST_KEY")
rest_api_encryption = "Basic"

times = ["12:30PM","06:00PM","09:00PM"]


class NotifArray:
    def __init__(self) : 
        self.messages = []

    def print(self):
        for val in self.messages:
            print(val)

    def __str__(self):
        str = ""
        for val in self.messages:
            str += val.__str__()
            str += "\n"
        return str

    def add(self, x):
        self.messages.append(x)
    
    

class Message:
    def __init__(self, titleDic, messageDic, hour, day, month) :
        self.titleDic = titleDic
        self.messageDic = messageDic
        self.hour = hour
        self.day = day
        self.month = month
        pass

    def __str__(self):
        enTitle = self.titleDic["en"]
        enMessage = self.messageDic["en"]
        return f"Time= {self.hour}/{self.day}/{self.month}\nTitle: {enTitle}\nMessage: {enMessage} \n\n"


if rest_api_key == "" : 
    print("call export REST_KEY=Api key")
    raise SystemExit


def GetLanguageCode(key):
    if key == "Greek":
        return ""
    key = key.replace('(','')
    splitted = key.split('\n')
    return splitted[2].split('_')[0]

languageDictionary = {
            "en": "",
            "ar": "",
            "de": "",
            "es": "",
            "fr": "",
            "hi": "",
            "id": "",
            "it": "",
            "ja": "",
            "ko": "",
            "nl": "",
            "pt": "",
            "ru": "",
            "tr": ""
}
titleDictionary = {
            "en": "",
            "ar": "",
            "de": "",
            "es": "",
            "fr": "",
            "hi": "",
            "id": "",
            "it": "",
            "ja": "",
            "ko": "",
            "nl": "",
            "pt": "",
            "ru": "",
            "tr": ""
}


columns = defaultdict(list) # each value in each column is appended to a list
keys = []
rows = []
header = []
rowCount = 0
columnCount = 0

with open("notifs.csv", encoding="utf-8") as f:
    dicReader = csv.DictReader(f)
    print(dicReader)
    for row in dicReader: # read a row as {column1: value1, column2: value2,...}
        columnCount = 0
        for (k,v) in row.items(): # go over each column name and value 
            keys.append(k)
            rows.append(v)
            columns[k].append(v)
            columnCount += 1
        rowCount+=1


def CreateMessage(order, hour, day, month):
    for i in range(7, columnCount):
        language = keys[i]
        if columns[language][order] != "":
            message = columns[language][order].split('\n')
            titleDictionary[GetLanguageCode(language)] = message[0]
            if(message[1]!= ''):
                languageDictionary[GetLanguageCode(language)] = message[1]
            elif(message[2]!= ''):
                languageDictionary[GetLanguageCode(language)] = message[2]
            else:
                print(f"ERROR Corrupted csv file. !! Column {columnCount + 2} Language {language}")
                sys.exit        
    message = columns[keys[3]][order].split('\n')
    titleDictionary["en"] = message[0]
    if(message[1]!=''):
        languageDictionary["en"] = message[1]
    elif(message[2]!=''):
        languageDictionary["en"] = message[2]
    
    copyTitle ={}
    copyMessage ={}
    for key, value in titleDictionary.items():
        copyTitle[key] = value

    for key, value in languageDictionary.items():
        copyMessage[key] = value


    msg = Message(copyTitle, copyMessage, hour, day, month)
    return msg


#languageDictionary["en"] = Emojize("Find the perfect pair of heels for you and shine on the podium! :sparkles::sparkling_heart:")

def ScheduleNotif(msg : Message):
    
    url = "https://onesignal.com/api/v1/notifications"
    
    app_id = "77ba9bcd-4fa6-4393-b7e0-2f569592c40f" ##high heels app id
    date = f"{msg.month} {msg.day}, 2022 02:00 AM UTC-03:00"

    campaignName = "UncoAutomation"

    titleDictionary = msg.titleDic
    content = msg.messageDic

    payload = {
        "app_id" : app_id,
        "included_segments": ["Subscribed Users"],
        "headings" : titleDictionary,
        "contents": content,
        "name": titleDictionary["en"],
        "send_after": date,
        "delayed_option": "timezone",
        "delivery_time_of_day": msg.hour
    }

    headers = {
        "Authorization": f"{rest_api_encryption} {rest_api_key}"
    }

    #response = requests.post(url, json=payload, headers=headers)
    #print(response.text)

def ControlCsvFile():
    for i in range(0, rowCount):
        CreateMessage(i)

def sendNotifs(startDay, endDay, restKey):
    rest_api_key = restKey
   
    notif_array = NotifArray()
    for i in range(startDay, endDay+1) :
        for k in range(0,3):
            key = ((i*k)+i) % rowCount
            notif_array.add(CreateMessage(key, times[k], i, pnMonth))
    notif_array.print()
    result = input("Do you want to send these messages? y/n")
    if(result == "y"):
        for message in notif_array.messages:
            ScheduleNotif(message)
    return notif_array


    
