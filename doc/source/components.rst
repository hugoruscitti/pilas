Componentes
===========

Pilas te permite añadir funcionalidad a tus objetos
de manera sencilla, dado que usamos el concepto
de componentes y mixins.


Un ejemplo
----------

Un componente es una funcionalidad que está implementada
en alguna clase, y que si quieres la puedes vincular
a un actor cualquiera.

Veamos un ejemplo, imagina que tienes un actor en
tu escena y quieres que la rueda del mouse te permita
cambiarle el tamaño.

Puedes usar el componente ``SizeByWheel`` y vincularlo
al actor fácilmente.

El siguiente código hace eso:

.. code-block:: python

    import pilas

    mono = pilas.actors.Monkey()
    mono.mixin(pilas.components.SizeByWheel)

así, cuando uses la rueda del mouse el tamaño del personaje aumentará
o disminuirá.



Un ejemplo mas: hacer que un actor sea arrastrable por el mouse
---------------------------------------------------------------

Algo muy común en los juegos es que puedas
tomar piezas con el mouse y moverlas por la pantalla.

El componente ``Draggable`` te permite hacer eso, puedes vincularlo
a cualquier actor y simplemente funciona:

.. code-block:: python

    import pilas

    mono = pilas.actors.Monkey()
    mono.mixin(pilas.components.Draggable)


Otro ejemplo: un actor que cambia de posición
---------------------------------------------

Veamos otro ejemplo sencillo, si queremos que un actor
se coloque en la posición del mouse cada vez que hacemos
click, podemos usar el componente: ``FollowMouseClicks``.

.. code-block:: python

    import pilas

    mono = pilas.actors.Monkey()
    mono.mixin(pilas.components.FollowMouseClicks)


Conflictos
----------

En pilas se ha intentado hacer que los componentes sean
lo mas independientes posibles, porque claramente lo mas
divertido de los componentes es poder combinarlos para
lograr comportamientos complejos.

Aún así, hay veces que dos componentes no se llevan bien... Principalmente
en esos casos donde ambos se suscriben a la misma señal.

Si encuentras alguno de estos casos comentalo a los desarrolladores
en el foro de losersjuegos, así juntos buscamos una forma
de solucionarlo:

http://www.losersjuegos.com.ar/foro



¿Cómo funciona?
---------------

Los componentes son clases normales, solo que se han
diseñadas para representar comportamiento en lugar de
entidades.

La vinculación con los actores se produce usando herencia
múltiple, una de las virtudes de python.

Así que internamente lo que sucede cuando ejecutas una
sentencia como::

    actor.mixin(pilas.components.Component)

es que la instancia de la clase actor pasa a tener una
superclase adicional, llamada ``Component``. 

A diferencia de la programación orientada a objetos
clásica, en ``pilas`` los objetos no guardan una
estrecha relación con una jerarquía de clases. Por el
contrario, los objetos se combinan a conveniencia, y
cada clase intenta tener solamente la mínima
funcionalidad que se necesita.
