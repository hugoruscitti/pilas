Cargar imágenes
===============

En los videojuegos 2d las imágenes suelen estar en formatos
gráficos como png o jpg ya diseñados con anterioridad.

En ``pilas`` se pueden cargar estos recursos usando
el módulo ``imagen``. Por ejemplo, si tenemos una
imágen llamada ``hola.png`` podríamos incorporarla a
nuestro juego así::

    import pilas

    hola = pilas.imagen.cargar('hola.png')


Las imágenes no se imprimen directamente en pantalla, en
su lugar tienes que crear un Actor y asignarle la
imagen.

Por ejemplo, el siguiente código muestra la imagen
en pantalla:

.. code-block:: python

    import pilas

    imagen = pilas.imagen.cargar("mi_personaje.png")
    actor = pilas.actores.Actor(imagen)
