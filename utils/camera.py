import cv2
import threading
from threading import RLock
from typing import Union

class CameraStream:

    def __init__(self, device: str = "/dev/video0") -> None:
        self.device = device
        self.lock = RLock()
        self.is_stop = True
        self.cap = cv2.VideoCapture(self.device)
        self.t: threading.Thread = threading.Thread(target=self._read_camera, daemon=True)

    def start(self):
        self.is_stop = False
        self.t.start()
        
    def _update_frame(self, frame):
        self.lock.acquire()
        self.frame = frame
        self.lock.release()

    def _read_camera(self):
        while(not self.is_stop):
            ret, frame = self.cap.read()
            if not ret:
                break
            self._update_frame(frame)
        self.cap.release()

    def _close(self):
        self.is_stop = True

    def read(self):
        return self.frame

    def release(self):
        self._close()

