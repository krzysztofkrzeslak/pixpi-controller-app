import time

class CameraPort:
    def __init__(self, focusPin, shutterPin):
        self.focusPin = focusPin
        self.shutterPin = shutterPin

    def focusHold(self):
        self.focusPin.setHighState()

    def shutterHold(self):
        self.shutterPin.setHighState()

    def triggerHold(self):
        # push and hold shutter button on camera does
        print('camera: trigger')
        self.focusHold()
        self.shutterHold()

    def focusRelease(self):
        self.focusPin.setLowState()

    def shutterRelease(self):
        self.shutterPin.setLowState()

    def triggerRelease(self):
        #release shutter button on camera
        print('camera: trigger release')
        self.shutterRelease()
        self.focusRelease()

    def triggerMomentary(self):
        #momentary push shutter button
        self.triggerHold()
        time.sleep(1)
        self.triggerRelease()
