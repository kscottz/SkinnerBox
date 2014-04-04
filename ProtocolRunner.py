import os
import time
import threading
import numpy as np
        
class ProtocolRunner(threading.Thread):
    def __init__(self,hardware,database):
        super(ProtocolRunner, self).__init__()
        self.running = False
        self.hardware = hardware
        self.hardware.on_button_down(self.button_callback)
        self.database = database
        self.isEnabled = False
        self.activity = 0
        self.state = "not_started" # not_started / waiting_for_press
        self.experiment_started = False
        
    def shutdown(self):
        self.running = False

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False


    def get_recent_activity(self):
        data = self.db.cv_data.find()
        signal = []
        for d in data:
            signal.append(d['activity'])
        return np.array(signal)
    
    def check_for_activity(self):
        if( self.activity > 0 ):
            self.activity = self.activity - 1
            if( self.activity == 0 ):
                # log failure
                pass
            return False
                
        signal = self.get_recent_activity()
        lately_sample = 60
        
        if( len(signal) < lately_sample ):
            return False

        lately = np.mean(signal[-1*lately_sample:])
        sz = min(len(signal),60*60*1.5)
        past_hour_mean = np.mean(signal[-1*sz:])
        past_hour_std = np.std(signal[-1*sz:])

        if( lately > past_hour_mean+1.5*past_hour_std):
            self.activity = 60
            return True
        return False

    def button_callback(self):
        if( self.state < 60 ):
            # log a success
            self.hardware.feed()
        
    def run(self):
        self.running = True
        while self.running:
            if( self.enabled ):
                if( self.check_for_activity()):                
                    self.hardware.buzz()
                    self.state = 60
                time.sleep(1)
