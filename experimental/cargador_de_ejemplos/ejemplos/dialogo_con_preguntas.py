# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()                                                                                         

# La secuencia es sencilla, el mono dice 'hola', 
mono = pilas.actores.Mono(x=-100)
mono_chiquito = pilas.actores.Mono(x=200)
mono_chiquito.escala = 0.75
d = pilas.actores.Dialogo()
d.decir(mono, "¿Cual es tu color favorito?")

def cuando_responde_color_favorito(respuesta):
    colores = {
               'rojo': pilas.colores.rojo,
               'verde': pilas.colores.verde,
               'azul': pilas.colores.azul,
              }

    pilas.fondos.Color(colores[respuesta])
    mono.sonreir()
    d.decir(mono, "¡mira!")
    d.decir(mono_chiquito, "fua...")

d.elegir(mono_chiquito, "Mi color favorito es el...", ["rojo", "verde", "azul"], cuando_responde_color_favorito)


d.iniciar()
pilas.avisar("Tienes que hacer click para que la animacion avance.")
pilas.ejecutar()
