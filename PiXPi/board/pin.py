from lowlevel import gpio


class Pin:

    DIR_OUT=1
    DIR_IN=0

    HIGH_STATE = 1
    LOW_STATE = 0

    def __init__(self, gpioNumber, direction=1):
        self.num = gpioNumber
        self.dir = direction
        self.state=0
        gpio.setup(self.num,self.dir);
        gpio.data(self.num, self.state);

    def setDirection(self, direction):
        self.dir=direction
        gpio.setup(self.num,self.dir)

    def configAsInput(self):
        self.dir=Pin.DIR_IN
        self.setDirection(self.dir)

    def configAsOutput(self):
        self.dir=Pin.DIR_OUT
        self.setDirection(self.dir)

    def setHighState(self):
        self.state=Pin.HIGH_STATE
        gpio.data(self.num,self.state)

    def setLowState(self):
        self.state=Pin.LOW_STATE
        gpio.data(self.num,self.state)


    def data(self, state=-1):
        self.state=state
        ##reading data mode
        if(state==-1):
            if(self.dir==Pin.DIR_OUT):
                print("do you really want to read data from output pin ?")
            return gpio.data(self.num)
        else:
            gpio.data(self.num,self.state)
