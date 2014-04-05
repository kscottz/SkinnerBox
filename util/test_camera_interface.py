import CameraInterface as ci
import time

my_cam = ci.CameraInterface('derp.jpg')
my_cam.start()
time.sleep(90)
my_cam.shutdown()
my_cam.join()

