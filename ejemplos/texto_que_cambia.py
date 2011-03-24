import pilas

pilas.iniciar()

texto = pilas.actores.Texto("Bienvenido.")

def cuando_pulsa_el_boton():
    texto.definir_texto("Has pulsado el boton")

b = pilas.actores.Boton(y=-100)
b.conectar_presionado(cuando_pulsa_el_boton)

pilas.avisar("Pulsa el boton para que cambie el texto.")
pilas.ejecutar()
