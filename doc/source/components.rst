Comportamientos
===============

Pilas permite añadir funcionalidad a tus objetos
de manera sencilla, dado que usamos el concepto
de comportamientos, un enfoque similar a la
programación orientada a componentes [#]_ y mixins [#]_.

.. [#] http://es.wikipedia.org/wiki/Programación_orientada_a_componentes
.. [#] http://es.wikipedia.org/wiki/Mixin


Un ejemplo
----------

Un comporamiento es una funcionalidad que está implementada
en alguna clase, y que si quieres la puedes vincular
a un actor cualquiera.

Veamos un ejemplo, imagina que tienes un actor en
tu escena y quieres que la rueda del mouse te permita
cambiarle el tamaño.

Puedes usar el comportamiento ``AumentarConRueda`` y vincularlo
al actor fácilmente.

El siguiente código hace eso:

.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()
    mono.aprender(pilas.comportamientos.AumentarConRueda)

así, cuando uses la rueda del mouse el tamaño del personaje aumentará
o disminuirá.

Nota que aquí usamos la metáfora de "aprender comportamientos", así
que te resultará sencillo recordarlo.


Un ejemplo mas: hacer que un actor sea arrastrable por el mouse
---------------------------------------------------------------

Algo muy común en los juegos es que puedas
tomar piezas con el mouse y moverlas por la pantalla.

El comportamiento ``Arrastrable`` representa eso, puedes vincularlo
a cualquier actor y simplemente funciona:

.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()
    mono.aprender(pilas.comportamientos.Arrastrable)


Otro ejemplo: un actor que cambia de posición
---------------------------------------------

Veamos otro ejemplo sencillo, si queremos que un actor
se coloque en la posición del mouse cada vez que hacemos
click, podemos usar el comportamiento: ``SeguirClicks``.

.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()
    mono.aprender(pilas.comportamientos.SeguirClicks)


Conflictos
----------

En pilas se ha intentado hacer que los comportamientos sean
lo mas independientes posibles, porque claramente lo mas
divertido de los componentes es poder combinarlos para
lograr comportamientos complejos.

Aún así, hay veces que dos componentes no se llevan bien...
Principalmente en esos casos donde ambos se suscriben
a la misma señal.

Si encuentras alguno de estos casos comentalo a los desarrolladores
en el foro de losersjuegos [#]_, así juntos buscamos una forma
de solucionarlo:

.. [#] http://www.losersjuegos.com.ar/foro



¿Cómo funciona?
---------------

Los comportamientos son clases normales, solo que se han
diseñado para representar funcionalidad y no entidades.

La vinculación con los actores se produce usando herencia
múltiple, una de las virtudes de python.

Así que internamente lo que sucede cuando ejecutas una
sentencia como::

    actor.aprender(pilas.comportamiento.Comportamiento)

es que la instancia de la clase actor pasa a tener una
superclase adicional, llamada ``Comportamiento``. 

A diferencia de la programación orientada a objetos
clásica, en ``pilas`` los objetos no guardan una
estrecha relación con una jerarquía de clases. Por el
contrario, los objetos se combinan a conveniencia, y
cada clase intenta tener solamente la mínima
funcionalidad que se necesita.
