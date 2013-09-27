Habilidades
===========

Pilas permite añadir funcionalidad a tus objetos
de manera sencilla, dado que usamos el concepto
de habilidades, un enfoque similar a la
programación orientada a componentes [#]_ y mixins [#]_.

.. [#] http://es.wikipedia.org/wiki/Programación_orientada_a_componentes
.. [#] http://es.wikipedia.org/wiki/Mixin


Un ejemplo
----------

Una habilidad es una funcionalidad que está implementada
en alguna clase, y que si quieres la puedes vincular
a un actor cualquiera.

Veamos un ejemplo, imagina que tienes un actor en
tu escena y quieres que la rueda del mouse te permita
cambiarle el tamaño.

Puedes usar la habilidad ``AumentarConRueda`` y vincularla
al actor fácilmente.

El siguiente código hace eso:

.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()
    mono.aprender(pilas.habilidades.AumentarConRueda)

así, cuando uses la rueda del mouse el tamaño del personaje aumentará
o disminuirá.

Nota que aquí usamos la metáfora de "aprender habilidades", porque
las habilidades son algo que duran para toda la vida
del actor.


Un ejemplo mas: hacer que un actor sea arrastrable por el mouse
---------------------------------------------------------------

Algo muy común en los juegos es que puedas
tomar piezas con el mouse y moverlas por la pantalla.

Esta habilidad llamada ``Arrastrable`` representa eso, puedes vincularlo
a cualquier actor y simplemente funciona:

.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()
    mono.aprender(pilas.habilidades.Arrastrable)


Otro ejemplo: un actor que cambia de posición
---------------------------------------------

Veamos otro ejemplo sencillo, si queremos que un actor
se coloque en la posición del mouse cada vez que hacemos
click, podemos usar la habilidad: ``SeguirClicks``.

.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()
    mono.aprender(pilas.habilidades.SeguirClicks)


Mezclar habilidades
-------------------

En pilas se ha intentado hacer que las habilidades sean
lo mas independientes posibles, porque claramente lo mas
divertido de este enfoque es poder combinar distintas
habilidades para lograr comportamientos complejos. 

Así que te invitamos a que pruebes y experimientes
mezclando habilidades.


Otras habilidades para investigar
---------------------------------

Pilas viene con varias habilidades incluidas, pero
lamentablemente este manual no las menciona a todas. Así
que te recomendamos abrir un intérprete de python
y consultarle directamente a él que habilidades tienes
diponibles en tu versión de pilas.


Para esto, abre un terminar de python y escribe lo siguiente:

.. code-block:: python

    import pilas
    pilas.iniciar()
    dir(pilas.habilidades)

esto imprimirá en pantalla todas las habilidades como una
lista de cadenas.





¿Cómo funcionan las habilidades?
--------------------------------

Las habilidades son clases normales de python, solo que se han
diseñado para representar funcionalidad y no entidades.

La vinculación con los actores se produce usando herencia
múltiple, una de las virtudes de python.

Así que internamente lo que sucede cuando ejecutas una
sentencia como::

    actor.aprender(pilas.habilidades.HabilidadDeEjemplo)

es que la instancia de la clase actor pasa a tener una
superclase adicional, llamada ``HabilidadDeEjemplo``. 

A diferencia de la programación orientada a objetos
clásica, en ``pilas`` los objetos no guardan una
estrecha relación con una jerarquía de clases. Por el
contrario, los objetos se combinan a conveniencia, y
cada clase intenta tener solamente la mínima
funcionalidad que se necesita.

Esta idea de combinación de objetos la hemos adoptado
de la programación orientada a componentes. Por lo
que puedes investigar en la red para conocer mas
acerca de ello.

¿Ideas?
-------

Si encuentras habilidades interesantes para desarrollar
te invitamos compartir tus ideas con las personas
que hacemos pilas y estamos en el foro de losersjuegos [#]_.

.. [#] http://www.losersjuegos.com.ar/foro


