from board import PiXPiBoard as Board
from board import CameraPort
from board import FlashPort
from board import ModulePort,ModuleComPort
from board import Buzzer
from board import Pin

from multiprocessing import Process
import os
import signal
import time

#from workerfuns import *

workerProcess = None
workerKilledFlag = 0


camera=None
flash=None
portRed=None
portGreen=None
PortBlue=None

def setup():
	vcBoardLed = Pin(44)
	vcBoardLed.setLowState()
	global camera
	camera = CameraPort( Pin(Board.FOCUS_PIN), Pin(Board.SHUTTER_PIN))
	global flash1
	flash1  = FlashPort( Pin(Board.FLASH1_PIN) )
	global flash2
	flash2  = FlashPort( Pin(Board.FLASH2_PIN) )

    #by default ports io are set as output
	global portRed
	portRed= ModuleComPort( Pin(Board.PORT_RED_PW), Pin(Board.PORT_RED_IO), Pin(Board.PORT_RED_PARA), Pin(Board.PORT_RED_LED))

	global portGreen
	portGreen = ModulePort( Pin(Board.PORT_GREEN_PW), Pin(Board.PORT_GREEN_IO), Pin(Board.PORT_GREEN_LED))

	global portBlue
	portBlue = ModulePort( Pin(Board.PORT_BLUE_PW), Pin(Board.PORT_BLUE_IO), Pin(Board.PORT_BLUE_LED))

	global statusLed
	statusLed=Pin(Board.LED_PIN)

	global buzzer
	buzzer=Buzzer()


def worker(bytecode):
	global workerProcess
	print("started process with pid: "+str(workerProcess.pid))
	exec(bytecode)

def startWorker(scriptContent):
	global workerProcess
	global workerKilledFlag

	if not isWorkerRunning():
		try:
			bytecode = compile(scriptContent,'','exec')
		except:
			return {"status":"compilation_error"}


		workerProcess = Process(target = worker, args=(bytecode, ))
		
		buzzer.execWarningSound()
		workerProcess.start()
		workerProcess.join()

		portRed.setDefaultState()
		portGreen.setDefaultState()
		portBlue.setDefaultState()

		if not workerKilledFlag:
			return {"status":"completed"}
		else:
			workerKilledFlag=0
			return {"status":"killed"}
	else:
		return {"status":"busy"}

def killWorker():
	global workerProcess
	global workerKilledFlag
	if (workerProcess is not None) and workerProcess.is_alive():
		workerProcess.terminate()
		time.sleep(0.001)
		if workerProcess.is_alive():
			pid=workerProcess.pid
			#jokes are over :P
			os.kill(pid, signal.SIGKILL)
			time.sleep(0.001)

		print("process should be terminated now,is alive: "+str(workerProcess.is_alive()))
	else:
		print("process is not running")


def isWorkerRunning():
	global workerProcess

	if workerProcess is not None:
		if workerProcess.is_alive():
			return 1
	return 0
