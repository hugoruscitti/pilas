# -*- encoding: utf-8 -*-
import sys
from PySFML import sf


app = sf.RenderWindow(sf.VideoMode(640, 480), "Pilas")
event = sf.Event()
clock = sf.Clock()
bg_color = sf.Color(200, 200, 200)


def exit():
    "Termina la ejecución de la biblioteca."
    app.Close()
    sys.exit(0)


def loop():
    "Pone en funcionamiento el bucle principal."

    while True:
        app.Clear(bg_color)

        # Procesa todos los eventos.
        while app.GetEvent(event):
            if event.Type == sf.Event.KeyPressed:
                if event.Key.Code == sf.Key.Escape:
                    exit()

        app.Display()
