import pilas
pilas.iniciar()


t = pilas.actores.Temporizador()

def funcion_callback():
    pilas.avisar("Temporizador: el tiempo se acabo!")

# ajustamos que despues de 3 segundos llame a funcion_callback
t.ajustar(10, funcion_callback)

# iniciamos temporizador
t.iniciar()


pilas.ejecutar()
