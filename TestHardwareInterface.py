import HardwareInterface as hwi
import time
import signal

hw = hwi.HardwareInterface()

def signal_handler(signal, frame):
    hw.join()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

hw.start()

print "buzz"
hw.buzz_once()
time.sleep(3)


print "dispense"
hw.dispense()
time.sleep(2)

print "buzz dispense"
hw.buzz_once()
hw.dispense()
time.sleep(3)

def buzzbuzz():
    hw.dispense()

hw.on_button_down(buzzbuzz)

time.sleep(20)




hw.power_down()
hw.join()
