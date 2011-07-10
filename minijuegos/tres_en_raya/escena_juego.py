import pilas
from random import random

class Juego(pilas.escenas.Escena):
    "Escena que Controla el juego"

    def __init__(self):        
        pilas.escenas.Escena.__init__(self) 
        pilas.actores.utils.eliminar_a_todos()
        pilas.fondos.Fondo('data/fondo.png')

        pilas.eventos.pulsa_tecla_escape.conectar(self.cuando_se_presione_escape)
        
        #creamos tablero
        self.crear_tablero()
        
        self.crear_pizarra() #servira para trazar lineas ganadoras
        
        #creamos fichas
        self.crear_fichas_1()
        self.crear_fichas_2()
        
        # turno = 0 para jugador 1
        # turno = 1 para jugador 2
        
        self.turno = int(random() * 2)
        
        # estado = -1 cuando estamos jugando
        # estado = 0 gana jugador 1
        # estado = 1 gano jugador 2
        # estado = 2 nadie gano
        
        self.estado = -1
        
        
        self.turno_o = pilas.imagenes.cargar('data/ficha1.png')
        self.turno_x = pilas.imagenes.cargar('data/ficha2.png')
        if self.turno == 0:
            self.turno_actual = pilas.actores.Actor(self.turno_o, -163, 80)
            self.turno_actual.escala = 0.5
        else:
            self.turno_actual = pilas.actores.Actor(self.turno_x, -163, 80)
            self.turno_actual.escala = 0.5
        
        self.conectar_fichas1_con_eventos()
        self.conectar_fichas2_con_eventos()
        
    def cuando_se_presione_escape(self, *k, **kv):
        "Regresa al menu principal"
        import escena_menu
        escena_menu.EscenaMenu()
    

    def crear_pizarra(self):
        self.pizarra = pilas.actores.Pizarra()
    

    def pintar_linea_horizontal(self, h):
        self.pizarra.linea(-100, h, 100, h, pilas.colores.cyan, grosor=3)
    
    
    def pintar_linea_diagonal_1(self):
        self.pizarra.linea(-84, 84, 84, -84, pilas.colores.cyan, grosor=3)
        
    def pintar_linea_diagonal_2(self):
        self.pizarra.linea(84, 84, -84, -84, pilas.colores.cyan, grosor=3)
        
    def pintar_linea_vertical(self, v):
        self.pizarra.linea(v, -100, v, 100, pilas.colores.cyan, grosor=3)
    
    def crear_tablero(self):
        self.tablero_matriz = [[-1, -1, -1],[-1, -1, -1],[-1, -1, -1]]
        
        # esta matriz se utiliza para saber que ficha se encuentra
        # en cada lugar o si es una casilla vacia.
        # 0 = ficha 1 
        # 1 = ficha 2
        # -1 = no hay ficha
        
    def crear_fichas_1(self):
        
        self.ruta_ficha_vacia = 'data/ficha_vacia.png'
        self.ruta_ficha_1 = 'data/ficha1.png'
        
        self.ficha1_1 = pilas.actores.Boton(-84, 84,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_2 = pilas.actores.Boton(0, 84,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_3 = pilas.actores.Boton(84, 84,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_4 = pilas.actores.Boton(-84, 0,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_5 = pilas.actores.Boton(0, 0,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_6 = pilas.actores.Boton(84, 0,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_7 = pilas.actores.Boton(-84, -84,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_8 = pilas.actores.Boton(0, -84,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        self.ficha1_9 = pilas.actores.Boton(84, -84,  self.ruta_ficha_vacia,  self.ruta_ficha_1, self.ruta_ficha_1)
        
        
    def crear_fichas_2(self):
        
        self.ruta_ficha_vacia = 'data/ficha_vacia.png'
        self.ruta_ficha_2 = 'data/ficha2.png'
        B = pilas.actores.Boton
        
        self.ficha2_1 = pilas.actores.Boton(-84, 84,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_2 = pilas.actores.Boton(0, 84,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_3 = pilas.actores.Boton(84, 84,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_4 = pilas.actores.Boton(-84, 0,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_5 = pilas.actores.Boton(0, 0,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_6 = pilas.actores.Boton(84, 0,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_7 = pilas.actores.Boton(-84, -84,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_8 = pilas.actores.Boton(0, -84,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        self.ficha2_9 = pilas.actores.Boton(84, -84,  self.ruta_ficha_vacia, self.ruta_ficha_2, self.ruta_ficha_2)
        
    
    
    
    
    
    
    def cambiar_visor_turno_o(self):
        self.turno_actual.definir_imagen(self.turno_o)
        
    def cambiar_visor_turno_x(self):
        self.turno_actual.definir_imagen(self.turno_x)
        
    def conectar_fichas1_con_eventos(self):
        self.ficha1_1.conectar_presionado(self.press_ficha1_1)
        self.ficha1_1.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_2.conectar_presionado(self.press_ficha1_2)
        self.ficha1_2.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_3.conectar_presionado(self.press_ficha1_3)
        self.ficha1_3.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_4.conectar_presionado(self.press_ficha1_4)
        self.ficha1_4.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_5.conectar_presionado(self.press_ficha1_5)
        self.ficha1_5.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_6.conectar_presionado(self.press_ficha1_6)
        self.ficha1_6.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_7.conectar_presionado(self.press_ficha1_7)
        self.ficha1_7.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_8.conectar_presionado(self.press_ficha1_8)
        self.ficha1_8.conectar_presionado(self.analizar_ganador)
        
        self.ficha1_9.conectar_presionado(self.press_ficha1_9)
        self.ficha1_9.conectar_presionado(self.analizar_ganador)
        
    
    def conectar_fichas2_con_eventos(self):
        self.ficha2_1.conectar_presionado(self.press_ficha2_1)
        self.ficha2_1.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_2.conectar_presionado(self.press_ficha2_2)
        self.ficha2_2.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_3.conectar_presionado(self.press_ficha2_3)
        self.ficha2_3.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_4.conectar_presionado(self.press_ficha2_4)
        self.ficha2_4.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_5.conectar_presionado(self.press_ficha2_5)
        self.ficha2_5.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_6.conectar_presionado(self.press_ficha2_6)
        self.ficha2_6.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_7.conectar_presionado(self.press_ficha2_7)
        self.ficha2_7.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_8.conectar_presionado(self.press_ficha2_8)
        self.ficha2_8.conectar_presionado(self.analizar_ganador)
        
        self.ficha2_9.conectar_presionado(self.press_ficha2_9)
        self.ficha2_9.conectar_presionado(self.analizar_ganador)
    
    
    # metodos para cada ficha 1
    
    # controlan si hay una casilla vacia, para poner una ficha
    # controla el visor de turnos y los turnos
    
    def press_ficha1_1(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[0][0] == -1:
                    self.tablero_matriz[0][0] = 0 
                    self.ficha1_1.pintar_presionado()
                    self.ficha1_1.escala = 0.8
                    self.ficha1_1.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
                    
    def press_ficha1_2(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[0][1] == -1:
                    self.tablero_matriz[0][1] = 0 
                    self.ficha1_2.pintar_presionado()
                    self.ficha1_2.escala = 0.8
                    self.ficha1_2.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_3(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[0][2] == -1:
                    self.tablero_matriz[0][2] = 0 
                    self.ficha1_3.pintar_presionado()
                    self.ficha1_3.escala = 0.8
                    self.ficha1_3.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_4(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[1][0] == -1:
                    self.tablero_matriz[1][0] = 0 
                    self.ficha1_4.pintar_presionado()
                    self.ficha1_4.escala = 0.8
                    self.ficha1_4.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_5(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[1][1] == -1:
                    self.tablero_matriz[1][1] = 0 
                    self.ficha1_5.pintar_presionado()
                    self.ficha1_5.escala = 0.8
                    self.ficha1_5.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_6(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[1][2] == -1:
                    self.tablero_matriz[1][2] = 0 
                    self.ficha1_6.pintar_presionado()
                    self.ficha1_6.escala = 0.8
                    self.ficha1_6.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_7(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[2][0] == -1:
                    self.tablero_matriz[2][0] = 0 
                    self.ficha1_7.pintar_presionado()
                    self.ficha1_7.escala = 0.8
                    self.ficha1_7.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_8(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[2][1] == -1:
                    self.tablero_matriz[2][1] = 0 
                    self.ficha1_8.pintar_presionado()
                    self.ficha1_8.escala = 0.8
                    self.ficha1_8.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    def press_ficha1_9(self):
        if self.estado == -1:
            if self.turno == 0:
                if self.tablero_matriz[2][2] == -1:
                    self.tablero_matriz[2][2] = 0 
                    self.ficha1_9.pintar_presionado()
                    self.ficha1_9.escala = 0.8
                    self.ficha1_9.escala = [1], 0.1
                    self.turno = 1
                    self.cambiar_visor_turno_x()
    
    
    
    
    
    
    
    
    
    #metodos para cada ficha 2
    
    def press_ficha2_1(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[0][0] == -1:
                    self.tablero_matriz[0][0] = 1 
                    self.ficha2_1.pintar_presionado()
                    self.ficha2_1.escala = 0.8
                    self.ficha2_1.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()

    def press_ficha2_2(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[0][1] == -1:
                    self.tablero_matriz[0][1] = 1 
                    self.ficha2_2.pintar_presionado()
                    self.ficha2_2.escala = 0.8
                    self.ficha2_2.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()

    def press_ficha2_3(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[0][2] == -1:
                    self.tablero_matriz[0][2] = 1 
                    self.ficha2_3.pintar_presionado()
                    self.ficha2_3.escala = 0.8
                    self.ficha2_3.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    def press_ficha2_4(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[1][0] == -1:
                    self.tablero_matriz[1][0] = 1 
                    self.ficha2_4.pintar_presionado()
                    self.ficha2_4.escala = 0.8
                    self.ficha2_4.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    def press_ficha2_5(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[1][1] == -1:
                    self.tablero_matriz[1][1] = 1
                    self.ficha2_5.pintar_presionado()
                    self.ficha2_5.escala = 0.8
                    self.ficha2_5.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    def press_ficha2_6(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[1][2] == -1:
                    self.tablero_matriz[1][2] = 1 
                    self.ficha2_6.pintar_presionado()
                    self.ficha2_6.escala = 0.8
                    self.ficha2_6.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    def press_ficha2_7(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[2][0] == -1:
                    self.tablero_matriz[2][0] = 1 
                    self.ficha2_7.pintar_presionado()
                    self.ficha2_7.escala = 0.8
                    self.ficha2_7.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    def press_ficha2_8(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[2][1] == -1:
                    self.tablero_matriz[2][1] = 1 
                    self.ficha2_8.pintar_presionado()
                    self.ficha2_8.escala = 0.8
                    self.ficha2_8.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    def press_ficha2_9(self):
        if self.estado == -1:
            if self.turno == 1:
                if self.tablero_matriz[2][2] == -1:
                    self.tablero_matriz[2][2] = 1 
                    self.ficha2_9.pintar_presionado()
                    self.ficha2_9.escala = 0.8
                    self.ficha2_9.escala = [1], 0.1
                    self.turno = 0
                    self.cambiar_visor_turno_o()
    
    
    

    
    

    # comprueba si a ocurrido tres en raya o empate
    def nadie_gano(self):
        for i in range(3):
            for j in range(3):
                if self.tablero_matriz[i][j] == -1:
                    return False
        return True
        
    def analizar_ganador(self):
        
        self.posicion_texto = [0, -180]
        
        ## gano player 1
        
        if (self.tablero_matriz[0][0] == self.tablero_matriz[0][1] == self.tablero_matriz[0][2] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_horizontal(84)
                t.color = (pilas.colores.blanco)
                
        elif (self.tablero_matriz[0][0] == self.tablero_matriz[1][0] == self.tablero_matriz[2][0] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_vertical(-84)
                t.color = (pilas.colores.blanco)

        if (self.tablero_matriz[1][0] == self.tablero_matriz[1][1] == self.tablero_matriz[1][2] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_horizontal(0)
                t.color = (pilas.colores.blanco)
        
        elif (self.tablero_matriz[0][1] == self.tablero_matriz[1][1] == self.tablero_matriz[2][1] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_vertical(0)
                t.color = (pilas.colores.blanco)

        if (self.tablero_matriz[0][2] == self.tablero_matriz[1][2] == self.tablero_matriz[2][2] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_vertical(84)
                t.color = (pilas.colores.blanco)

        elif (self.tablero_matriz[2][0] == self.tablero_matriz[2][1] == self.tablero_matriz[2][2] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_horizontal(-84)
                t.color = (pilas.colores.blanco)

        if (self.tablero_matriz[0][0] == self.tablero_matriz[1][1] == self.tablero_matriz[2][2] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_diagonal_1()
                t.color = (pilas.colores.blanco)
                
        if (self.tablero_matriz[0][2] == self.tablero_matriz[1][1] == self.tablero_matriz[2][0] == 0):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 1!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 0
                self.pintar_linea_diagonal_2()
                t.color = (pilas.colores.blanco)
	
	
	    ## gano player 2
        
        if (self.tablero_matriz[0][0] == self.tablero_matriz[0][1] == self.tablero_matriz[0][2] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_horizontal(84)
                t.color = (pilas.colores.blanco)
                
        elif (self.tablero_matriz[0][0] == self.tablero_matriz[1][0] == self.tablero_matriz[2][0] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_vertical(-84)
                t.color = (pilas.colores.blanco)

        if (self.tablero_matriz[1][0] == self.tablero_matriz[1][1] == self.tablero_matriz[1][2] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_horizontal(0)
        
        elif (self.tablero_matriz[0][1] == self.tablero_matriz[1][1] == self.tablero_matriz[2][1] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_vertical(0)
                t.color = (pilas.colores.blanco)

        if (self.tablero_matriz[0][2] == self.tablero_matriz[1][2] == self.tablero_matriz[2][2] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_vertical(84)
                t.color = (pilas.colores.blanco)

        elif (self.tablero_matriz[2][0] == self.tablero_matriz[2][1] == self.tablero_matriz[2][2] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_horizontal(-84)
                t.color = (pilas.colores.blanco)

        if (self.tablero_matriz[0][0] == self.tablero_matriz[1][1] == self.tablero_matriz[2][2] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_diagonal_1()
                t.color = (pilas.colores.blanco)
        if (self.tablero_matriz[0][2] == self.tablero_matriz[1][1] == self.tablero_matriz[2][0] == 1):
            if self.estado == -1:
                t = pilas.actores.Texto("Gana Jugador 2!", 
                                        self.posicion_texto[0], 
                                        self.posicion_texto[1])
                self.estado = 1
                self.pintar_linea_diagonal_2()
                t.color = (pilas.colores.blanco)
                
        temp_nadie_gana = self.nadie_gano()


        if temp_nadie_gana == True:
            if self.estado == -1:
                t = pilas.actores.Texto("Nadie ha ganado, vuelve a intentarlo!",
                                         self.posicion_texto[0], 
                                         self.posicion_texto[1])
                self.estado = 2
                t.color = (pilas.colores.blanco)


