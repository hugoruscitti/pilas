# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import dispatch

mueve_camara = dispatch.Signal(providing_args=['x', 'y', 'dx', 'dy'])
mueve_mouse = dispatch.Signal(providing_args=['x', 'y', 'dx', 'dy'])
click_de_mouse = dispatch.Signal(providing_args=['button', 'x', 'y'])
termina_click = dispatch.Signal(providing_args=['button', 'x', 'y'])
mueve_rueda = dispatch.Signal(providing_args=['delta'])
pulsa_tecla = dispatch.Signal(providing_args=['codigo', 'texto'])
suelta_tecla = dispatch.Signal(providing_args=['codigo', 'texto'])
pulsa_tecla_escape = dispatch.Signal(providing_args=[])
actualizar = dispatch.Signal(providing_args=[])
actualizar_pausado = dispatch.Signal(providing_args=[])
post_dibujar = dispatch.Signal(providing_args=[])

# Se emite cuando el mundo ingresa o sale del modo depuracion (pulsando F12)
inicia_modo_depuracion = dispatch.Signal(providing_args=[]) 
sale_modo_depuracion = dispatch.Signal(providing_args=[])
actualiza_modo_depuracion = dispatch.Signal(providing_args=[])


def imprimir_todos():
    "Muestra en consola los eventos activos y a quienes invocan"
    imprime_alguno = False
    
    for x in globals().items():
        nombre = x[0]
        evento = x[1]
        
        if isinstance(evento, dispatch.Signal):
            if evento.esta_conectado():
                imprime_alguno = True
                print "%s:" %(nombre)
                evento.imprimir_funciones_conectadas()
                
    if not imprime_alguno:
        print "Ningun evento esta conectado."
