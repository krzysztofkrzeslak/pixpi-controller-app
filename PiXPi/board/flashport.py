import time

class FlashPort:
    def __init__(self,flashPin):
        self.flashPin = flashPin

    def trigger(self):
        self.flashPin.setHighState()
        print('flash')
        time.sleep(0.001)
        self.flashPin.setLowState()
