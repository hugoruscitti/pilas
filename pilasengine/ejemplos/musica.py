# http://en.wikipedia.org/wiki/File:Rayman_2_music_sample.ogg



# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
sys.path.insert(0, "../..")
sys.path.insert(0, ".")

import pilasengine

sonido_wav = None
sonido_ogg = None

pilas = pilasengine.iniciar()

try:
    sonido_wav = pilas.musica.cargar("rayman.wav")
except:
    print("Imposible leer el archivo .wav")

try:
    sonido_ogg = pilas.musica.cargar("rayman.ogg")
except:
    print("Imposible leer el archivo .ogg")


boton_wav = pilas.interfaz.Boton("Reproducir .wav")
boton_wav.x = -100

boton_ogg = pilas.interfaz.Boton("Reproducir .ogg")
boton_ogg.x = 100

def reproducir_wav():
    if not sonido_wav:
        boton_wav.decir("No se pudo cargar el archivo ogg")
    else:
        sonido_wav.reproducir()

def reproducir_ogg():
    if not sonido_ogg:
        boton_ogg.decir("No se pudo cargar el archivo ogg")
    else:
        sonido_ogg.reproducir()

boton_wav.conectar(reproducir_wav)
boton_ogg.conectar(reproducir_ogg)
pilas.actores.Sonido()

pilas.ejecutar()
