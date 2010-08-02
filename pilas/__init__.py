# -*- encoding: utf-8 -*-
import sys
import time

from PySFML import sf

app = 1
event = 1
clock = 1





def exit():
    "Termina la ejecución de la biblioteca."
    sys.exit(0)


def loop():
    "Pone en funcionamiento el bucle principal."
    global app

    if app == 1:
        app = sf.RenderWindow(sf.VideoMode(640, 480), "Pilas")

    event = sf.Event()
    clock = sf.Clock()
    bg_color = sf.Color(200, 200, 200)

    while True:
        time.sleep(0.1)

        app.Clear(bg_color)

        # Procesa todos los eventos.
        while app.GetEvent(event):
            if event.Type == sf.Event.KeyPressed:
                if event.Key.Code == sf.Key.Escape:
                    exit()

        app.Display()


def loop_bg():
    "Ejecuta el bucle de pilas en segundo plano."
    import threading

    bg = threading.Thread(target=loop)
    bg.start()



# Detecta si la biblioteca se esta ejecutando
# desde el modo interactivo o desde un script.

# Cuando inicia en modo interactivo se asegura
# de crear la ventana dentro del mismo hilo que
# tiene el contexto opengl.

try:
    cursor = sys.ps1
    loop_bg()
except AttributeError:
    app = sf.RenderWindow(sf.VideoMode(640, 480), "Pilas")
