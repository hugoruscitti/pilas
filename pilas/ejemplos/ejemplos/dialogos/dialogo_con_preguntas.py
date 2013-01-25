# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()

# La secuencia es sencilla, el mono dice 'hola',
mono = pilas.actores.Mono(x=-100)
mono_chiquito = pilas.actores.Mono(x=200)
mono_chiquito.escala = 0.75
d = pilas.actores.Dialogo()
d.decir(mono, u"¿Cual es tu color favorito?")

def cuando_responde_color_favorito(respuesta):
    colores = {
               u'rojo': pilas.colores.rojo,
               u'verde': pilas.colores.verde,
               u'azul': pilas.colores.azul,
              }

    pilas.fondos.Color(colores[respuesta])
    mono.sonreir()
    d.decir(mono, u"¡mira!")
    d.decir(mono_chiquito, u"fua...")

d.elegir(mono_chiquito, u"Mi color favorito es el...", [u"rojo", u"verde", u"azul"], cuando_responde_color_favorito)


d.iniciar()
pilas.avisar(u"Tienes que hacer click para que la animación avance.")
pilas.ejecutar()
