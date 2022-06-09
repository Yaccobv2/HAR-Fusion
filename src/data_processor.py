"""
Module responsible for getting data from sensors.
"""

from typing import Tuple, List, Any, Union
import cv2
import sys

from src.camera import Camera
from src.smatband import Smartband
from src.dataset_maker import save_data


def main_loop(camera_source: int = 1, mode: str = "run", class_name: str = "None", frames_num: int = 20) -> None:
    """
        Start getting data from sesors. You can break it using "q" key.
        :param frames:
        :param class_name:
        :param mode:
        :param camera_source:
        :return: None
    """
    cam = Camera(camera_source)
    smartband = Smartband()
    smartband.start_gyroscope()

    if mode == "run":
        while True:

            gyroscope_data = smartband.get_gyro_data()
            if gyroscope_data:
                # Capture frame-by-frame
                frame = cam.get_data_from_camera()
                print(gyroscope_data)
                cv2.imshow("frame", frame)

            # break the loop
            pressed_key = cv2.waitKey(1) & 0xFF
            if pressed_key & 0xFF == ord('q'):
                break

    if mode == "dataset":
        frames = []
        gyro_data = []
        while len(frames) != frames_num:
            gyroscope_data = smartband.get_gyro_data()
            if gyroscope_data:
                # Capture frame-by-frame
                frame = cam.get_data_from_camera()
                print(gyroscope_data)
                gyro_data.append(gyroscope_data)
                frames.append(frame)
                cv2.imshow("frame", frame)

            # break the loop
            pressed_key = cv2.waitKey(1) & 0xFF
            if pressed_key & 0xFF == ord('q'):
                break

        if len(frames) == frames_num:
            save_data(class_name=class_name, frames=frames, gyro_data=gyro_data)

    cam.kill_camera()
    # smartband.stop_gyroscope()
    sys.exit()

if __name__ == "__main__":
    main_loop(camera_source=1)
