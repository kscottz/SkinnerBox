import RPi.GPIO as GPIO
import os
import time
import threading

        
class HardwareInterface(threading.Thread):
    def __init__(self):
        super(HardwareInterface, self).__init__()
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

        self.buzz = False
        self.buzz_count = 0
        self.buzz_max = 100
        self.delay=0.01

    def dispense(self):
        if not self.dispensing:
            self.step=0
            self.dispensing = True
            
    def buzz_once(self):
        if not self.buzz:
            self.buzz_count = 0
            self.buzz = True
            self.turn_on_buzzer()

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
            
            time.sleep(self.delay)
        
       

 
 
