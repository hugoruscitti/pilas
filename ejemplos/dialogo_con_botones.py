import pilas

pilas.iniciar()

# Genera al personaje que habla
aceituna = pilas.actores.Aceituna(x=-100)


# Se crean los dos botones.
b1 = pilas.actores.Boton(x=100, y=50)
b2 = pilas.actores.Boton(x=100, y=-50)


# Generamos el administrador de los dialogos.
dialogo = pilas.actores.Dialogo()


# Ahora las acciones que vamos a ejecutar cuando
# se pulsan los botones.

def cuando_pulsa_el_boton(texto):
    dialogo.decir(aceituna, "Has pulsado: " + texto)
    dialogo.iniciar()


# Y conectamos las funciones con los botones.
b1.conectar_presionado(cuando_pulsa_el_boton, "boton de arriba")
b2.conectar_presionado(cuando_pulsa_el_boton, "boton de abajo")

pilas.avisar("Pulsa alguno de los botones")
pilas.ejecutar()
