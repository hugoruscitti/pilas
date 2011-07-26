import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()


puntaje = pilas.actores.Puntaje()


texto = pilas.actores.Texto('Puntaje:')
texto.x = -80
texto.y = -2

def sumar_5_al_clickear(evento):
    puntaje.aumentar(5)
    
pilas.eventos.click_de_mouse.conectar(sumar_5_al_clickear)
pilas.avisar('Clickea la pantalla y agregaras 5 puntos al puntaje')

pilas.ejecutar()
