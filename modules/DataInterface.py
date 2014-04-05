import pymongo
from pymongo import MongoClient
import matplotlib
matplotlib.use('AGG') # gets rid of the backend
import matplotlib.pyplot as plt
import numpy as np
from  datetime import datetime

class DataInterface():

    def __init__(self,uri='mongodb://localhost:27017',db_name="SkinnerBox"):
        self.client = None
        self.db = None
        try:
            self.client = MongoClient(uri)
            print self.client
            self.db = self.client[db_name]
            self.activity = self.db.activity
            self.events = self.db.events
            self.experiment = self.db.experiment
        except:
            print "Golly, we can't connect to Mongo."
            

    def log_activity(self,activity):
        data = {}
        data['activity'] = activity
        data['time_stamp'] = datetime.now()
        self.activity.insert(data)

    def log_experient(self,success):
        data = {}
        data['success'] = success
        data['time_stamp'] = datetime.now()
        self.experiment.insert(data)

    def log_buzz(self):
        data = {}
        data['event'] = "buzz"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)
       
    def log_press(self):
        data = {}
        data['event'] = "press"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)

    def log_food(self):
        data = {}
        data['event'] = "food"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)

    def generateActivity(self,path='./img/activity.png'):
        mydata = self.activity.find().sort('time_stamp', pymongo.DESCENDING).limit(60)
        times = []
        values = []
        for d in mydata:
            times.append(d['time_stamp'])
            values.append(d['activity'])
        values.reverse()
        plt.plot(values,'b-')
        plt.grid()
        plt.title("Rat activity over time.")
        plt.xlabel("Time in S.")
        plt.ylabel("Activity")
        plt.savefig(path)
        plt.close()

    
