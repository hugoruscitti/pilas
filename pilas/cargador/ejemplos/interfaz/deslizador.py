import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
mono = pilas.actores.Mono(y=-100)

def cuando_cambia_escala(valor):
    mono.escala = valor * 2

deslizador_escala = pilas.interfaz.Deslizador(y=50)
deslizador_escala.conectar(cuando_cambia_escala)


def cuando_cambia_rotacion(valor):
    mono.rotacion = valor * 360

deslizador_rotacion = pilas.interfaz.Deslizador(y=100)
deslizador_rotacion.conectar(cuando_cambia_rotacion)


def cuando_cambia_posicion(valor):
    # Obtiene valores entre -200 y 400
    mono.x = -200 + 400 * valor
    print valor


deslizador_posicion = pilas.interfaz.Deslizador(y=150)
deslizador_posicion.conectar(cuando_cambia_posicion)

pilas.avisar("Usa el deslizador para modificar al mono.")
pilas.ejecutar()
