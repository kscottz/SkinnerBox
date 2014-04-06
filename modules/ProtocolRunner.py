import os
import time
import datetime as dt
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
        self.isEnabled = True
        self.activity = 0
        self.state = "not_started" # not_started / waiting_for_press
        self.experiment_running = False
        self.period_minutes = dt.timedelta(seconds=period_minutes*60)
        self.last_experiment = dt.datetime.now()
        self.response_window_s = dt.timedelta(seconds=response_window_s)
        
    def shutdown(self):
        self.running = False

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False

    def button_callback(self):
        print "BUTTON"
        if( self.experiment_running ):
            diff = dt.datetime.now() - self.last_experiment
            # did we press the button in time?
            if( diff <= self.response_window_s):                
                print "PASS!!!"
                self.hardware.dispense()
                self.data_interface.log_success()
                self.experiment_running = False

            
    def run(self):
        self.running = True
        while self.running:
            if( self.isEnabled ):
                diff = dt.datetime.now() - self.last_experiment
                if( self.experiment_running ):
                    print "EXPERIMENT RUNNING"
                    if( diff > self.response_window_s ):
                        print "EXPERIMENT DONE"
                        self.experiment_running = False
                        self.data_interface.log_fail()                 
                # time to do another experiment?
                elif(diff > self.period_minutes):
                    print "EXPERIMENT STARTED"
                    self.last_experiment = dt.datetime.now()
                    self.hardware.buzz_once()
                    self.experiment_running = True
            time.sleep(0.2)
