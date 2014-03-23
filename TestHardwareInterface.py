import HardwareInterface
import time


hw = HardwareInterface()
hw.run()

print "buzz"
hw.buzz()
time.sleep(1)


print "dispense"
hw.dispense()
time.sleep(1)

print "buzz dispense"
hw.buzz()
hw.dispense()
time.sleep(1)
