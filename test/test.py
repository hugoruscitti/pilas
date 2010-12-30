import pilas
import pilas.elements as elements

pilas.iniciar()
size = (640, 480)
mundo = elements.Elements(screen_size=size, renderer="cairo")

b = pilas.actores.Pizarra()

b1 = mundo.add.ball((0, 0), 20)
b1 = mundo.add.ball((120, 0), 20)
v2 = mundo.add.triangle((120, 0), 20)
v3 = mundo.add.rect((120, 0), 20, 30)
v4 = mundo.add.wall((0, 200), (400, 300))


class estado_boton:
    presionado = False

class elementos:
    figura = 0

boton = pilas.actores.Boton(250, 220, 'data/circulo_normal.png', 'data/circulo_press.png')
boton1 = pilas.actores.Boton(250, 190, 'data/triangulo_normal.png', 'data/triangulo_press.png')
boton2 = pilas.actores.Boton(250, 160, 'data/rectangulo_normal.png', 'data/rectangulo_press.png')

def press_boton():
    estado_boton.presionado = True
    boton.pintar_presionado()
    elementos.figura = 0

def press_boton1():
    estado_boton.presionado = True
    boton1.pintar_presionado()
    elementos.figura = 1

def press_boton2():
    estado_boton.presionado = True
    boton2.pintar_presionado()
    elementos.figura = 2


#conectamos funciones boton 
boton.conectar_presionado(press_boton)
boton1.conectar_presionado(press_boton1)
boton2.conectar_presionado(press_boton2)

boton.conectar_normal(boton.pintar_normal)
boton1.conectar_normal(boton1.pintar_normal)
boton2.conectar_normal(boton2.pintar_normal)


def agregar_elemeto(evento):    
    if estado_boton.presionado:
        estado_boton.presionado = False
    else:
        if elementos.figura == 0:
            b1 = mundo.add.ball((evento.x + (640 / 2), (evento.y * -1) + (480 / 2)), 20)

        elif elementos.figura == 1:
            v2 = mundo.add.triangle((evento.x + (640 / 2), (evento.y * -1) + (480 / 2)), 20)

        elif elementos.figura == 2:
            v3 = mundo.add.rect((evento.x + (640 / 2), (evento.y * -1) + (480 / 2)), 20, 30)


pilas.eventos.click_de_mouse.conectar(agregar_elemeto)



mundo.renderer.set_pizarra(b)
mundo.add.ground()

class Actor(pilas.actores.Actor):

    def __init__(self):
        pilas.actores.Actor.__init__(self, 'invisible.png')

    def actualizar(self):
        mundo.update()
        mundo.draw()
        b.actualizar_imagen()
        pass



a = Actor()

pilas.ejecutar()
