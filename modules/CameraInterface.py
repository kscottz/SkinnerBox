import os
import io
import cv2
import cv
import picamera
import threading
import numpy as np
import time

class CameraInterface(threading.Thread):
    def __init__(self,img_path="/img/live.jpg"):
        super(CameraInterface, self).__init__()
        self.setDaemon(True)
        # set our path for ouput images
        self.img_path = img_path
        # our default size
        self.img_sz = (640,480)
        self.running = False
        self.delay=0.1
        # images for activity calculations
        self._current_image = None
        self._last_image = None 
        # our list of callbacks
        self._cvlist = []

        
    # allow the user to set a callback
    def set_motion_callback(self,cb):
        self._cvlist.append(cb)

    # stop the main thread
    def shutdown(self):
        self.running = False

    # do the activity calculation
    def _calculate_motion(self):
        # if this our first call to this function
        if( self._last_image is None ):
            # convert the image to gray
            temp = cv2.cvtColor(self._current_image,cv2.cv.CV_BGR2GRAY)
            # set the last image to this image -- causes no motion
            # on first iteration
            self._last_image = temp   
        # make the current image gray -- faster
        temp = cv2.cvtColor(self._current_image,cv2.cv.CV_BGR2GRAY)
        # get the diff of the images
        diff = self._last_image-temp
        # get the mean of absolute difference between images
        change =  np.mean(np.abs(diff))
        # now filter the image, so we don't jump super quick
        self._last_image = (0.2*temp)+(self._last_image*0.8)
        # do our call backs
        for cb in self._cvlist:
            cb(change)
            
    def _get_image(self):
        # get a new image through a stream
        stream = io.BytesIO()
        # get the image out of the camera
        with picamera.PiCamera() as camera:
            camera.start_preview()
            # have the camera do the resizing onboard and save as png
            camera.capture(stream, format='png',resize=self.img_sz)
        # convert the png string from the camera to np 
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        # convert the image to a cv2 image -- stripping compression
        self._current_image = cv2.imdecode(data, 1)
        # save the image to file
        cv2.imwrite(self.img_path,self._current_image)
    
    def run(self):
        self.running = True
        while self.running:
            # now the thread loop is easy
            # get an image
            self._get_image()
            # calculate motion
            self._calculate_motion()
            # hang out for a bit
            time.sleep(self.delay)
        

