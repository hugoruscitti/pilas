# -*- encoding: utf-8 -*-
# For pilas engine - a video game framework.
#
# copyright 2010 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
from random import random

class clase_fichas:
    
    def __init__(self):

        self.fichas_array = [['v', 'v', 'v', 'v'],
                             ['v', 'v', 'v', 'v'],
                             ['v', 'v', 'v', 'v'],
                             ['v', 'v', 'v', 'v']]
        
        
        self.fichas_posicion = [[[-121, 130], [-40, 130], [41, 130], [122, 130]],
                                [[-121,  43], [-40,  43], [41,  43], [122,  43]],
                                [[-121, -44], [-40, -44], [41, -44], [122, -44]],
                                [[-121,-131], [-40,-131], [41,-131], [122,-131]]]


    
    def imprimir_array(self):
        for i in range(4):
            print self.fichas_array[i] 
        print    
        
        
    def crear_fichas(self):
        
        # primer grupo de fichas
        self.ficha_a = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_a.png')

        self.ficha_b = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_b.png')
        
        self.ficha_c = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_c.png')
        
        self.ficha_d = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_d.png')
        
        self.ficha_e = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_e.png')
        
        self.ficha_f = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_f.png')
        
        self.ficha_g = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_g.png')
        
        self.ficha_h = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_h.png')
        
        
        # segundo grupo de fichas
        self.ficha_a2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_a.png')

        self.ficha_b2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_b.png')
        
        self.ficha_c2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_c.png')
        
        self.ficha_d2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_d.png')
        
        self.ficha_e2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_e.png')
        
        self.ficha_f2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_f.png')
        
        self.ficha_g2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_g.png')
        
        self.ficha_h2 = pilas.actores.Boton(0, 0,'data/casilla.png', 
                                                'data/casilla_h.png')
        
        
        
        
        
    def ordenar_fichas(self):
        caracter = ['a_1', 'a_2', 'b_1', 'b_2', 'c_1', 'c_2', 'd_1', 'd_2',
                    'e_1', 'e_2', 'f_1', 'f_2', 'g_1', 'g_2', 'h_1', 'h_2']

        for i in range(4):
            for j in range(4):
                ocupado = True
                while ocupado:
                    rand_i = int(random() * 16)
                    if caracter[rand_i] != 'x':
                        self.fichas_array[i][j] = caracter[rand_i]
                        caracter[rand_i] = 'x'
                        ocupado = False
    
    
    
    def posicionar_botones_fichas(self):
        
        def posicionar_ficha_x(fichax, i, j):
            fichax.x = self.fichas_posicion[i][j][0]
            fichax.y = self.fichas_posicion[i][j][1]
            

        for i in range(4):
            for j in range(4):
                if self.fichas_array[i][j] == 'a_1':
                    posicionar_ficha_x(self.ficha_a, i, j)
                
                # posicionamos primer grupo de fichas 
                if self.fichas_array[i][j] == 'b_1':
                    posicionar_ficha_x(self.ficha_b, i, j)
               
                if self.fichas_array[i][j] == 'c_1':
                    posicionar_ficha_x(self.ficha_c, i, j)
                 
                if self.fichas_array[i][j] == 'd_1':
                    posicionar_ficha_x(self.ficha_d, i, j)

                if self.fichas_array[i][j] == 'e_1':
                    posicionar_ficha_x(self.ficha_e, i, j)

                if self.fichas_array[i][j] == 'f_1':
                    posicionar_ficha_x(self.ficha_f, i, j)

                if self.fichas_array[i][j] == 'g_1':
                    posicionar_ficha_x(self.ficha_g, i, j)

                if self.fichas_array[i][j] == 'h_1':
                    posicionar_ficha_x(self.ficha_h, i, j)
                
                
                 # posicionamos segundo grupo de fichas 
                if self.fichas_array[i][j] == 'a_2':
                    posicionar_ficha_x(self.ficha_a2, i, j)
                 
                if self.fichas_array[i][j] == 'b_2':
                    posicionar_ficha_x(self.ficha_b2, i, j)
               
                if self.fichas_array[i][j] == 'c_2':
                    posicionar_ficha_x(self.ficha_c2, i, j)
                 
                if self.fichas_array[i][j] == 'd_2':
                    posicionar_ficha_x(self.ficha_d2, i, j)

                if self.fichas_array[i][j] == 'e_2':
                    posicionar_ficha_x(self.ficha_e2, i, j)

                if self.fichas_array[i][j] == 'f_2':
                    posicionar_ficha_x(self.ficha_f2, i, j)

                if self.fichas_array[i][j] == 'g_2':
                    posicionar_ficha_x(self.ficha_g2, i, j)

                if self.fichas_array[i][j] == 'h_2':
                    posicionar_ficha_x(self.ficha_h2, i, j)

    
