# http://en.wikipedia.org/wiki/File:Rayman_2_music_sample.ogg



# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
sys.path.insert(0, ".")

import pilasengine

pilas = pilasengine.iniciar()

sonido = pilas.musica.cargar("rayman.ogg")

def reproducir_sonido_cuando_hace_click(evento):
    sonido.reproducir()

pilas.escena_actual().click_de_mouse.conectar(reproducir_sonido_cuando_hace_click)

pilas.avisar("Pulse sobre la pantalla para emitir un sonido de explosion.")
pilas.ejecutar()
