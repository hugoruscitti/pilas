# -*- encoding: utf-8 -*-
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import pilas

def obtener_celda(evento):
    global mapa
    izquierda, derecha, arriba, abajo = pilas.escena_actual().camara.obtener_area_visible()

    x, y = mapa.convertir_de_coordenada_absoluta_a_coordenada_mapa(izquierda, arriba)
    y = mapa.obtener_numero_de_fila(y)
    x = mapa.obtener_numero_de_columna(x)
    print "X: %s" %(x)
    print "Y: %s" %(y)

def crear_mapa():
    mapa = pilas.actores.Mapa(filas=15, columnas=200)



    # Pinta todo el suelo
    for columna in range(0, 200):
        mapa.pintar_bloque(14, columna, 1)

    # Pinta todo el suelo
    for columna in range(0, 200):
        mapa.pintar_bloque(9, columna, 1)

    return mapa

pilas.iniciar()

mapa = crear_mapa()
martian = pilas.actores.Martian(mapa)
martian.aprender(pilas.habilidades.SiempreEnElCentro)

#pilas.escena_actual().mueve_mouse.conectar(obtener_celda)

pilas.ejecutar()
