import RPi.GPIO as GPIO
import os
import time
import threading

        
class HardwareInterface(threading.Thread):
    def __init__(self):
        super(HardwareInterface, self).__init__()
        self.setDaemon(True)
        self.running = False
        # Set our RPI pin numbers
        self.coil_A_1_pin = 18# 4
        self.coil_A_2_pin = 23#17
        self.coil_B_1_pin = 24 #23
        self.coil_B_2_pin = 25 #24
        self.bzzz = 4
        self.trigger = 27 #22
        GPIO.setwarnings(False)
        # Set our input versus output pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        GPIO.setup(self.bzzz, GPIO.OUT)
        GPIO.setup(self.trigger, GPIO.IN)

        # setup our internal state
        self.step = 0
        self.max_steps = 5
        self.dispensing = False
        self.last_button_state = False
        self.buzz = False
        self.buzz_count = 0
        self.buzz_max = 100
        self.delay=0.015

        # setup our callback lists
        self.down_cb = []
        self.up_cb = []
        self.feed_cb = []
        self.buzz_cb = []
        

    def dispense(self):
        # dispense a treat 
        if not self.dispensing:
            # set the flag and do our work
            self.step=0
            self.dispensing = True
            # tell all our call backs what up
            for cb in self.feed_cb:
                cb()

            
    def buzz_once(self):
        # if we're not already buzzing 
        if not self.buzz:
            # set the state variables
            self.buzz_count = 0
            self.buzz = True
            self.turn_on_buzzer()
            for cb in self.buzz_cb:
                cb()



    # Methods to set the call back
    def on_button_down(self,cb):
        self.down_cb.append(cb)

    def on_button_up(self,cb):
        self.up_cb.append(cb)

    def on_feed(self,cb):
        self.feed_cb.append(cb)

    def on_buzz(self,cb):
        self.buzz_cb.append(cb)


    # Set the pins forward in order.
    def forward_step(self):  
        self.set_step(1, 0, 1, 0)
        time.sleep(self.delay)
        self.set_step(0, 1, 1, 0)
        time.sleep(self.delay)
        self.set_step(0, 1, 0, 1)
        time.sleep(self.delay)
        self.set_step(1, 0, 0, 1)

    # Set the pins high/low in order
    def backwards_step(self):
        self.set_step(1, 0, 0, 1)
        time.sleep(self.delay)
        self.set_step(0, 1, 0, 1)
        time.sleep(self.delay)
        self.set_step(0, 1, 1, 0)
        time.sleep(self.delay)
        self.set_step(1, 0, 1, 0)
 
    # map high/low to actual pins
    def set_step(self,w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    # turn on the buzzer
    def turn_on_buzzer(self):
        GPIO.output(self.bzzz,1)

    def turn_off_buzzer(self):
        GPIO.output(self.bzzz,0)

    def shutdown(self):
        # signal the main thread
        self.running = False
        # give it a second to end
        time.sleep(0.1)
        # set all the pins low
        GPIO.output(self.coil_A_1_pin,0)
        GPIO.output(self.coil_A_2_pin,0)
        GPIO.output(self.coil_B_1_pin,0)
        GPIO.output(self.coil_B_2_pin,0) 
        GPIO.output(self.bzzz, 0)

        
    def run(self):
        self.running = True
        # while running
        while self.running:
            # if buzzing update the buzz countdown
            if( self.buzz ):
                self.buzz_count += 1
                if( self.buzz_count >= self.buzz_max ):
                    self.turn_off_buzzer()
                    self.buzz = False
        
            # if dispensiing move one step forward and update
            if( self.dispensing ):
                self.forward_step()
                self.step += 1
                if( self.step >= self.max_steps):
                    self.dispensing = False
            # look for the the 1->0 button transition
            if( self.last_button_state and 
                GPIO.input(self.trigger) == False ):
                self.last_button_state = False
                # signal our callbacks
                for cb in self.up_cb:
                    cb()
            # button down
            # look for the the 0->1 button transition
            if( not self.last_button_state and 
                GPIO.input(self.trigger) == True ):
                self.last_button_state = True
                # signal our callbacks
                for cb in self.down_cb:
                    cb()
            time.sleep(self.delay)
        
       

 
 
