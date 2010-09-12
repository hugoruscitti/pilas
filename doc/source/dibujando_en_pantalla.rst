Dibujando en pantalla
=====================

Para dibujar en la pantalla se pude usar
un actor denominado ``Pizarra``. Este
actor es cómo un lienzo invisible sobre
el que podemos dibujar y observar trazos.

Por ejemplo, para crear el actor y
dibujar un punto en el centro de la
pantalla se puede usar el siguiente
código:

.. code-block:: python

    pizarra = pilas.actores.Pizarra()
    pizarra.dibujar_punto(0, 0)


Y para hacer algo mas complejo como dibujar
un cuadrado se puede escribir:

.. code-block:: python

    pizarra.dibujar_cuadrado(0, 0, 20)

donde ``20`` indica que el tamaño del cuadrado
será de ``20`` pixels de ancho y ``20`` pixels de
alto.
