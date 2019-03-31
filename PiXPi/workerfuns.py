import time
#import pixpi


def rdyLed(value):
	gpio.data(gpio.LED_PIN,value)

def delay(miliseconds):
	time.sleep( (miliseconds*0.001) )

def flash():
	print("flash")
	#pixpi.flash.trigger()

def cam_trigger_focus():
	gpio.data(gpio.FOCUS_PIN,gpio.HIGH_STATE)

def cam_trigger_shutter():
	gpio.data(gpio.FOCUS_PIN,gpio.HIGH_STATE)
	gpio.data(gpio.SHUTTER_PIN,gpio.HIGH_STATE)

def cam_fire():
	cam_trigger_focus()
	cam_trigger_shutter()

def cam_trigger_release():
	gpio.data(gpio.SHUTTER_PIN,gpio.LOW_STATE)
	gpio.data(gpio.FOCUS_PIN,gpio.LOW_STATE)

def setChannel(channel,value):
	gpio.data(channel,value)
