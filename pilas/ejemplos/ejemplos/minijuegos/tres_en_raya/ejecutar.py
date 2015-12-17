import pilas

pilas.iniciar(titulo = "3 en Raya")





# ejecuta escena actual.
from . import escena_menu
pilas.cambiar_escena(escena_menu.EscenaMenu())

pilas.ejecutar()
