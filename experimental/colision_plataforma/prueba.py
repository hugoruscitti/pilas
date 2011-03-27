import pilas
from scroll_parallax import layers

pilas.iniciar()

velocidad = 5
GRAVEDAD = 0.9

class var:
    dy = 0
    colision = False
    gravedad = True

class variables:
    velocidad = 5

class tiles:
    def __init__(self):
        self.tiles = []

    def agregar_tile(self, y, x, ruta):
        img = pilas.imagenes.cargar(ruta)
        tile = pilas.actores.Actor(img)

        tile.x = (32 * (x - 10)) + 16
        tile.y = (32 * (-y + 7))

        self.tiles.append(tile)


capas = layers(modo = 'manual')

capas.agregar('cielo.png')
capas.agregar('montes.png', 1, sentido = -1)
capas.agregar('pasto.png', 3, sentido = -1, y = -120)
capas.agregar('arboles.png', 4, sentido = -1, y = -90)


tilset = tiles()

# suelo
for i in range(40):
    tilset.agregar_tile(14, i, 'b.png')

# esquinas
tilset.agregar_tile(14, -1, 'a.png')
tilset.agregar_tile(14, 40, 'c.png')

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






imagen = pilas.imagenes.cargar("cuadrado.png")
caja = pilas.actores.Actor(imagen)

caja.centro = ("centro", "abajo")









def press(evento):
    caja.y -= var.dy
    var.dy += GRAVEDAD

    if var.dy >= 0:
        if var.colision == False:
            var.gravedad = True

    if caja.y <= -240:
        var.dy = 0
        caja.y = -240

    for i in tilset.tiles:
        if var.gravedad == True:
            if i.colisiona_con_un_punto(caja.x, caja.y):
                var.colision = True
                var.dy = 0
                caja.y = (i.y + 16)
            else:
                var.colision = False
        
    if pilas.mundo.control.izquierda:
        if caja.x < -210:
            capas.mover_izquierda()
            for i in tilset.tiles:
                i.x += variables.velocidad
        else:
            caja.x -= velocidad
                

    if pilas.mundo.control.derecha:
        if caja.x > 210:
            capas.mover_derecha()
            for i in tilset.tiles:
                i.x -= variables.velocidad                
        else:
            caja.x += velocidad

    if var.dy == 0:
        var.colision = False
        if pilas.mundo.control.arriba:
            var.gravedad = False
            var.dy = -25
        
    


pilas.eventos.actualizar.conectar(press)

pilas.ejecutar()
