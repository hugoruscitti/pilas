# -*- encoding: utf-8 -*-
# For pilas engine - a video game framework.
#
# copyright 2010 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas

class EscenaMenu(pilas.escenas.Escena):
    "Escena de presentacion del juego."

    def __init__(self):
        pilas.actores.utils.eliminar_a_todos()
        pilas.fondos.Fondo('data/menu.png')
        self.titulo_de_juego()
        self.menu_de_juego()

    def titulo_de_juego(self):
        titulo = pilas.actores.Actor('data/titulo.png')
        
        titulo.y = 250

        titulo.y = pilas.interpolar(170, 1.5)

    def menu_de_juego(self):
        
        opcion = pilas.actores.Actor('data/opcion.png')
        opcion.x = 133
        opcion.y = 23
        
        # boton inicio
        def presionamos_boton_inicio():
            self.iniciar_juego()
        
        def sobre_boton_inicio():
            self.boton_inicio.pintar_sobre()
            opcion.y = 23
            
            
        
        self.boton_inicio = pilas.actores.Boton(-550, 20, 'data/b_inicio.png', 'data/b_inicio_over.png','data/b_inicio_over.png')
        
        self.boton_inicio.conectar_presionado(presionamos_boton_inicio)
        self.boton_inicio.conectar_sobre(sobre_boton_inicio)
        self.boton_inicio.conectar_normal(self.boton_inicio.pintar_normal)
        
        self.boton_inicio.x = [-130]
        
        # boton ayuda
        def presionamos_boton_ayuda():
            self.mostrar_ayuda()
        
        def sobre_boton_ayuda():
            opcion.y = -52
            self.boton_ayuda.pintar_sobre()
        
        self.boton_ayuda = pilas.actores.Boton(-550, -53, 'data/b_ayuda.png', 'data/b_ayuda_over.png','data/b_ayuda_over.png')
        
        self.boton_ayuda.conectar_presionado(presionamos_boton_ayuda)
        self.boton_ayuda.conectar_sobre(sobre_boton_ayuda)
        self.boton_ayuda.conectar_normal(self.boton_ayuda.pintar_normal)
        
        self.boton_ayuda.x = [-130]
        
        # boton salir
        def presionamos_boton_salir():
            self.salir_del_juego()
        
        def sobre_boton_salir():
            opcion.y = -121
            self.boton_salir.pintar_sobre()

        self.boton_salir = pilas.actores.Boton(-550, -126, 'data/b_salir.png', 'data/b_salir_over.png','data/b_salir_over.png')
        
        self.boton_salir.conectar_presionado(presionamos_boton_salir)
        self.boton_salir.conectar_sobre(sobre_boton_salir)
        self.boton_salir.conectar_normal(self.boton_salir.pintar_normal)
        
        self.boton_salir.x = [-130]

        
    def desactivar_botones(self):
        self.boton_inicio.desactivar()
        self.boton_ayuda.desactivar()
        self.boton_salir.desactivar()

            
    def iniciar_juego(self):
        import escena_juego
        escena_juego.Juego()
        self.desactivar_botones()


    def salir_del_juego(self):
        pilas.terminar()

    def mostrar_ayuda(self):
        import escena_ayuda
        escena_ayuda.Ayuda()
