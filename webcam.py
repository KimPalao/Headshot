# import the necessary packages
from collections import Callable
from threading import Thread
import cv2
from imutils.video import WebcamVideoStream


class Facecam(WebcamVideoStream):
    on_face_move: Callable = None

    def __init__(self, face_cascade, *args):
        self.face_cascade = face_cascade
        super().__init__(*args)

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()
            self.frame = cv2.flip(self.frame, -1)
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                self.on_face_move(x, y, w, h)

    def start(self):
        t = Thread(target=self.update, name=self.name, args=())
        t.daemon = True
        t.start()
        return self

