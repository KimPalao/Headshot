# import the necessary packages
import cv2 as cv

from collections import Callable
from threading import Thread

from imutils.video import WebcamVideoStream
from .event_widget import EventWidget


class Facecam(WebcamVideoStream, EventWidget):
    _on_face_move: Callable = None
    thread: Thread = None

    def __init__(self, face_cascade=None, detector=None, src=0, *args):
        self.face_cascade = face_cascade
        self.detector = detector
        super().__init__(src=src, *args)

    def update(self):
        while True:
            if self.stopped:
                return

            (self.grabbed, self.frame) = self.stream.read()
            # self.frame = cv.flip(self.frame, -1)
            gray = cv.cvtColor(self.frame, cv.COLOR_BGR2GRAY)  # Convert to grayscale
            if self.face_cascade:  # If using OpenCV's Haar cascade
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5, flags=cv.CASCADE_SCALE_IMAGE)
                for (x, y, w, h) in faces:
                    cv.rectangle(self.frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    if self._on_face_move:
                        self._on_face_move(x, y, w, h)

    def start(self):
        self.thread = Thread(target=self.update, name=self.name, args=())
        self.thread.daemon = True
        self.thread.start()
        return self

    def _on_face_move_base(self, x: int, y: int, w: int, h: int) -> None:
        """
        A placeholder function that will be called when the button is clicked.
        :param x:
        :param y:
        :param w:
        :param h:
        """
        pass

    @property
    def on_face_move(self):
        """
        Returns the event handler for mouse presses
        :return: Callable
        """
        if self._on_face_move:
            return self._on_face_move
        return self._on_face_move_base

    @on_face_move.setter
    def on_face_move(self, func):
        self._on_face_move = func

    def __del__(self):
        self.stop()
        self.stream.release()

    def clean(self):
        self.stop()
        self.stream.release()
        del self
