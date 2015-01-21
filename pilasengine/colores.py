# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

diccionario_colores = {}

class Color(object):
    "Representa un color en base a 4 componentes."

    def __init__(self, r, g, b, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    def __repr__(self):
        return "<Color (%d, %d, %d, %d)>" % (self.r, self.g, self.b, self.a)

    def obtener_componentes(self):
        return (self.r, self.g, self.b, self.a)
    
def generar_color_desde_texto(texto_del_color):
    
    if isinstance(texto_del_color, Color):
        return texto_del_color
    else:
        if diccionario_colores.has_key(texto_del_color):
            return diccionario_colores[texto_del_color.lower()]
        else:
            raise TypeError("No se puede reconocer el color " + texto_del_color)

# Colores principales.
negro = Color(0, 0, 0)
blanco = Color(255, 255, 255)
rojo = Color(255, 0, 0)
verde = Color(0, 255, 0)
azul = Color(0, 0, 255)
gris = Color(128, 128, 128)

# Colores secundarios
amarillo = Color(255, 255, 0)
magenta = Color(255, 0, 255)
cyan = Color(0, 255, 255)
grisclaro = Color(192, 192, 192)
grisoscuro = Color(100, 100, 100)
verdeoscuro = Color(0, 128, 0)
azuloscuro = Color(0, 0, 128)
naranja = Color(255, 200, 0)
rosa = Color(255, 175, 175)
violeta = Color(128, 0, 255)
marron = Color(153, 102, 0)

# Colores transparentes
negro_transparente = Color(0, 0, 0, 160)
blanco_transparente = Color(255, 255, 255, 160)
rojo_transparente = Color(255, 0, 0, 160)
verde_transparente = Color(0, 255, 0, 160)
azul_transparente = Color(0, 0, 255, 160)
gris_transparente = Color(128, 128, 128, 160)
naranja_transparente = Color(255, 200, 0, 140)


diccionario_colores['negro'] = negro
diccionario_colores['blanco'] = blanco
diccionario_colores['rojo'] = rojo
diccionario_colores['verde'] = verde
diccionario_colores['azul'] = azul
diccionario_colores['gris'] = gris

# Colores secundarios
diccionario_colores['amarillo'] = amarillo
diccionario_colores['magenta '] = magenta
diccionario_colores['cyan'] = cyan
diccionario_colores['grisclaro'] = grisclaro
diccionario_colores['grisoscuro'] = grisoscuro
diccionario_colores['verdeoscuro'] = verdeoscuro
diccionario_colores['azuloscuro'] = azuloscuro
diccionario_colores['naranja'] = naranja
diccionario_colores['rosa'] = rosa
diccionario_colores['violeta'] = violeta
diccionario_colores['marron'] = marron

# Colores transparentes
diccionario_colores['negro_transparente'] = negro_transparente
diccionario_colores['blanco_transparente'] = blanco_transparente
diccionario_colores['rojo_transparente'] = rojo_transparente
diccionario_colores['verde_transparente'] = verde_transparente
diccionario_colores['azul_transparente'] = azul_transparente
diccionario_colores['gris_transparente'] = gris_transparente
diccionario_colores['naranja_transparente'] = naranja_transparente