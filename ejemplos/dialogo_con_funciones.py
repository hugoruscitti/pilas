# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()

# La secuencia es sencilla, el mono dice 'hola', 
mono = pilas.actores.Mono(x=-100)
mono_chiquito = pilas.actores.Mono(x=200)
mono_chiquito.escala = 0.75

d = pilas.actores.Dialogo()
d.decir(mono, "Hola, como estas?")
d.decir(mono_chiquito, "Bien, ¿y vos?...")
d.decir(mono, "Bien... ¡Mirá cómo salto !")

def hacer_que_el_mono_salte():
    mono.sonreir()
    mono.y = [300], 1

d.ejecutar(hacer_que_el_mono_salte)
d.decir(mono_chiquito, "wow...")

d.iniciar()
pilas.ejecutar()

