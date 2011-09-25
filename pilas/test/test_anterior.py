# -*- encoding: utf-8 -*-
import pilas

def test_existe_mundo():
    pilas.iniciar()
    assert pilas.mundo

def test_cargar_imagenes():
    pilas.iniciar()
    original_image = pilas.imagenes.cargar('mono.png')

    actor = pilas.actores.Actor(original_image)
    actors_image = actor.imagen

    assert original_image == actors_image

def test_planificador():
    pilas.iniciar()
    pilas.mundo.agregar_tarea_una_vez(2, None)
    pilas.mundo.agregar_tarea_una_vez(2, None, (1, 2, 3))

def test_interpolacion():
    pilas.iniciar()
    a = pilas.interpolar([0, 100])
    assert a.values == [0, 100]

    # Invierte la interpolacion.
    a = -a
    assert a.values == [100, 0]

def test_actor_texto():
    pilas.iniciar()
    texto = pilas.actores.Texto("Hola")
    assert texto.texto == "Hola"

    # verificando que el tamaño inicial es de 30 y el color negro
    assert texto.magnitud == 30

def test_habilidades():
    texto = pilas.actores.Texto("Hola")

    # Vincula la clase Text con un componente.
    component = pilas.habilidades.AumentarConRueda 
    texto.aprender(component)

    # Se asegura que el componente pasa a ser de la superclase.
    assert component == texto.habilidades[0].__class__

def test_existen_los_atajos():
    assert pilas.atajos

def test_Ejes():
    ejes = pilas.actores.Ejes()
    assert ejes


def test_Grilla():
    grilla = pilas.imagenes.cargar_grilla("fondos/volley.png", 10, 10)
    assert grilla
    grilla.avanzar()

def test_Fondo():
    un_fondo = pilas.fondos.Tarde()
    assert un_fondo

def test_Control():
    control = pilas.mundo.control

    assert control.izquierda
    assert control.derecha
    assert control.arriba
    assert control.abajo
    assert control.boton


def test_Distancias():
    assert 0 ==  pilas.utils.distancia(0, 0)
    assert 10 == pilas.utils.distancia(0, 10)
    assert 10 == pilas.utils.distancia(0, -10)
    assert 10 == pilas.utils.distancia(-10, 0)

    assert 0 == pilas.utils.distancia_entre_dos_puntos((0, 0), (0, 0))
    assert 10 == pilas.utils.distancia_entre_dos_puntos((0, 0), (10, 0))
    assert 10 == pilas.utils.distancia_entre_dos_puntos((0, 0), (0, 10))
    assert 10 == pilas.utils.distancia_entre_dos_puntos((10, 10), (0, 10))


def test__posiciones_del_texto():
    m = pilas.actores.Texto("Hola")
    assert m.x == 0

    ancho = m.obtener_ancho()
    algo = m.obtener_alto()

    # Verifica que la izquierda del actor esté asociada a la
    # posición 'x'.
    m.izquierda = m.izquierda - 50
    assert m.x == -50

    m.izquierda = m.izquierda - 50
    assert m.x == -100

    # Analiza si la parte derecha del actor esta vinculada a 'x'
    m.derecha = m.derecha + 50
    assert m.x == -50

    # Verifica si la posicion superior e inferior alteran a 'y'
    assert m.y == 0
    m.arriba = m.arriba - 100
    assert m.y == -100

    m.abajo = m.abajo + 100
    assert m.y == 0

if __name__ == '__main__':
    pilas.iniciar()
    unittest.main()
