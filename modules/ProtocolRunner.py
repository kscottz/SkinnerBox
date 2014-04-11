import os
import time
import datetime as dt
import threading
import numpy as np
        
class ProtocolRunner(threading.Thread):
    def __init__(self,hardware,period_s=60,response_window_s=10):
        super(ProtocolRunner, self).__init__()
        # have this thread exit when main loop exits
        self.setDaemon(True)
        self.running = False
        # add a pointer to our hardware object
        self.hardware = hardware
        # allows us to turn off experiments.
        self.isEnabled = True
        self.experiment_running = False
        # set the time between experiments as a time delta. 
        self.period_seconds = dt.timedelta(seconds=period_s)
        # the time of the last experiment
        self.last_experiment = dt.datetime.now()
        # how long the rat's have to respond.
        self.response_window_s = dt.timedelta(seconds=response_window_s)
        # a set of lists of callbacks.
        self.on_fail_cb = []
        self.on_pass_cb = []
        self.on_start_cb = []
        self.on_end_cb = []

        
    # allow the user to set callbacks.
    def add_on_start_cb(self,cb):
        self.on_start_cb.append(cb)

    def add_on_end_cb(self,cb):
        self.on_end_cb.append(cb)

    def add_on_pass_cb(self,cb):
        self.on_pass_cb.append(cb)

    def add_on_fail_cb(self,cb):
        self.on_fail_cb.append(cb)


    # stop the main loop.
    def shutdown(self):
        self.running = False

    def enable(self):
        self.isEnabled = True

    def disable(self):
        self.isEnabled = False

    # this method must be added to the main hardware
    # button callback.
    def button_callback(self):        
        if( self.experiment_running ):
            diff = dt.datetime.now() - self.last_experiment
            # did we press the button in time?
            if( diff <= self.response_window_s):
                # tell the hardware to dispense a treat
                self.hardware.dispense()
                # kill the experiments
                self.experiment_running = False
                # get ready for the next experiments
                self.last_experiment = dt.datetime.now()
                # call all of our callbacks
                [cb() for cb in self.on_end_cb]
                [cb() for cb in self.on_pass_cb]
            
    def run(self):
        self.running = True
        while self.running:
            if( self.isEnabled ):
                # do a time diff to see how long it
                # has been since the last experiment
                diff = dt.datetime.now() - self.last_experiment
                # if the experiment is running
                if( self.experiment_running ):
                    # the rat didn't push the lever in time
                    if( diff > self.response_window_s ):
                        self.experiment_running = False
                        # set time for the next experiment
                        self.last_experiment = dt.datetime.now()
                        # do our callbacks
                        [cb() for cb in self.on_end_cb]
                        [cb() for cb in self.on_fail_cb]

                # time to do another experiment?
                elif(diff > self.period_seconds):
                    # mark the experiment start time
                    self.last_experiment = dt.datetime.now()
                    # buzz the buzzer
                    self.hardware.buzz_once()
                    # do our callbacks
                    [cb() for cb in self.on_start_cb]
                    # set our flag to true. 
                    self.experiment_running = True
            time.sleep(0.2)
