import CameraInterface as ci

my_cam = ci.CameraInterface('./derp.jpg')
my_cam.start()
time.sleep(30)
my_cam.shutdown()
my_cam.join()

