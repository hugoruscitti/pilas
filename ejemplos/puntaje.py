import pilas
pilas.iniciar()


puntaje = pilas.actores.Puntaje()



texto = pilas.actores.Texto('Puntaje:')
texto.x = -80
texto.y = -2

# variables que modificaremos en el juego
class variables:
    c = 0

def sumar_5_al_clickear(evento):
    # sumamos 5 a la variable
    variables.c = variables.c + 5
    
    # mostramos por pantalla los cambios en nuestra variable
    puntaje.definir(variables.c)

pilas.eventos.click_de_mouse.conectar(sumar_5_al_clickear)
pilas.avisar('Clickea la pantalla y agregaras 5 puntos al puntaje')

pilas.ejecutar()
