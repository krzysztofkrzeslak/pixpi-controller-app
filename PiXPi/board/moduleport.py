from pin import Pin
import time
import threading
from multiprocessing import Process


class ModulePort:
    def __init__(self,powerDrivePin,IOPin,ledPin,powerDriveMode=False):
        self.powerDrivePin = powerDrivePin
        self.powerDriveMode = powerDriveMode
        if(powerDriveMode==False):
            self.powerUp()
        self.IOPin = IOPin
        self.ledPin = ledPin
        self.function = "out"
        self.defaultState = "low"


    def powerUp(self):
        self.powerDrivePin.setHighState()

    def powerDown(self):
        self.powerDrivePin.setLowState()

    def setFunction(self,function="out"):
        #set function for control(IO) Pin
        self.function = function
        if(function=="out"):
            self.IOPin.setDirection(Pin.DIR_OUT)
        elif(function=="in"):
            self.IOPin.setDirection(Pin.DIR_IN)

    def getFunction(self):
        return self.function

    def setPowerDriveMode(self, powerDriveMode):
        self.powerDriveMode = powerDriveMode
        if(powerDriveMode==True):
            self.powerDrivePin.data(0)
        else:
            self.powerDrivePin.data(1)


    def setDefaultState(self, defaultState=None):
        if(defaultState!=None):
            self.defaultState = defaultState
        if(self.function == "out"):
            if(self.defaultState=="high"):
                self.write(Pin.HIGH_STATE)
            elif(self.defaultState=="low"):
                self.write(Pin.LOW_STATE)

    def getDefaultState(self):
        defaultState = self.IOPin.defaultState
        if(defaultState==Pin.HIGH_STATE):
            return "high"
        elif(defaultState==Pin.LOW_STATE):
            return "low"

    def write(self,state):
        if(self.function=="in"):
            print "Warning:writing data to port pin initialized as input"
        else:
            self.ledPin.data(state)
        if(self.powerDriveMode==True):
            self.powerDrivePin.data(state)
        else:
            self.IOPin.data(state)

    def read(self):
        if(self.function=="out"):
            print "Warning:reading port pin initialized as output"
        return self.IOPin.data()

    def pulse(self, timeMsHigh, timeMsLow, cycles):
        timeSecHigh = timeMsHigh*0.001
        timeSecLow = timeMsLow*0.001
        for count in range(0,cycles):
            start = time.time()
            self.IOPin.data(1)
            time.sleep(timeSecHigh-((time.time()-start)+0.000150))
            start = time.time()
            self.IOPin.data(0)
            time.sleep( timeSecLow-((time.time()-start)+0.000150) )
        self.setDefaultState()

    def pulseProcess(self, timeMsHigh, timeMsLow, cycles, daemon=True):
        pulseProcess = Process(target = self.pulse, args=(timeMsHigh, timeMsLow, cycles, ))
        pulseProcess.start()
        if not daemon:
            pulseProcess.join()

    def pulseThreaded(self, timeMsHigh, timeMsLow, cycles):
        #pulseProcess = Process(target = self.pulse, args=(timeMsHigh, timeMsLow, cycles, ))
        pulseThread = threading.Thread(target = self.pulse, args=(timeMsHigh, timeMsLow, cycles,))

from onewire.master import UART_Adapter
from onewire.device import AddressableModule
from onewire.exceptions import OneWireException
from lowlevel import gpio

class ModuleComPort(ModulePort):
    def __init__(self,powerDrivePin,IOPin,paraPin,ledPin):
        self.paraPin = paraPin
        ModulePort.__init__(self, powerDrivePin, IOPin, ledPin)

    def setFunction(self,function="out"):
        if hasattr(self, 'bus'):
            self.bus.close()

        if(function == "in"):
            self.IOPin.setDirection(Pin.DIR_IN)
            self.paraPin.setDirection(Pin.DIR_OUT)
            self.paraPin.data(1)
        elif(function=="out"):
            self.IOPin.setDirection(Pin.DIR_OUT)
            self.paraPin.setDirection(Pin.DIR_OUT)
            self.paraPin.data(1)
        elif(function=="com"):
            gpio.setupPeriphial("UART0")
            #self.bus.close()
            self.bus = UART_Adapter('/dev/ttyS0')
            try:
                self.adrModule = AddressableModule(self.bus)
            except:
                print 'error initializing, none devices detected'
                self.bus.close()


        self.function = function

    def getConnectedRoms(self):
        if(self.function=="com"):
            try:
                 connectedRoms=self.adrModule.get_connected_ROMs()
                 return connectedRoms
            except :
                print 'Error fetching roms, None onewire devices detected'
                self.bus.close()
                return []
        else:
            print "port not initialized as communication port"

    def writeCommand(self,command_code):
        responseCode = self.adrModule.send_command(command_code)
        print("driver respone: "+str(responseCode))
