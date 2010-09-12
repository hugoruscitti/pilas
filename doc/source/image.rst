Manejo de imágenes
==================

En los videojuegos 2D las imágenes suelen estar en formatos
gráficos como **png** o **jpg** ya diseñados con anterioridad.

En ``pilas`` se pueden cargar estos recursos usando
el módulo ``imagenes``. Por ejemplo, si tenemos una
imagen llamada ``hola.png`` podríamos incorporarla a
nuestro juego así::

    import pilas

    hola = pilas.imagenes.cargar('hola.png')


Las imágenes no se imprimen directamente en pantalla, en
su lugar tienes que crear un Actor y asignarle la
imagen.

Por ejemplo, el siguiente código muestra la imagen
en pantalla:

.. code-block:: python

    import pilas

    imagen = pilas.imagenes.cargar("mi_personaje.png")
    actor = pilas.actores.Actor(imagen)


Grillas de imágenes
-------------------

Un forma conveniente de almacenar las imágenes de tus
personajes es usar una grilla.

La siguiente imagen es una grilla de 10 columnas
que utilizamos para crear al personaje "pingu":

.. image:: images/pingu.png


Internamente la imagen se almacena así, pero a la
hora de mostrarse en pantalla se puede seleccionar
el cuadro.


Este es un ejemplo que carga la grilla de mas arriba
y genera un actor para mostrar el cuadro 1:

.. code-block:: python

    actor = pilas.actores.Actor()
    animacion = pilas.imagenes.Grilla("pingu.png", 10)
    animacion.asignar(actor)

Luego, una vez que tienes asociado la grilla al actor, puedes
cambiar el cuadro de animación ejecutando las sentencias:

.. code-block:: python

    animacion.avanzar()
    animacion.asignar(actor)

Ten en cuenta que siempre tienes que llamar a al método
``asignar`` luego de hacer algo con la animación. De otra forma
no verás reflejado el cambio en el actor...
