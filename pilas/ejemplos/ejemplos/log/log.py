import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
b = pilas.actores.Boton()


def cuando_pulsan_el_boton():
    b.pintar_presionado()
    # Un mensaje
    pilas.log.imprimir("Han pulsado el boton")
    # Una variable
    var_1 = 1500
    pilas.log.imprimir(var_1)
    # Un actor
    pilas.log.imprimir(b)
    # Un diccionario
    pilas.log.imprimir({"Mi variable" : var_1})
    
def cuando_deja_de_pulsar():
    b.pintar_normal()

b.conectar_presionado(cuando_pulsan_el_boton)
b.conectar_normal(cuando_deja_de_pulsar)

pilas.ejecutar()
