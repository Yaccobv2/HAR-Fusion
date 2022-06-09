"""
Module responsible for communication wit smartband.
"""
from __future__ import annotations

from typing import Dict
import threading
import time
import ctypes
from bluepy.btle import BTLEDisconnectError

from src.miband import miband


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(StoppableThread, self).__init__(*args, **kwargs)
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

class Smartband:
    def __init__(self, file: str = "miband_data.txt"):
        self.output = []
        self.file = file
        self.mac_adress = None
        self.auth_key = None
        self.get_mac_and_auth_key()
        self.band = None
        self.thread = None
        self.init_smartband()

    def init_smartband(self):
        success = False
        while not success:
            try:
                self.band = miband(self.mac_adress, self.auth_key, debug=True)
                success = self.band.initialize()
            except BTLEDisconnectError:
                print('Connection to the MIBand failed. Trying out again in 3 seconds')
                print("Press any key to stop")
                time.sleep(3)
                continue
            except KeyboardInterrupt:
                print("\nExit.")
                exit()

    def get_mac_and_auth_key(self) -> None:
        try:
            with open(self.file, "r") as f:
                self.mac_adress = f.readline().strip()
                self.auth_key = f.readline().strip()

        except FileNotFoundError:
            self.mac_adress = None
            self.auth_key = None
            print("Error:")
            print("  Please specify MAC address and auth key of the MiBand")
            print("  Put your MAC to the first line of 'miband_data.txt' file")
            print("  Put your auth key to the second line of 'miband_data.txt' file")
            exit(1)

        if self.mac_adress:
            # Validate MAC address
            if 1 < len(self.mac_adress) != 17:
                print("Error:")
                print("  Your MAC length is not 17, please check the format")
                print("  Example of the MAC: a1:c2:3d:4e:f5:6a")
                exit(1)

        if self.auth_key:
            if 1 < len(self.auth_key) != 32:
                print("Error:")
                print("  Your AUTH KEY length is not 32, please check the format")
                print("  Example of the Auth Key: 8fa9b42078627a654d22beff985655db")
                exit(1)

        # Convert Auth Key from hex to byte format
        self.auth_key = bytes.fromhex(self.auth_key)


    def gyro_callback(self, data: Dict) -> None:
        self.output.append(data)
        # print('Realtime gyro', data)

    def start_gyroscope(self) -> None:
        try:
            self.thread = StoppableThread(target=self.band.start_accel_realtime, args=(self.gyro_callback,))
            self.thread.daemon = True
            self.thread.start()
        except RuntimeError:
            print("Can't create new accelerometer thread ")

    def stop_gyroscope(self) -> None:
        self.thread.stop()
        self.thread.join()

    def get_gyro_data(self) -> Dict | None:
        if len(self.output) == 0:
            return None
        if len(self.output) < 2:
            data = self.output.pop(0)
            return data
        if len(self.output) > 2:
            data = self.output.pop()
            self.output.clear()
            return data
