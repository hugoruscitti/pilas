# For pilas engine - a video game framework.
#
# copyright 2011 - Pablo Garrido
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar

import pilas
pilas.iniciar()

class variables:
    velocidad = 3

class tiles:
    def __init__(self):
        self.tiles = []

    def agregar_tile(self, y, x, ruta):
        img = pilas.imagenes.cargar(ruta)
        tile = pilas.actores.Actor(img)

        tile.x = (32 * (x - 10)) + 16
        tile.y = (32 * (-y + 7)) 

        self.tiles.append(tile)


texto = pilas.actores.Texto("Presiona las flechas para mover el escenario")
texto.color = pilas.colores.negro
texto.magnitud = 20
texto.y = 200


tilset = tiles()

# suelo
for i in range(30):
    tilset.agregar_tile(14, i, 'b.png')

# esquinas
tilset.agregar_tile(14, -1, 'a.png')
tilset.agregar_tile(14, 30, 'c.png')

# plataforma 1
tilset.agregar_tile(7, 11, 'a.png')
tilset.agregar_tile(7, 12, 'b.png')
tilset.agregar_tile(7, 13, 'b.png')
tilset.agregar_tile(7, 14, 'c.png')

# plataforma 2
tilset.agregar_tile(4, 3, 'a.png')
tilset.agregar_tile(4, 4, 'b.png')
tilset.agregar_tile(4, 5, 'b.png')
tilset.agregar_tile(4, 6, 'b.png')
tilset.agregar_tile(4, 7, 'c.png')

# plataforma 3

tilset.agregar_tile(5, 25, 'a.png')
tilset.agregar_tile(5, 26, 'b.png')
tilset.agregar_tile(5, 27, 'b.png')
tilset.agregar_tile(5, 28, 'b.png')
tilset.agregar_tile(5, 29, 'c.png')


def press(evento):        
    if pilas.mundo.control.derecha:
        for i in tilset.tiles:
            i.x -= variables.velocidad 
            

    if pilas.mundo.control.izquierda:
        for i in tilset.tiles:
            i.x += variables.velocidad

pilas.eventos.actualizar.conectar(press)
pilas.ejecutar()
