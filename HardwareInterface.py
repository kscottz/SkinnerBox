import RPi.GPIO as GPIO
import os
import time
import threading

        
class HardwareInterface(threading.Thread):
    def __init__(self):
        super(HardwareInterface, self).__init__()
        self.setDaemon(True)
        self.running = False
        self.coil_A_1_pin = 18# 4
        self.coil_A_2_pin = 23#17
        self.coil_B_1_pin = 24 #23
        self.coil_B_2_pin = 25 #24
        self.bzzz = 4
        self.trigger = 27 #22
        print "setting up io"
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)
        GPIO.setup(self.bzzz, GPIO.OUT)
        GPIO.setup(self.trigger, GPIO.IN)

        self.step = 0
        self.max_steps = 4
        self.dispensing = False

        self.last_button_state = False
        self.down_cb = []
        self.up_cb = []
        self.feed_cb = []
        self.buzz_cb = []
        
        self.buzz = False
        self.buzz_count = 0
        self.buzz_max = 100
        self.delay=0.01

    def dispense(self):
        if not self.dispensing:
            self.step=0
            self.dispensing = True
            for cb in self.feed_cb:
                cb()

            
    def buzz_once(self):
        if not self.buzz:
            self.buzz_count = 0
            self.buzz = True
            self.turn_on_buzzer()
            for cb in self.buzz_cb:
                cb()


    def on_button_down(self,cb):
        self.down_cb.append(cb)

    def on_button_up(self,cb):
        self.up_cb.append(cb)

    def on_feed(self,cb):
        self.feed_cb.append(cb)

    def on_buzz(self,cb):
        self.buzz_cb(cb)


    def forward_step(self):  
        self.set_step(1, 0, 1, 0)
        time.sleep(self.delay)
        self.set_step(0, 1, 1, 0)
        time.sleep(self.delay)
        self.set_step(0, 1, 0, 1)
        time.sleep(self.delay)
        self.set_step(1, 0, 0, 1)

 
    def backwards_step(self):
        self.set_step(1, 0, 0, 1)
        time.sleep(self.delay)
        self.set_step(0, 1, 0, 1)
        time.sleep(self.delay)
        self.set_step(0, 1, 1, 0)
        time.sleep(self.delay)
        self.set_step(1, 0, 1, 0)
 
    def set_step(self,w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def turn_on_buzzer(self):
        GPIO.output(self.bzzz,1)

    def turn_off_buzzer(self):
        GPIO.output(self.bzzz,0)

    def power_down(self):
        self.running = False
        time.sleep(0.01)
        GPIO.output(self.coil_A_1_pin,0)
        GPIO.output(self.coil_A_2_pin,0)
        GPIO.output(self.coil_B_1_pin,0)
        GPIO.output(self.coil_B_2_pin,0) 
        GPIO.output(self.bzzz, 0)

        
    def run(self):
        self.running = True
        while self.running:
            if( self.buzz ):
                self.buzz_count += 1
                if( self.buzz_count >= self.buzz_max ):
                    self.turn_off_buzzer()
                    self.buzz = False
        
            if( self.dispensing ):
                self.forward_step()
                self.step += 1
                if( self.step >= self.max_steps):
                    self.dispensing = False
            # button up
            if( self.last_button_state and 
                GPIO.input(self.trigger) == False ):
                self.last_button_state = False
                for cb in self.up_cb:
                    cb()
            # button down
            if( not self.last_button_state and 
                GPIO.input(self.trigger) == True ):
                self.last_button_state = True
                for cb in self.down_cb:
                    cb()
            time.sleep(self.delay)
        
       

 
 
