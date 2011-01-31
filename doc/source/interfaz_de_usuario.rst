Interfaz de usuario
===================

Pilas incluye un submódulo que te permitirá crear
una interfaz de usuario con deslizadores, botones, cajas
de texto y selectores.

Este submódulo tiene objetos basados en actores, así que
lo que conoces sobre actores vas a poder usarlo para construir
una interfaz.


Deslizador
----------

El deslizador es útil para que el usuario pueda seleccionar
un valor intermedio entre dos números, por ejemplo entre 0 y 1, 0 y
100 etc.

Un ejemplo típico de este componente puedes encontrarlo
en las preferencias de audio de algún programa de sonido, los
deslizadores te permiten regular el grado de volúmen.


Esta es una imagen del ejemplo ``deslizador.py`` que está
en el directoio ``ejemplos``. Tiene tres deslizadores, y
el usuario puede regular cualquiera de los tres para ver
los cambios en el actor:

.. image:: images/deslizador.png


Para construir un deslizador y asociarlo a una función
puedes escribir algo como esto:

.. code-block:: python

    def cuando_cambia(valor):
        print "El deslizador tiene grado:", valor

    deslizador = pilas.interfaz.Deslizador()
    deslizador.conectar(cuando_cambia)


Entonces, a medida que muevas el deslizador se imprimirán
en pantalla valores del 0 al 1, por ejemplo 0.25, 0.52777 etc...


Si quieres cambiar los valores iniciales y finales de la 
escala de valores, lo mas sencillo es multiplicar el argumento
``valor`` de la función. Por ejemplo, si quieres valores entre
0 y 100:

.. code-block:: python

    def cuando_cambia(valor):
        valor_entre_cero_y_cien = valor * 100
        
