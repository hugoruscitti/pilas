import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
b = pilas.actores.Boton()


def cuando_pulsan_el_boton():
    b.pintar_presionado()
    pilas.avisar("Han pulsado el boton")

def cuando_pasa_sobre_el_boton():
    b.pintar_sobre()
    pilas.avisar("Pasa el mouse sobre el boton")

def cuando_deja_de_pulsar():
    b.pintar_normal()
    pilas.avisar("")


b.conectar_presionado(cuando_pulsan_el_boton)
b.conectar_sobre(cuando_pasa_sobre_el_boton)
b.conectar_normal(cuando_deja_de_pulsar)

pilas.ejecutar()
