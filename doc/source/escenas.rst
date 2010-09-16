Escenas
=======

Las escenas te permiten dividir el juego en partes
reconocibles y que interactúan de manera diferente
con el usuario.


Algunas observaciones:

- La escena actual siempre está señalada por el atributo ``pilas.escena``.
- Solo puede existir una escena a la vez.
- Cuando se cambia de escena, se borran todos los objetos que viven en ella.


La escena Normal
----------------

Cuando iniciamos pilas por primera vez se creará
una escena llamada ``Normal``. Esta escena no
tiene un comportamiento muy elaborado, simplemente
imprime toda la pantalla de gris para que
podamos colocar actores sobre ella.


Otras escenas
-------------

Para hacer un pequeña prueba sobre otra escena
podrías ejecutar la siguiente sentencia
de código:

.. code-block:: python

    pilas.escenas.Paisaje()

Esto borrará a todos los actores de la escena
y aplicará un nuevo fondo de pantalla a la 
ventana de pilas:

.. image:: images/paisaje.png
