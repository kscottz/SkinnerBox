import pymongo
from pymongo import MongoClient
import matplotlib
matplotlib.use('AGG') # gets rid of the backend
# matplot lib wants to pop up windows.
# this tells matplotlib, no, we really just want to render 
# to file 'cause the pi is in headless mode.
import matplotlib.pyplot as plt
import numpy as np
from  datetime import datetime, timedelta

class DataInterface():

    def __init__(self,uri='mongodb://localhost:27017',db_name="SkinnerBox"):
        self.client = None
        self.db = None
        try:
            # try to create our client
            self.client = MongoClient(uri)
            print self.client
            self.db = self.client[db_name]
            # set our databases
            self.activity = self.db.activity
            self.events = self.db.events
            self.experiment = self.db.experiment
        except:
            print "Golly, we can't connect to Mongo."
            

    # the following functions are really simple
    # but provide a standard way of saving data to the db
    # if we just had one method you could have someone
    # using different terms e.g. success vs. win
    # All our events are basically timestamp / event type
    # pairs.
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

    def generateActivity(self,path='./img/activity.png'):
        """
        Generate an activity plot of the past 24 hours
        """
        # create a time difference that is 24 hours in the past
        yesterday = datetime.now() - timedelta(hours=24)
        # ask mongo to find where the timestamp of activity
        # is greater than yesterday, and sort it descending
        query = {"time_stamp": {"$gt": yesterday}}
        mydata = self.activity.find(query).sort('time_stamp', pymongo.ASCENDING)
        #values = [d['activity'] for d in mydata]
        #times = [d['time_stamp'] for d in mydata]
        values = []
        times = []
        for d in mydata:
            values.append(d['activity'])
            times.append(d['time_stamp'])
        values = np.array(values)

        # normalize the values
        values = values / np.max(values)
        # do numpy stuff
        fig, ax = plt.subplots()
        ax.plot_date(times, values)        
        fig.autofmt_xdate()
        plt.grid()
        plt.title("Relative Rat Activity Over Time.")
        plt.xlabel("Time")
        plt.ylabel("Normalized Activity")
        # save the figure to file and close. 
        plt.savefig(path)
        plt.close()

    def generatePassFail(self,path='./img/pass_fail.png'):
        """
        Generate a bar chart of passes versus fails.
        """
        # figure out the end of our 24 hour period
        yesterday = datetime.now() - timedelta(hours=24)
        # ask mongo to count the number of pass and fail events
        # between now and yesterday
        passes = self.events.find({"time_stamp": {"$gt": yesterday},"event":"success"}).count()
        fails  = self.events.find({"time_stamp": {"$gt": yesterday},"event":"fail"}).count()
        width = 1.0
        fig, ax = plt.subplots()
        # generate the bar chart
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
        """
        Resturn a summarized dictionary of all the events in the
        past 24 hours.
        """
        # figure out the difference between now and 24 hours ago
        yesterday = datetime.now() - timedelta(hours=24)
        # count all of each event type for the past data.
        events = ["success","fail","food","buzz","press"]
        count = {}
        for e in events:
            query = {"time_stamp": {"$gt": yesterday},"event":e}
            count[e] = self.events.find(query).count()
        # activity has its own repo
        activity_data = self.activity.find({"time_stamp": {"$gt": yesterday}}).sort('time_stamp', pymongo.DESCENDING)
        retVal = {}
        # we're going to use dicts here to make rendering easy
        retVal["experiments"] = {}
        retVal["events"] = {}
        retVal["activity"] = {}

        retVal["experiments"]['passes'] = count["success"]
        retVal["experiments"]['fails'] = count["fail"]
        total = count["fail"]+count["success"]
        retVal["experiments"]['total'] = total
        retVal["experiments"]['correct'] = round(count["success"]/float(total),2)
        retVal["experiments"]['incorrect'] = round(count["fail"]/float(total),2)

        retVal["events"]['food'] = count["food"]
        retVal["events"]['buzz'] = count["buzz"]
        retVal["events"]['press'] = count["press"]
        activity={}

        values = np.array([d['activity'] for d in activity_data])
        retVal["activity"]['Avg Activity'] = np.mean(values)
        retVal["activity"]['Max Activity'] = np.max(values)
        retVal["activity"]['Min Activity'] = np.min(values)

        return retVal
