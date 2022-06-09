"""
Module responsible for getting data from sensors.
"""
from typing import Tuple, Any, List
import cv2
import threading
import queue


# bufferless VideoCapture
class VideoCapture:

    def __init__(self, name):
        self.cap = cv2.VideoCapture(name)
        self.q = queue.Queue()
        t = threading.Thread(target=self._reader)
        t.daemon = True
        t.start()

    # read frames as soon as they are available, keeping only most recent one
    def _reader(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            if not self.q.empty():
                try:
                    self.q.get_nowait()  # discard previous (unprocessed) frame
                except queue.Empty:
                    pass
            self.q.put(frame)

    def read(self):
        return self.q.get()

    def release(self):
        self.cap.release()


class Camera:
    def __init__(self, camera_source: int):
        """
        Init camera.
        :param camera_source: Camera source number
        """
        self.cap = VideoCapture(camera_source)

    def get_data_from_camera(self) -> Tuple[Any, List]:
        """
            Get frame from the camera.
            :param: None
            :return: Frame with image from the camera and a flag indicating successfully acquisition
        """

        # Capture frame-by-frame
        frame = self.cap.read()

        return frame

    def kill_camera(self) -> None:
        """
        Deinitialize the camera.
        :param: None
        :return: None
        """
        self.cap.release()
        cv2.destroyAllWindows()
