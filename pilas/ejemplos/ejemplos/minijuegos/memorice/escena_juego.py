# -*- encoding: utf-8 -*-
# For pilas engine - a video game framework.
#
# copyright 2011 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from random import random

class puntuacion:
    p = 0

class Juego(pilas.escena.Base):
    "Escena que Controla el juego"

    def __init__(self, nivel):
        pilas.escena.Base.__init__(self)
        self.nivel = nivel
    
    def iniciar(self):
        puntuacion.p = 0 
        self.iniciar_juego(self.nivel)
    
    def iniciar_juego(self, nivel):
        pilas.actores.utils.eliminar_a_todos()
        pilas.fondos.Fondo('data/fondo.png')

        if nivel == 1:
            self.pos_iniciar = [-35, -35]
            self.filas = 2
            self.columnas = 2
            self.espaciado = 30
            self.pares = 2
            self.agregar_puntaje = 5
            self.restar_puntaje = 1

        elif nivel == 2:
            self.pos_iniciar = [-50, -35]
            self.filas = 3
            self.columnas = 2
            self.espaciado = 15
            self.pares = 3
            self.agregar_puntaje = 10
            self.restar_puntaje = 2

        elif nivel == 3:
            self.pos_iniciar = [-78, -65]
            self.filas = 4
            self.columnas = 3
            self.espaciado = 15
            self.pares = 6
            self.agregar_puntaje = 15
            self.restar_puntaje = 3

        elif nivel == 4:
            self.pos_iniciar = [-70, -85]
            self.filas = 4
            self.columnas = 4
            self.espaciado = 10
            self.pares = 8
            self.agregar_puntaje = 20
            self.restar_puntaje = 4

        elif nivel == 5:
            self.pos_iniciar = [-93, -85]
            self.filas = 5
            self.columnas = 4
            self.espaciado = 10
            self.pares = 10
            self.agregar_puntaje = 25
            self.restar_puntaje = 5

        elif nivel == 6:
            self.pos_iniciar = [-118, -85]
            self.filas = 6
            self.columnas = 4
            self.espaciado = 10
            self.pares = 12
            self.agregar_puntaje = 30
            self.restar_puntaje = 5
            
        elif nivel == 7:
            self.pos_iniciar = [-105, -155]
            self.filas = 6
            self.columnas = 6
            self.espaciado = 5
            self.pares = 18
            self.agregar_puntaje = 35
            self.restar_puntaje = 6
  
        elif nivel == 8:
            self.pos_iniciar = [-130, -150]
            self.filas = 7
            self.columnas = 6
            self.espaciado = 5
            self.pares = 21
            self.agregar_puntaje = 100
            self.restar_puntaje = 7
         
        self.pulsa_tecla_escape.conectar(self.cuando_se_presione_escape)
        
        
        self.crear_puntaje()
        self.crear_nivel(nivel)
        self.crear_parejas()

        self.nivel = nivel
        self.estado = True

        self.tiempo = 0.5
        
        self.area = self.columnas * self.filas

        self.intentos = []
        self.cantidad_de_pares = 0

        self.array_caracteres = self.generar_array_caracteres()
        
        self.fabricar_botones_personalizados()
        self.configurar_botones()


    def cambiar_nivel(self, nivel):
        self.nivel = nivel
        self.iniciar_juego(self.nivel)
            
    def fabricar_botones_personalizados(self):
        self.botones = pilas.atajos.fabricar(boton_personalizado, self.area, False)

    def cuando_se_presione_escape(self, *k, **kv):
        "Regresa al menu principal"
        from . import escena_menu
        pilas.cambiar_escena(escena_menu.EscenaMenu())


    def crear_puntaje(self):
        self.puntaje = pilas.actores.Puntaje()
        self.puntaje.definir(puntuacion.p)
        self.puntaje.x = -200
        self.puntaje.y = 55
        self.puntaje.magnitud = 18
        
    def crear_parejas(self):
        self.parejas = pilas.actores.Puntaje()
        self.parejas.definir(0)
        self.parejas.x = -200
        self.parejas.y = 17
        self.parejas.magnitud = 18
       
    def crear_nivel(self, nivel):
        self.nivel_texto = pilas.actores.Puntaje()
        self.nivel_texto.x = -200
        self.nivel_texto.y = 93
        self.nivel_texto.magnitud = 18
        self.nivel_texto.definir(nivel)

        


    def generar_array_caracteres(self):
        # lista con caracteres

        # lista con caracteres aleatorios
        caracteres_aleatorios = []
        for c_a in range(self.area):
            caracteres_aleatorios.append("null")

        # lista con letras 
        l = []
        for c in "abcdefghijklmnopqrstu":
            l.append(c)
        
        

        # creamos una lista 'caracteres_aleatorios' con letras
        # desordenadas
    
        caracteres = []
        limite = 0
        limite = self.pares


        for i in range(limite):
            caracteres.append(l[i])
            caracteres.append(l[i] + '2')


        for i in range(self.area):
            ocupado = True
            while ocupado:
                rand_i = int(random() * self.area)
                if caracteres_aleatorios[rand_i] == "null":
                    caracteres_aleatorios[rand_i] = caracteres[i]
                    ocupado = False

        return caracteres_aleatorios

        
        

    def pintar_boton_x(self, n):
        if self.estado == True:
            if n.primera_vez_presionado == False:
            
                for c in 'abcdefghijklmnopqrstu':
                    if n.apariencia == c:
                        self.intentos.append([c, 1])                    
                        n.boton.pintar_presionado(c + '.png')  

                    if n.apariencia == c + '2':
                        self.intentos.append([c, 2])
                        n.boton.pintar_presionado(c + '.png')               
                
        
            n.primera_vez_presionado = True

    def termino_juego(self):
        self.termino = pilas.actores.Actor("termino.png")
        self.termino.y = 300
        self.termino.y = pilas.interpolar(0, 2)

        self.p = pilas.actores.Puntaje()
        self.p.definir(puntuacion.p)
        
        self.p.y = 280
        self.p.x = -10
        self.p.y = pilas.interpolar(-20, 2)
        
        self.estado = False

    
    def analizar_pares(self):

        def aumentar_pares():
            self.cantidad_de_pares += 1
            self.parejas.definir(self.cantidad_de_pares)
            puntuacion.p += self.agregar_puntaje
            self.puntaje.definir(puntuacion.p)

        def borrar_ficha_x(ficha_x, ficha_x2):
            ficha_x.boton.eliminar()
            ficha_x.boton.desactivar()

            ficha_x2.boton.eliminar()
            ficha_x2.boton.desactivar()
            aumentar_pares()

            if self.cantidad_de_pares == self.pares:

                self.nivel += 1
                if self.nivel > 8:
                    self.termino_juego()
                else:
                    self.cambiar_nivel(self.nivel)                
            self.estado = True

        def encontrar_boton_x(c):
            x = 0
            for i in self.array_caracteres:
                if self.botones[x].apariencia == c:
                   return self.botones[x]
                x += 1
            
        
        if (len(self.intentos))  == 2:
            # si son pares
            if self.intentos[0][0] == self.intentos[1][0]:
                if self.estado == True:
                    for c in 'abcdefghijklmnopqrstu': 
                        if self.intentos[0][0] == c: 
                            boton_x = encontrar_boton_x(c)
                            boton_x2 = encontrar_boton_x(c + '2')
                            pilas.mundo.agregar_tarea_una_vez(self.tiempo, borrar_ficha_x, boton_x, boton_x2)

                self.estado = False
            else:
            # si no son pares

                puntuacion.p -= self.restar_puntaje
                self.puntaje.definir(puntuacion.p)

                def pintar_normal_ficha_x(n):
                    n.boton.pintar_normal()
                    self.estado = True

                for i in range(self.area):
                    self.botones[i].primera_vez_presionado = False
                    self.estado = False
                    pilas.mundo.agregar_tarea_una_vez(self.tiempo, pintar_normal_ficha_x, self.botones[i])
                
            self.intentos.pop()
            self.intentos.pop()

    def configurar_botones(self):
        x = 0

        for i in range(self.columnas):
            for j in range(self.filas):        
                
                self.botones[x].boton.x = self.pos_iniciar[0] 
                self.botones[x].boton.y = self.pos_iniciar[1]

                # posicionamos botones en filas y columnas
                self.botones[x].boton.x += (self.botones[x].boton.obtener_ancho() + self.espaciado) * j     
                self.botones[x].boton.y += (self.botones[x].boton.obtener_alto() + self.espaciado) * i 

                # agregamos identidad al boton
                self.botones[x].apariencia = self.array_caracteres[x] 
       
                # conectamos funcion
                self.botones[x].boton.conectar_presionado(self.pintar_boton_x, self.botones[x])
                self.botones[x].boton.conectar_presionado(self.analizar_pares)

                x += 1    


class boton_personalizado:
    def __init__(self, x = 0, y = 0):

        ruta_normal = "casilla.png"        

        self.boton = pilas.actores.Boton(x, y, ruta_normal)
        self.apariencia = 'null'
        self.primera_vez_presionado = False
