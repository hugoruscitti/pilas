Dibujando en pantalla
=====================

Para dibujar en la pantalla se pude usar
un actor denominado ``Pizarra``. Este
actor es cómo un lienzo invisible sobre
el que podemos dibujar y observar trazos.

Por ejemplo, para crear la pizarra
dibujar un punto en el centro de la
pantalla se puede usar el siguiente
código:

.. code-block:: python

    pizarra = pilas.actores.Pizarra()
    pizarra.dibujar_punto(0, 0)


Dibujando usando lapices
------------------------

La pizarra tiene un componente interno que se
parece a un lapiz de color. Este lapiz
lo utilizaremos para dibujar sobre la
pizarra.

Este código es un ejemplo que imprime sobre
la pizarra una linea de color negro en diagonal:

.. code-block:: python

    pizarra = pilas.actores.Pizarra()
    pizarra.pintar_punto(0, 0)
    pizarra.bajar_lapiz()
    pizarra.mover_lapiz(100, 100)


