import pilas
from pilas import dev


def accion3(evento):
    dev.deprecated_warning("accion3", se_desactiva_en="0.81", se_elimina_en="0.83",
                reemplazo="accion3_nueva")
    print("Accion 3")

@dev.deprecated(se_desactiva_en="0.81", se_elimina_en="0.83",
                reemplazo="accion4_nueva")
def accion4(evento):
        print("Accion 4")

pilas.iniciar()

actor = pilas.actores.Actor()

pilas.escena_actual().pulsa_tecla.conectar(accion3)
pilas.escena_actual().suelta_tecla.conectar(accion4)

