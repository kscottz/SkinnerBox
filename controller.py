import RPi.GPIO as GPIO
import os
import time
 
GPIO.setmode(GPIO.BCM)
 
enable_pin = 22 #18
coil_A_1_pin = 18# 4
coil_A_2_pin = 23#17
coil_B_1_pin = 24 #23
coil_B_2_pin = 25 #24

bzzz = 4
trigger_pin = 27 #22
 
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
GPIO.setup(bzzz, GPIO.OUT)
GPIO.setup(trigger_pin, GPIO.IN)
 
GPIO.output(enable_pin, 1)
 
def forward(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)
 
def backwards(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1)
    GPIO.output(bzzz,0)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    GPIO.output(bzzz,0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    GPIO.output(bzzz,0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    GPIO.output(bzzz,0)
    time.sleep(delay)
 
  
def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)
 

steps = 5
delay = 10
i = 0

while True:
  print GPIO.input(trigger_pin)
  if( GPIO.input(trigger_pin) == False ):
    forward(int(delay) / 1000.0, int(steps))
    GPIO.output(bzzz,1)
    name = "Image{0}.jpg".format(i)
    os.system("raspistill -t 0.01 -o "+name)
    time.sleep(0.3)
    i+=1
  else:
    backwards(int(delay) / 1000.0,int(1))
