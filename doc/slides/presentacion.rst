============================
Pilas, un motor hacer juegos
============================

:autor: Hugo Ruscitti
:resumen: Una breve reseña del proyecto, algunos ejemplos e ideas.


Introducción
------------

Pilas es una herramienta para hacer videojuegos de manera sencilla.

¿Por qué?
_________

- Hacer juegos debería ser mas sencillo.
- Queremos que mas gente haga juegos, incluso en la escuela.
- Nos encanta programar, hacer pilas es muy divertido !!

Características, objetivos
--------------------------

- Orientada a principiantes y programadores casuales.
- Viene con objetos pre-diseñados, llamados actores.
- Completamente en español.
- Es interactiva, para aprender realizando.
- Documentación con ejemplos orientada a resultados.


Un ejemplo
----------

Crear un personaje en la pantalla: 


.. code-block:: python

    import pilas

    pilas.iniciar()
    mono = pilas.actores.Mono()

Atributos
---------

Todos los actores tienen atributos
cómo: x, y, z, rotacion y escala.

.. code-block:: python

    mono.x = 100
    mono.escala = 3


Animaciones
-----------

Las animaciones mas simples se pueden
lograr mediante interpolaciones:

.. code-block:: python 

    mono.x = range(0, 300)
    mono.escala = [1, 4]
    mono.x = [-100]

o bien usando una forma mas sofisticada:

.. code-block:: python 

    mono.x = pilas.interpolar(100)
    mono.rotacion = pilas.interpolar([360, 128, 0], duracion=10)


Métodos
-------

Los actores también tienen comportamiento:

.. code-block:: python

    mono.sonreir()
    bomba.explotar()


.. image:: ../pilas/data/monkey_smile.png
    :width: 2cm

esto te permite crear un juego intercambiando mensajes entre actores.


Habilidades
-----------

Hay algo que todo actor puede hacer, interactuar
con el usuario. Para eso usamos **habilidades**.

Una **habilidad** es algo que el actor puede
aprender a hacer:

.. code-block:: python

    mono.aprender(pilas.habilidades.Arrastrable)
    mono.aprender(pilas.habilidades.AumentarConRueda)


Colisiones
----------

Para que los actores puedan interactuar
entre sí, generalmente se programan respuestas
a las colisiones.

Los radios de colisión se pueden ver pulsando
la tecla F12.

Y para que colisionen hay que seguir tres
pasos:

    - Crear la respuesta a la colisión en una función.
    - Agrupar los actores que van a colisionar en dos listas.
    - Avisarle a pilas que relacione la función con los grupos.


Colisiones, un ejemplo
----------------------

.. code-block:: python

    def comer(mono, banana):
        mono.sonreir()
        banana.eliminar()

    bananas = pilas.atajos.fabricar(pilas.actores.Banana, 40)

    pilas.colisiones.agregar(mono, bananas, comer)


Referencias
-----------

El sitio web de pilas:
    http://www.pilas-engine.com.ar

Sitio web de losersjuegos:
    http://www.losersjuegos.com.ar

Biblioteca SFML:
    http://www.sfml-dev.org
