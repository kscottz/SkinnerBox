import os
import io
import cv2
import cv
import picamera
import threading
import numpy as np
import time

class CameraInterface(threading.Thread):
    def __init__(self,img_path):
        super(CameraInterface, self).__init__()
        self.setDaemon(True)
        self.img_path = img_path
        self.img_sz = (320,240)
        self.running = False
        self.delay=0.01
        self._current_image = None
        self._last_image = None 
        self._cvlist = []

        
    def set_motion_callback(self,cb):
        self._cvlist.append(cb)

    def shutdown(self):
        self.running = False

    def _calculate_motion(self):
        if( self._last_image is None ):
            temp = cv2.cvtColor(self._current_image,cv2.cv.CV_BGR2GRAY)
            self._last_image = temp        
        temp = cv2.cvtColor(self._current_image,cv2.cv.CV_BGR2GRAY)
        diff = self._last_image-temp 
        change =  np.mean(np.abs(diff))
        self._last_image = (0.2*temp)+(self._last_image*0.8)
        for cb in self._cvlist:
            cb(change)
            
    def _get_image(self):
        #self._last_image = self._current_image
        stream = io.BytesIO()
        with picamera.PiCamera() as camera:
            camera.start_preview()
            camera.capture(stream, format='png',resize=self.img_sz)
        data = np.fromstring(stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        self._current_image = cv2.imdecode(data, 1)
        cv2.imwrite(self.img_path,self._current_image)
    
    def run(self):
        self.running = True
        while self.running:
            self._get_image()
            self._calculate_motion()
            time.sleep(self.delay)
        

