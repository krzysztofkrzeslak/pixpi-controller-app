from board import PiXPiBoard as Board
from pin import Pin
import time


class Buzzer:
    def __init__(self):
        self.pin = Pin(Board.BUZZ_PIN)

    def execWarningSound(self):
        self.pin.data(1)
        time.sleep(0.2)
        self.pin.data(0)
        time.sleep(0.4)
        self.pin.data(1)
        time.sleep(0.4)
        self.pin.data(0)
        time.sleep(0.4)
        self.pin.data(1)
        time.sleep(0.6)
        self.pin.data(0)
        time.sleep(0.4)

    def serverReadySound(self):
        for i in range(1,6):
            self.pin.data(1)
            time.sleep(0.1)
            self.pin.data(0)
            time.sleep(0.1)
