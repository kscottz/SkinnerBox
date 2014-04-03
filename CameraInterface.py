import os
import io
import cv2
import time
import picamera
import threading
import numpy as np

class CameraInterface(threading.Thread):
    def __init__(self,img_path):
        super(HardwareInterface, self).__init__()
        self.img_path
        self.img_sz = (320,240)
        self.running = False
        self.delay=1.0
        self.current_image = None
        self.current_image_gray = None
        self.last_image = None
        self.last_image_gray = None
        self._stream = io.BytesIO()
        self._mx = cv2.cv.CreateImage(self.img_sz, cv2.cv.IPL_DEPTH_32F, 1)
        self._my = cv2.cv.CreateImage(self.img_sz, cv2.cv.IPL_DEPTH_32F, 1)
        
        
    def set_motion_callback(self,cb):
        pass

    def shutdown(self):
        self.running = False

    def _calculate_motion(self):
        cv2.cvtColor(self._current_image,self._current_image_gray,cv2.CV_RGB2GRAY)
        if( self._current_image_gray ):
            window = (11,11)
            cv.CalcOpticalFlowLK(self.current_image_gray,
                                 self.last_image_gray,
                                 window,
                                 self._mx,self._my)
           

    def _get_image(self):
        self._last_image = self._current_image
        self._last_image_gray = self.current_image_gray
        with picamera.PiCamera() as camera:
            camera.start_preview()
            time.sleep(0.5)
            camera.capture(self._stream, format='jpeg',resize=self.img_sz)
            # Construct a numpy array from the stream
        data = np.fromstring(self._stream.getvalue(), dtype=np.uint8)
        # "Decode" the image from the array, preserving colour
        self._current_image = cv2.imdecode(data, 1)
        cv2.imwrite(self.img_path,self._current_image)
    
    def run(self):
        self.running = True
        while self.running:
            self._get_image()
            self._calculate_motion()
            time.sleep(self.delay)
        

