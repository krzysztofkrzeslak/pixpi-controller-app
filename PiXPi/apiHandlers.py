import pixpi

from bottle import request, response
from bottle import post, get, put, delete
import json

@post('/api/worker/run')
def postWorkerExec():
    requestData=json.load(request.body)

    scriptContent = requestData["script_content"]
    status = pixpi.startWorker(scriptContent)

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(status)

@post('/api/worker/kill')
def postWorkerStop():
    pixpi.killWorker()

    response.headers['Content-Type'] = 'application/json'
    return json.dumps({"worker running":pixpi.isWorkerRunning()})

@get('/api/worker/status')
def getWorkerStatus():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({"worker running":pixpi.isWorkerRunning()})

@post('/api/ports/config')
def postPortsConfig():
    portConfJson = request.body
    portConf=json.load(portConfJson)

    print(portConf)

    responseBody = portConf

    #port red configuration, it`s more complicated due it can serve as input,output or communication port
    if 'portRed' in portConf:
        portRedConf = portConf['portRed']
        if(portRedConf['function'] == 'out'):
            pixpi.portRed.setFunction('out')
            if(portRedConf['defaultState']):
                pixpi.portRed.setDefaultState(portRedConf['defaultState'])
                responseBody['portRed']={'defaultState':pixpi.portRed.read()}
        elif(portRedConf['function'] == 'in'):
            pixpi.portRed.setFunction('in')
	elif(portRedConf['function'] == 'step'):
            pixpi.portRed.setFunction('out')
        elif(portRedConf['function'] == 'com'):
            pixpi.portRed.setFunction(portRedConf['function'])
            responseBody['portRed']={'roms':pixpi.portRed.getConnectedRoms()}
    #port green config as input/output
    if 'portGreen' in portConf:
	if(portConf['portGreen']['function'] == 'step'):
            pixpi.portRed.setFunction('out')
	else:
	    pixpi.portGreen.setFunction(portConf['portGreen']['function'])
            if('defaultState' in portConf['portGreen']):
            	pixpi.portGreen.setDefaultState(portConf['portGreen']['defaultState'])


    #port blue config as input/output
    if 'portBlue' in portConf:
        if(portConf['portBlue']['function'] == 'step'):
            pixpi.portBlue.setFunction('out')
        else:
            pixpi.portBlue.setFunction(portConf['portBlue']['function'])
            if('defaultState' in portConf['portBlue']):
                 pixpi.portBlue.setDefaultState(portConf['portBlue']['defaultState'])

        responseBody['portBlue']={'state':pixpi.portBlue.read()}

    response.headers['Content-Type'] = 'application/json'

    return json.dumps(responseBody)

@get('/api/ports/config')
def getPortsConfig():
    responseJson={}

    responseJson['portRed']={'function':pixpi.portRed.function}
    if(responseJson['portRed']['function']=='out'):
        responseJson['portRed']['defaultState']=pixpi.portRed.getDefaultState()
    elif(responseJson['portRed']['function']=='com'):
        pass

    responseJson['portGreen']={'function':pixpi.portGreen.function}
    if(responseJson['portGreen']['function']=='out'):
        responseJson['portGreen']['defaultState']=pixpi.portGreen.getDefaultState()

    responseJson['portBlue']={'function':pixpi.portBlue.function}
    if(responseJson['portBlue']['function']=='out'):
        responseJson['portBlue']['defaultState']=pixpi.portBlue.getDefaultState()

    response.headers['Content-Type'] = 'application/json'
    return json.dumps(responseJson)

@get('/api/device/info')
def getStatus():
    response.headers['Content-Type'] = 'application/json'
    return json.dumps({"software_version":pixpi.software_version,
                       "worker running":pixpi.isWorkerRunning()})
