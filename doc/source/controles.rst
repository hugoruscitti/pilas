Controles
=========

Si quieres conocer el estado de los controles
en pilas, tienes que usar el objeto ``pilas.mundo.control``.

Por ejemplo, para hacer que un actor
se mueva por la pantalla simplemente puedes crear
al actor y escribir estas sentencias.

.. code-block:: python

    if pilas.escena_actual().control.izquierda:
        mono.x -= 1
    elif pilas.escena_actual().control.derecha:
        mono.x += 1

Esta no es la única forma de mover a un personaje por
la pantalla, pero suele ser la mas conveniente porque
es muy directa, y se puede escribir en cualquier parte
del código.

.. note::
    Recuerda que para poder interactuar con el teclado, debes seleccionar la
    ventana de resultado. Haz click en la parte de arriba del intérprete de
    pilas para seleccionarla.

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

Esto te permite simplificar el código, porque no tienes que
conocer específicamente las teclas que activan cada acción, y en
todos los juegos serán las mismas teclas.


¿Dónde consultar los controles?
-------------------------------

El mejor lugar para consultar el estado de los controles
es en la actualización de un actor.

Esto se logra colocando un método llamado ``actualizar`` dentro
del actor y haciendo la consulta ahí. Veamos un
actor sencillo que se pueda mover de izquierda a derecha. El código sería
así:

.. code-block:: python

    import pilas

    pilas.iniciar()

    class MiActor(pilas.actores.Actor):

        def __init__(self):
            pilas.actores.Actor.__init__(self)
            self.imagen = pilas.imagenes.cargar("aceituna.png")

        def actualizar(self):
            if pilas.escena_actual().control.izquierda:
                self.x -= 10

            if pilas.escena_actual().control.derecha:
                self.x += 10

    MiActor()
    
    pilas.ejecutar() # Necesario al ejecutar en scripts.
