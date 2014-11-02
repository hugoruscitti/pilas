import pilas
import random

pilas.iniciar(titulo="Asteroides")






# Inicia la escena actual.
from . import escena_menu
pilas.cambiar_escena(escena_menu.EscenaMenu())
pilas.ejecutar()
