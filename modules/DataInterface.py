import pymongo
from pymongo import MongoClient
import matplotlib
matplotlib.use('AGG') # gets rid of the backend
import matplotlib.pyplot as plt
import numpy as np
from  datetime import datetime, timedelta

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
            
    def isActive(self,threshold=20.0):
        return True

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

    def log_success(self):
        data = {}
        data['event'] = "success"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)

    def log_fail(self):
        data = {}
        data['event'] = "fail"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)

    def log_start(self):
        data = {}
        data['event'] = "exp_start"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)

    def log_stop(self):
        data = {}
        data['event'] = "exp_stop"
        data['time_stamp'] = datetime.now()
        self.events.insert(data)

    def eventToNP(self,event,count):
        data = self.events.find({'event':event}).sort('time_stamp', pymongo.DESCENDING).limit(count)
        times = []
        for d in data:
            times.append(d['time_stamp'])
        times.reverse()
        return times

    def generateEvents(self,path='./img/events.png',count=10):
        food_time = self.eventToNP('food',count)
        buzz_time = self.eventToNP('buzz',count)
        press_time = self.eventToNP('press',count)
        fig, ax = plt.subplots()
        ax.plot_date(food, food_time)
        ax.plot_date(buzz, buzz_time)
        ax.plot_date(press, press_time)
        #plt.plot(values,'b-')
        fig.autofmt_xdate()
        plt.grid()
        plt.title("Rat Events")
        plt.xlabel("Time")
        plt.ylabel("Event")
        plt.savefig(path)
        plt.close()


    def generateActivity(self,path='./img/activity.png'):
        yesterday = datetime.now() - timedelta(hours=24)
        mydata = self.activity.find({"time_stamp": {"$gt": yesterday}}).sort('time_stamp', pymongo.DESCENDING)
        times = []
        values = []
        for d in mydata:
            times.append(d['time_stamp'])
            values.append(d['activity'])
        values.reverse()
        values = np.array(values)
        values = values / np.max(values)
        times.reverse()
        fig, ax = plt.subplots()
        ax.plot_date(times, values)
        #plt.plot(values,'b-')
        fig.autofmt_xdate()
        plt.grid()
        plt.title("Relative Rat Activity Over Time.")
        plt.xlabel("Time")
        plt.ylabel("Normalized Activity")
        plt.savefig(path)
        plt.close()

    def generatePassFail(self,path='./img/pass_fail.png'):
        yesterday = datetime.now() - timedelta(hours=24)
        passes = self.events.find({"time_stamp": {"$gt": yesterday},"event":"success"}).count()
        fails  = self.events.find({"time_stamp": {"$gt": yesterday},"event":"fail"}).count()
        width = 1.0
        fig, ax = plt.subplots()
        print passes,fails
        rects1 = ax.bar([1],[passes], width=1, color='g')
        rects2 = ax.bar([3],[fails], width=1, color='r')
        # add some
        ax.set_ylabel('Scores Today')
        ax.set_title('Test Performance')
        ax.set_xticks([1.5,3.5])
        ax.set_xticklabels( ('pass', 'fail') )
        plt.xlim([0,5])
        ax.legend( ('PASS', 'FAIL') )
        plt.grid()
        plt.savefig(path)
        plt.close()

    def generateStats(self):
        yesterday = datetime.now() - timedelta(hours=24)
        passes = self.events.find({"time_stamp": {"$gt": yesterday},"event":"success"}).count()
        fails  = self.events.find({"time_stamp": {"$gt": yesterday},"event":"fail"}).count()
        food  = self.events.find({"time_stamp": {"$gt": yesterday},"event":"food"}).count()
        buzz  = self.events.find({"time_stamp": {"$gt": yesterday},"event":"buzz"}).count()
        press  = self.events.find({"time_stamp": {"$gt": yesterday},"event":"press"}).count()
        activity_data = self.activity.find({"time_stamp": {"$gt": yesterday}}).sort('time_stamp', pymongo.DESCENDING)
        retVal = {}
        experiments={}
        experiments['passes'] = passes
        experiments['fails'] = fails
        total = passes+fails
        experiments['total'] = total
        experiments['correct'] = round(passes/float(total),2)
        experiments['incorrect'] = round(fails/float(total),2)
        events={}
        events['food'] = food
        events['buzz'] = buzz
        events['press'] = press
        activity={}
        values = []
        for d in activity_data:
            values.append(d['activity'])
        activ= np.array(values)
        activity['mean activity'] = np.mean(activ)
        activity['max activity'] = np.max(activ)
        activity['min activity'] = np.min(activ)
        retVal['activity'] = activity
        retVal['experiments'] = experiments
        retVal['events'] = events
        return retVal
