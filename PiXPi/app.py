import pixpi
import time

import bottle
import apiHandlers

API_PORT=8000

app = application = bottle.default_app()

if __name__ == '__main__':

    pixpi.setup()
    print("Pixel PI App starting on port: "+str(API_PORT))
    pixpi.buzzer.serverReadySound()
    pixpi.statusLed.data(1)

    bottle.run(host = '192.168.61.1', server='rocket', port = API_PORT)
    pixpi.statusLed.data(0)
