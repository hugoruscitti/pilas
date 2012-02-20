# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilas.dispatch.dispatcher import Signal

class Evento(Signal):

    def __init__(self, argumentos=[]):
        Signal.__init__(self, argumentos)

    def emitir(self, emisor, **argumentos):
        return self.send(emisor, **argumentos)

    def conectar(self, receptor, emisor=None, weak=True, uid=None):
        return self.connect(receptor, emisor, weak, uid)

    def desconectar(self, receptor=None, emisor=None, weak=True, uid=None):
        self.disconnect(receptor, emisor, weak, uid)

    def esta_conectado(self):
        "Indica si tiene alguna funcion conectada."
        return len(self.receivers) > 0

    def imprimir_funciones_conectadas(self):
        "Imprime todas las funciones que tiene conectado el evento."
        for clave, referencia in self.receivers:
            nombre = referencia.__str__()
            nombre = nombre[nombre.index('(')+1:nombre.index(")")]
            print "\t", nombre

mueve_camara = Evento(['x', 'y', 'dx', 'dy'])
mueve_mouse = Evento(['x', 'y', 'dx', 'dy'])
click_de_mouse = Evento(['button', 'x', 'y'])
termina_click = Evento(['button', 'x', 'y'])
mueve_rueda = Evento(['delta'])
pulsa_tecla = Evento(['codigo', 'texto'])
suelta_tecla = Evento(['codigo', 'texto'])
pulsa_tecla_escape = Evento([])
actualizar = Evento([])
actualizar_pausado = Evento([])
post_dibujar = Evento([])

# Se emite cuando el mundo ingresa o sale del modo depuracion (pulsando F12)
inicia_modo_depuracion = Evento([]) 
sale_modo_depuracion = Evento([])
actualiza_modo_depuracion = Evento([])


def imprimir_todos():
    "Muestra en consola los eventos activos y a quienes invocan"
    imprime_alguno = False
    
    for x in globals().items():
        nombre = x[0]
        evento = x[1]
        
        if isinstance(evento, Evento):
            if evento.esta_conectado():
                imprime_alguno = True
                print "%s:" %(nombre)
                evento.imprimir_funciones_conectadas()
                
    if not imprime_alguno:
        print "Ningun evento esta conectado."
