# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import SocketServer



def iniciar_servidor():


    class EchoRequestHandler(SocketServer.BaseRequestHandler ):
        def setup(self):
            print self.client_address, 'connected!'
            self.request.send('hi ' + str(self.client_address) + '\n')

        def handle(self):
            data = 'dummy'
            while data:
                data = self.request.recv(1024)
                print "ha llegado el mensaje:", data
                self.request.send(data)
                
                if data.strip() == 'bye':
                    return

        def finish(self):
            print self.client_address, 'disconnected!'
            self.request.send('bye ' + str(self.client_address) + '\n')


    #server host is a tuple ('host', port)
    puerto = 50008
    print "iniciando el modo servidor en el puerto %d" %(puerto)

    servidor = SocketServer.ThreadingTCPServer(('', puerto), EchoRequestHandler)
    servidor.serve_forever()
