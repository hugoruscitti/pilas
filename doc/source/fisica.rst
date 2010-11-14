Física
======

Pilas incluye integración con un sistema de física
para realizar simulaciones y dotar a tus juegos
de mas realismo y diversión.


Instalar pymunk
---------------

Quien realiza todo el trabajo de simulación es
el módulo ``pilas.fisica``, que a su vez delega
todas las tareas a una biblioteca llamada pymunk.

Por lo tanto es necesario que tu sistema tenga
instalado pymunk para funcionar correctamente.

Te recomiendo instalar pymunk de la siguiente
manera, ejecuta el comando::

    sudo easy_install pymunk

Una vez instalada la biblioteca, tendrías que poder
asegurarte de todo funciona correctamente usando
el intérprete de python::

    python
    >>> import pymunk
    >>> pymunk.version
    '1.0.0'


Un ejemplos
-----------

El motor de física se puede mostrar en funcionamiento
usando un ejemplo, escribe el siguiente código:

.. code-block:: python

    pelotas = pilas.atajos.fabricar(pilas.actor.Pelota, 30)

esto creará un grupo de circunferencias que rebotarán
hasta la parte inferior de la pantalla.
