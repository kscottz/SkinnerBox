import os
import time
import datetime as dt
import threading
import numpy as np
        
class ProtocolRunner(threading.Thread):
    def __init__(self,hardware,data,period_seconds=60,response_window_s=10):
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
        self.period_seconds = dt.timedelta(seconds=period_seconds)
        self.last_experiment = dt.datetime.now()
        self.response_window_s = dt.timedelta(seconds=response_window_s)
        self.on_fail_cb = []
        self.on_pass_cb = []
        self.on_start_cb = []
        self.on_end_cb = []

    def add_on_start_cb(self,cb):
        self.on_start_cb.append(cb)

    def add_on_end_cb(self,cb):
        self.on_end_cb.append(cb)

    def add_on_pass_cb(self,cb):
        self.on_pass_cb.append(cb)

    def add_on_fail_cb(self,cb):
        self.on_fail_cb.append(cb)

    def shutdown(self):
        self.running = False

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False

    def button_callback(self):
        if( self.experiment_running ):
            diff = dt.datetime.now() - self.last_experiment
            # did we press the button in time?
            if( diff <= self.response_window_s):                
                self.hardware.dispense()
                #self.data_interface.log_success() # this needs to be moved out
                self.experiment_running = False
                self.last_experiment = dt.datetime.now()
                [cb() for cb in self.on_end_cb]
                [cb() for cb in self.on_pass_cb]
            
    def run(self):
        self.running = True
        while self.running:
            if( self.isEnabled ):
                diff = dt.datetime.now() - self.last_experiment
                if( self.experiment_running ):
                    if( diff > self.response_window_s ):
                        self.experiment_running = False
                        self.data_interface.log_fail() # this needs to be moved out 
                        self.last_experiment = dt.datetime.now()
                        [cb() for cb in self.on_end_cb]
                        [cb() for cb in self.on_fail_cb]

                # time to do another experiment?
                elif(diff > self.period_seconds):
                    self.last_experiment = dt.datetime.now()
                    self.hardware.buzz_once()
                    [cb() for cb in self.on_start_cb]
                    self.experiment_running = True
            time.sleep(0.2)
