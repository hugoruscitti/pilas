# -*- encoding: utf-8 -*-
# Pilas engine - A video game framework.
#
# Copyright 2010 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os
import sys
import time

from PySFML import sf

import actors
import image
import task_scheduler
import pytweener
import utils

tweener = pytweener.Tweener()

app = 1
event = 1
clock = 1

path = os.path.dirname(os.path.abspath(__file__))


    

tasks = task_scheduler.TaskScheduler() 
 
def add_task(time_out, function, *params): 
    tasks.add(time_out, function, params)


def loop():
    "Pone en funcionamiento el bucle principal."
    global app

    if app == 1:
        app = sf.RenderWindow(sf.VideoMode(640, 480), "Pilas")
        utils.float_child_window()

    event = sf.Event()
    clock = sf.Clock()
    bg_color = sf.Color(200, 200, 200)

    while True:
        time.sleep(0.01)

        tweener.update(16)
        tasks.update(app.GetFrameTime())
        app.Clear(bg_color)

        # Procesa todos los eventos.
        while app.GetEvent(event):
            if event.Type == sf.Event.KeyPressed:
                if event.Key.Code == sf.Key.Escape:
                    app.Close()
                    sys.exit(0)

        for actor in actors.all:
            actor.update()
            app.Draw(actor)

        app.Display()


def loop_bg():
    "Ejecuta el bucle de pilas en segundo plano."
    import threading

    bg = threading.Thread(target=loop)
    bg.start()


def load_autocompletation_modules():
    "Carga los modulos de python para autocompletar desde la consola interactiva."
    import rlcompleter
    import readline

    readline.parse_and_bind("tab: complete")


# Detecta si la biblioteca se esta ejecutando
# desde el modo interactivo o desde un script.

# Cuando inicia en modo interactivo se asegura
# de crear la ventana dentro del mismo hilo que
# tiene el contexto opengl.

try:
    cursor = sys.ps1
    load_autocompletation_modules()
    loop_bg()
except AttributeError:
    app = sf.RenderWindow(sf.VideoMode(640, 480), "Pilas")
    utils.float_child_window()
    utils.center_window(app)
