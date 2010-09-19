Controles
=========

Si quieres conocer el estado de los controles
en pilas tienes que usar el objeto ``pilas.mundo.control``.

Por ejemplo, para hacer que un actor
se mueva por la pantalla simplemente puedes crear
al actor y escribir estas sentencias.

.. code-block:: python

    if pilas.mundo.control.izquierda:
        mono.x -= 1
    elif pilas.mundo.control.derecha:
        mono.x += 1


Investigando al objeto control
------------------------------

En realidad, cuando usamos a ``pilas.mundo.control``, accedemos
a un objeto que tienen varios atributos.

Estos atributos pueden valer ``True`` o ``False``, dependiendo
de la pulsación de las teclas:

- izquierda
- derecha
- arriba
- abajo
- boton


