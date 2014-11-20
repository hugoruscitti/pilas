# -*- encoding: utf-8 -*-

# Importat la librería 
import pilas
from pilas.utils import obtener_ruta_al_recurso
pilas.iniciar()


# Definición de actores
b = pilas.actores.Board("/dev/tty/USB0")
r = pilas.actores.Robot(b, 1)

# Cargar el fondo a evaluar


pilas.fondos.FondoPersonalizado(obtener_ruta_al_recurso('robot_sensor_lineas.png'))    

# Avance del robot
r.forward()

# Recprre hasta que el valor del sensor de línea obtenga el valor:255.0
iq, dr = r.getLine()  
while  iq != 255.0 and  dr != 255.0 :
    iq, dr = r.getLine()
    print iq, dr

r.stop()
pilas.ejecutar()
