# coding: utf-8
import pilasengine

pilas = pilasengine.iniciar()

duracion = 3

#Construye a los 8 actores, uno por cada tipo de interpolación que tiene pilas.
actores = pilas.actores.Aceituna() * 5
textos = ["lineal", "aceleracion_gradual", "desaceleracion_gradual",
          "gradual", "elastico"]


# Toma a los actores y los ordena, para que aparezcan en una linea vertical.
# Además, por cada actor, genera un texto que indica el tipo de interpolación
# que realizará.
for indice, actor in enumerate(actores):
    actor.y = 157 + indice * -50
    actor.x = 0

    actor_texto = pilas.actores.Texto(textos[indice], magnitud=12)
    actor_texto.y  = actor.y
    actor_texto.centro_x = 0
    actor_texto.x = -150

# Función para retornar a todos los actores a su posición inicial.
# como "actores" es un grupo, que se generó haciendo una multiplicación
# por 8, se puede usar el atajo "actores.x" para indicarle a todos
# los actores del grupo que cambien su coordenada x.
# Otra forma de hacer lo mismo es así:
#
#     for un_actor in actores:
#         un_actor.x = 0
#
def mover_a_posicion_inicial():
    actores.x = 0

# Se genera el botón para que el usuario pueda hacer que todos los
# actores regresen a la posición incial.
boton_reiniciar = pilas.interfaz.Boton(u"Volver a la posición inicial")
boton_reiniciar.conectar(mover_a_posicion_inicial)
boton_reiniciar.x = -246
boton_reiniciar.y = 150


# Realiza las interpolaciones de los actores.
def realizar_interpolaciones():
    actores.x = 0
    pilas.utils.interpolar(actores[0], 'x', 200, duracion=duracion, tipo='lineal')
    pilas.utils.interpolar(actores[1], 'x', 200, duracion=duracion, tipo='aceleracion_gradual')
    pilas.utils.interpolar(actores[2], 'x', 200, duracion=duracion, tipo='desaceleracion_gradual')
    pilas.utils.interpolar(actores[3], 'x', 200, duracion=duracion, tipo='gradual')
    pilas.utils.interpolar(actores[4], 'x', 200, duracion=duracion, tipo='elastico')

# Se genera el botón que hará que se inicien todas las interpolaciones.
boton_interpolacion = pilas.interfaz.Boton("Realizar interpolaciones")
boton_interpolacion.conectar(realizar_interpolaciones)
boton_interpolacion.x = -250
boton_interpolacion.y = 100


pilas.ejecutar()
