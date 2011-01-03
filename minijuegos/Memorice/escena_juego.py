# -*- encoding: utf-8 -*-
# For pilas engine - a video game framework.
#
# copyright 2010 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from fichas import clase_fichas


class Juego(pilas.escenas.Escena):
    "Escena que Controla el juego"

    def __init__(self):        
        self.iniciar_juego()
        
    def iniciar_juego(self):
        pilas.escenas.Escena.__init__(self) 
        pilas.actores.utils.eliminar_a_todos()
        pilas.fondos.Fondo('data/fondo.png')
        pilas.eventos.pulsa_tecla_escape.conectar(self.cuando_se_presione_escape)

        self.fichas = clase_fichas()
        
        self.crear_temporizador()
        
        self.fichas.crear_fichas()
        self.fichas.ordenar_fichas()
        
        self.crear_boton_reiniciar()
        self.crear_puntaje()
        
        self.fichas.posicionar_botones_fichas()
        
        self.conectar_funciones_fichas()
        self.conectar_funciones_para_analizar_pares()
        
        self.crear_variables_para_presionar_una_vez_ficha()
        
        self.intentos = []
        self.estado = True

    def cuando_se_presione_escape(self, *k, **kv):
        "Regresa al menu principal"
        import escena_menu
        escena_menu.EscenaMenu()

    def crear_puntaje(self):
        self.puntaje = pilas.actores.Puntaje()
        self.puntaje.x = -215
        self.puntaje.y = -143
        
    def crear_boton_reiniciar(self):
        self.boton_reiniciar = pilas.actores.Boton(240, -140, 'data/reiniciar.png', 
                                                              'data/reiniciar2.png', 
                                                              'data/reiniciar2.png')
        def al_presionar_boton_reiniciar():
            self.iniciar_juego()

        self.boton_reiniciar.conectar_presionado(al_presionar_boton_reiniciar)
        self.boton_reiniciar.conectar_normal(self.boton_reiniciar.pintar_normal) 
        self.boton_reiniciar.conectar_sobre(self.boton_reiniciar.pintar_sobre)

    def crear_temporizador(self):
        def termina_juego():
            self.estado = False
            pilas.avisar("Termino el tiempo, Reincia Partida y Supera tu puntaje !")
            

        t = pilas.actores.Temporizador(0, -185)

        t.ajustar(50,termina_juego)
        
        t.iniciar()
    
    def crear_variables_para_presionar_una_vez_ficha(self):
        
        self.primera_vez_presionado_ficha_a1 = False
        self.primera_vez_presionado_ficha_b1 = False
        self.primera_vez_presionado_ficha_c1 = False
        self.primera_vez_presionado_ficha_d1 = False
        self.primera_vez_presionado_ficha_e1 = False
        self.primera_vez_presionado_ficha_f1 = False
        self.primera_vez_presionado_ficha_g1 = False
        self.primera_vez_presionado_ficha_h1 = False
        
        self.primera_vez_presionado_ficha_a2 = False
        self.primera_vez_presionado_ficha_b2 = False
        self.primera_vez_presionado_ficha_c2 = False
        self.primera_vez_presionado_ficha_d2 = False
        self.primera_vez_presionado_ficha_e2 = False
        self.primera_vez_presionado_ficha_f2 = False
        self.primera_vez_presionado_ficha_g2 = False
        self.primera_vez_presionado_ficha_h2 = False
        
        
        
    def conectar_funciones_fichas(self):
        
        # primer grupo de funciones 

        def press_ficha_a_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_a1 == False:
                    self.fichas.ficha_a.pintar_presionado()
                    self.primera_vez_presionado_ficha_a1 = True
                    self.intentos.append(['a', 1])

        def press_ficha_b_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_b1 == False:
                    self.fichas.ficha_b.pintar_presionado()
                    self.primera_vez_presionado_ficha_b1 = True
                    self.intentos.append(['b', 1])
        
        def press_ficha_c_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_c1 == False:
                    self.fichas.ficha_c.pintar_presionado()
                    self.primera_vez_presionado_ficha_c1 = True
                    self.intentos.append(['c', 1])
        
        def press_ficha_d_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_d1 == False:
                    self.fichas.ficha_d.pintar_presionado()
                    self.primera_vez_presionado_ficha_d1 = True
                    self.intentos.append(['d', 1])
        
        def press_ficha_e_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_e1 == False:
                    self.fichas.ficha_e.pintar_presionado()
                    self.primera_vez_presionado_ficha_e1 = True
                    self.intentos.append(['e', 1])
        
        def press_ficha_f_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_f1 == False:
                    self.fichas.ficha_f.pintar_presionado()
                    self.primera_vez_presionado_ficha_f1 = True
                    self.intentos.append(['f', 1])
        
        def press_ficha_g_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_g1 == False:
                    self.fichas.ficha_g.pintar_presionado()
                    self.primera_vez_presionado_ficha_g1 = True
                    self.intentos.append(['g', 1])
        
        def press_ficha_h_1():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_h1 == False:
                    self.fichas.ficha_h.pintar_presionado()
                    self.primera_vez_presionado_ficha_h1 = True
                    self.intentos.append(['h', 1])
        
        
        
        # segudo grupo de funciones
        def press_ficha_a_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_a2 == False:
                    self.fichas.ficha_a2.pintar_presionado()
                    self.primera_vez_presionado_ficha_a2 = True
                    self.intentos.append(['a', 2])

        def press_ficha_b_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_b2 == False:
                    self.fichas.ficha_b2.pintar_presionado()
                    self.primera_vez_presionado_ficha_b2 = True
                    self.intentos.append(['b', 2])
        
        def press_ficha_c_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_c2 == False:
                    self.fichas.ficha_c2.pintar_presionado()
                    self.primera_vez_presionado_ficha_c2 = True
                    self.intentos.append(['c', 2])
        
        def press_ficha_d_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_d2 == False:
                    self.fichas.ficha_d2.pintar_presionado()
                    self.primera_vez_presionado_ficha_d2 = True
                    self.intentos.append(['d', 2])
        
        def press_ficha_e_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_e2 == False:
                    self.fichas.ficha_e2.pintar_presionado()
                    self.primera_vez_presionado_ficha_e2 = True
                    self.intentos.append(['e', 2])
        
        def press_ficha_f_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_f2 == False:
                    self.fichas.ficha_f2.pintar_presionado()
                    self.primera_vez_presionado_ficha_f2 = True
                    self.intentos.append(['f', 2])
        
        def press_ficha_g_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_g2 == False:
                    self.fichas.ficha_g2.pintar_presionado()
                    self.primera_vez_presionado_ficha_g2 = True
                    self.intentos.append(['g', 2])
        
        def press_ficha_h_2():
            if self.estado == True:
                if self.primera_vez_presionado_ficha_h2 == False:
                    self.fichas.ficha_h2.pintar_presionado()
                    self.primera_vez_presionado_ficha_h2 = True
                    self.intentos.append(['h', 2])
        
        
        
        
        
        
        
        
        self.fichas.ficha_a.conectar_presionado(press_ficha_a_1)
        self.fichas.ficha_b.conectar_presionado(press_ficha_b_1)
        self.fichas.ficha_c.conectar_presionado(press_ficha_c_1)
        self.fichas.ficha_d.conectar_presionado(press_ficha_d_1)
        self.fichas.ficha_e.conectar_presionado(press_ficha_e_1)
        self.fichas.ficha_f.conectar_presionado(press_ficha_f_1)
        self.fichas.ficha_g.conectar_presionado(press_ficha_g_1)
        self.fichas.ficha_h.conectar_presionado(press_ficha_h_1)
        
        
        
        self.fichas.ficha_a2.conectar_presionado(press_ficha_a_2)
        self.fichas.ficha_b2.conectar_presionado(press_ficha_b_2)
        self.fichas.ficha_c2.conectar_presionado(press_ficha_c_2)
        self.fichas.ficha_d2.conectar_presionado(press_ficha_d_2)
        self.fichas.ficha_e2.conectar_presionado(press_ficha_e_2)
        self.fichas.ficha_f2.conectar_presionado(press_ficha_f_2)
        self.fichas.ficha_g2.conectar_presionado(press_ficha_g_2)
        self.fichas.ficha_h2.conectar_presionado(press_ficha_h_2)




    def conectar_funciones_para_analizar_pares(self):
        # borramos la ficha y agregamos 10 a puntaje
        def borrar_ficha_x(ficha_x):
            ficha_x.eliminar()
            ficha_x.desactivar()
            self.crear_variables_para_presionar_una_vez_ficha()
            
            # aumentamos 5 dos veces al ser dos pares o sea 10
            self.puntaje.aumentar(5)
            self.estado = True
            
        
        # pintamos fichas impares y restamos 2 a puntaje
        def pintar_normal_ficha_x(n, tipo):
            
            self.puntaje.aumentar(-1)
    
            if n == 1 and tipo == 1:
                self.fichas.ficha_a.pintar_normal()
            if n == 1 and tipo == 2:
                self.fichas.ficha_a2.pintar_normal()
            
            if n == 2 and tipo == 1:
                self.fichas.ficha_b.pintar_normal()
            if n == 2 and tipo == 2:
                self.fichas.ficha_b2.pintar_normal()
            
            if n == 3 and tipo == 1:
                self.fichas.ficha_c.pintar_normal()
            if n == 3 and tipo == 2:
                self.fichas.ficha_c2.pintar_normal()
            
            if n == 4 and tipo == 1:
                self.fichas.ficha_d.pintar_normal()
            if n == 4 and tipo == 2:
                self.fichas.ficha_d2.pintar_normal()
            
            if n == 5 and tipo == 1:
                self.fichas.ficha_e.pintar_normal()
            if n == 5 and tipo == 2:
                self.fichas.ficha_e2.pintar_normal()
            
            if n == 6 and tipo == 1:
                self.fichas.ficha_f.pintar_normal()
            if n == 6 and tipo == 2:
                self.fichas.ficha_f2.pintar_normal()
            
            if n == 7 and tipo == 1:
                self.fichas.ficha_g.pintar_normal()
            if n == 7 and tipo == 2:
                self.fichas.ficha_g2.pintar_normal()
            
            if n == 8 and tipo == 1:
                self.fichas.ficha_h.pintar_normal()
            if n == 8 and tipo == 2:
                self.fichas.ficha_h2.pintar_normal()
            
            
            self.estado = True
            
            
        
        def analizar_pares():

            if len(self.intentos) == 2:
                if self.intentos[0][0] == self.intentos[1][0]:
                    if self.intentos[0][0] == 'a':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_a)   
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_a2)  
                    
                    if self.intentos[0][0] == 'b':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_b)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_b2)  
                    
                    if self.intentos[0][0] == 'c':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_c)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_c2)  
                    
                    if self.intentos[0][0] == 'd':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_d)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_d2)  
                    
                    if self.intentos[0][0] == 'e':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_e)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_e2) 
                    
                    if self.intentos[0][0] == 'f':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_f)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_f2) 
                    
                    if self.intentos[0][0] == 'g':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_g)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_g2) 
                    
                    if self.intentos[0][0] == 'h':
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_h)  
                        pilas.mundo.agregar_tarea(1, borrar_ficha_x,self.fichas.ficha_h2) 
                    
                    self.estado = False
                    
                    
                    self.intentos.pop()
                    self.intentos.pop()

                else:
                    contador = 0
                    contador_2 = 0

                    for i in 'abcdefgh':
                        contador = contador + 1
                        contador_2 = contador_2 + 1
                        if self.intentos[0][0] == i:
                            if self.intentos[0][1] == 1:
                                pilas.mundo.agregar_tarea(1, pintar_normal_ficha_x,contador, 1)

                            if self.intentos[0][1] == 2:
                                pilas.mundo.agregar_tarea(1, pintar_normal_ficha_x,contador, 2)

                        if self.intentos[1][0] == i:
                            if self.intentos[1][1] == 1:
                                pilas.mundo.agregar_tarea(1, pintar_normal_ficha_x,contador_2, 1)
                            
                            if self.intentos[1][1] == 2:
                                pilas.mundo.agregar_tarea(1, pintar_normal_ficha_x,contador_2, 2)
                        
                        self.estado = False
                            
                            
                    self.crear_variables_para_presionar_una_vez_ficha()
                    self.intentos.pop()
                    self.intentos.pop()


        self.fichas.ficha_a.conectar_presionado(analizar_pares)
        self.fichas.ficha_b.conectar_presionado(analizar_pares)
        self.fichas.ficha_c.conectar_presionado(analizar_pares)
        self.fichas.ficha_d.conectar_presionado(analizar_pares)
        self.fichas.ficha_e.conectar_presionado(analizar_pares)
        self.fichas.ficha_f.conectar_presionado(analizar_pares)
        self.fichas.ficha_g.conectar_presionado(analizar_pares)
        self.fichas.ficha_h.conectar_presionado(analizar_pares)
        
        
        
        self.fichas.ficha_a2.conectar_presionado(analizar_pares)
        self.fichas.ficha_b2.conectar_presionado(analizar_pares)
        self.fichas.ficha_c2.conectar_presionado(analizar_pares)
        self.fichas.ficha_d2.conectar_presionado(analizar_pares)
        self.fichas.ficha_e2.conectar_presionado(analizar_pares)
        self.fichas.ficha_f2.conectar_presionado(analizar_pares)
        self.fichas.ficha_g2.conectar_presionado(analizar_pares)
        self.fichas.ficha_h2.conectar_presionado(analizar_pares)





