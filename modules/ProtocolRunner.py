import os
import time
import datetime.datetime as dt
import threading
import numpy as np
        
class ProtocolRunner(threading.Thread):
    def __init__(self,hardware,data,period_minutes=1,response_window_s=60):
        super(ProtocolRunner, self).__init__()
        self.setDaemon(True)
        self.running = False
        self.hardware = hardware
        # this might need to go outside the class
        self.hardware.on_button_down(self.button_callback)
        self.data_interface = data
        self.isEnabled = False
        self.activity = 0
        self.state = "not_started" # not_started / waiting_for_press
        self.experiment_running = False
        self.last_experiment = dt.now()
        self.response_window_s = response_window_s
        
    def shutdown(self):
        self.running = False

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False


    # def get_recent_activity(self):
    #     data = self.db.cv_data.find()
    #     signal = []
    #     for d in data:
    #         signal.append(d['activity'])
    #     return np.array(signal)
    
    # def check_for_activity(self):
    #     if( self.activity > 0 ):
    #         self.activity = self.activity - 1
    #         if( self.activity == 0 ):
    #             # log failure
    #             pass
    #         return False
                
    #     signal = self.get_recent_activity()
    #     lately_sample = 60
        
    #     if( len(signal) < lately_sample ):
    #         return False

    #     lately = np.mean(signal[-1*lately_sample:])
    #     sz = min(len(signal),60*60*1.5)
    #     past_hour_mean = np.mean(signal[-1*sz:])
    #     past_hour_std = np.std(signal[-1*sz:])

    #     if( lately > past_hour_mean+1.5*past_hour_std):
    #         self.activity = 60
    #         return True
    #     return False

    def button_callback(self):
        if( self.experiment_running ):
            diff = dt.now() - self.last_experiment
            # did we press the button in time?
            if( diff.seconds <= self.response_window_s):                
                self.hardware.feed()
                self.data_interface.log_success()
                self.experiment_running = False

            
    def run(self):
        self.running = True
        while self.running:
            if( self.enabled ):
                diff = dt.now() - self.last_experiment
                if( self.experiment_running ):
                    if( diff > self.response_window_s ):
                        self.experiment_running = False
                        self.data_inteface.log_fail()
                        
                # time to do another experiment?
                elif (diff.seconds / 60) > self.period_minutes):
                    self.last_experiment = dt.now()
                    self.hardware.buzz()
                    self.experiment_running = True
            time.sleep(0.2)
