Escenas
=======

Las escenas te permiten dividir el juego en partes
reconocibles y que interactúan de manera diferente
con el usuario.

Algunas observaciones:

- La escena actual siempre está señalada por el atributo ``pilas.escena``.
- Solo puede existir una escena a la vez.
- Cuando se cambia de escena, generalmente la misma escena eliminará a todos los actores del escenario.


La escena Normal
----------------

Cuando iniciamos pilas por primera vez se creará
una escena llamada ``Normal``. Esta escena no
tiene un comportamiento muy elaborado, simplemente
imprime toda la pantalla de gris para que
podamos colocar actores sobre ella.


Cambiando el fondo de las escenas
---------------------------------

Para hacer un pequeña prueba sobre una
escena, podrías ejecutar la siguiente sentencia
de código:

.. code-block:: python

    pilas.fondos.Volley()

Esto le dará a tu escena una vista
mas agradable, porque carga un fondo de
pantalla colorido y mas divertido:

.. image:: images/paisaje.png
    :width: 15cm
