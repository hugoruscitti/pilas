Textos
======

Los mensajes de texto se tratan de manera similar
a los actores. Por lo tanto, si ya sabes usar
actores, no tendrás problemas en usar cadenas
de texto.


Crear cadenas de texto
----------------------

El objeto que representa texto se llama ``Text`` y
está dentro del modulo ``actors``.

Para crear un mensaje tienes que escribir:

.. code-block:: python

    texto = pilas.actors.Text("Hola, este es mi primer texto.")

y tu cadena de texto aparecerá en pantalla en color
negro y con un tamaño predeterminado:

.. image:: images/texto.png


Si quieres en la cadena de texto puedes usar caracteres
especiales como ``\n`` para colocar un salto de linea.

Los textos son actores
----------------------

Al principio comenté que los textos también son actores, esto
significa que casi todo lo que puedes hacer con un actor
aquí también funciona, por ejemplo:

.. code-block:: python

    texto.x = 100
    texto.scale = 2

incluso también funcionarán las interpolaciones:

.. code-block:: python

    texto.rotation = pilas.interpolate(360)


Propiedades exclusivas de los textos
------------------------------------

Existen varias propiedades que te permitirán alterar la
apariencia de los textos.

Esta es una lista de los mas importantes.

- color
- size
- text

Por ejemplo, para alterar el texto, color y tamaño de un
texto podría escribir algo así:

.. code-block:: python

    texto.size = 50
    texto.color = (0, 0, 0)   # Color negro
    texto.color = (255, 0, 0, 128)   # Color rojo, semi transparente.
    texto.text = "Hola, este texto \n tiene 2 lineas separadas"

