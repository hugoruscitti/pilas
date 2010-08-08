Empezando, la primer prueba
===========================

Si ya tienes instalada la biblioteca podemos
comenzar a realizar nuestras primeras pruebas.

Para empezar, pilas se puede usar directamente
desde un intérprete iteractivo de python.

Iniciando la biblioteca
-----------------------

Ingresa en un terminal de tu sistema, inicia
el comando ``python`` y luego
ingresa la sentencia::

    import pilas

En tu pantalla tiene que aparecer una ventana
de color gris:

.. image:: images/cap1.png
    :width: 50%

Esa pantalla será la que utilizaremos para interactuar
con el motor. Y mas adelante será la única pantalla
que verán los usuarios de nuestros juegos.

Creando al primer personaje
---------------------------

Un concepto importante en ``pilas`` es del de ``actores``. Un
actor en pilas es un objeto que aparece en pantalla, tiene
una posición determinada y se puede manipular.

Por ejemplo, una nave, un enemigo, una medalla... etc.

Para agilizar el desarrollo de juegos se incluyen varios
actores dentro del motor, un de ellos es ``Monkey``.

Escriba la siguiente sentencia dentro del intérprete de
python:

.. code-block:: python

    mono = pilas.actors.Monkey()

En pantalla aparecerá un simpático personaje de color marrón:

.. image:: images/cap2.png
    :width: 50%

Adoptaremos a este personaje dentro de nuestro juego
bajo un nombre, en este caso ``mono``. Así que para indicarle
acciones solo tenemos que utilizar su nombre y sentencias
simples.

Por ejemplo, para que el personaje cambie su expresión
facil podemos usar sentencias cómo:


.. code-block:: python

    mono.smile()

o:

.. code-block:: python

    mono.shout()


En cualquiera de los dos casos el personaje
cambiará por algo cómo:

.. image:: images/mono/smile.png


Cosas en común para los actores
-------------------------------

Internamente, ``Monkey`` es un actor, así que encontraremos
mucha funcionalidad en él que la tendrán el resto de los
actores.

Veamos algunas de estas características:

- Podemos cambiar la posición de un actor mediante las propiedades ``x`` e ``y``:

.. code-block:: python

    mono.x = 100
    mono.y = 100

.. image:: images/mono/normal.png

- Todo actor tiene un atributo para indicar su tamaño en pantalla, el atributo ``scale`` (que originalmente vale 1):

.. code-block:: python

    mono.scale = 2


- También contamos con un atributo que indica la rotación en ángulos que debe tener el actor en pantalla. El atributo ``rotation``:


.. code-block:: python

    mono.rotation = 40

.. image:: images/mono/rotation40.png

o bien:

.. code-block:: python

    mono.rotation = 80

.. image:: images/mono/rotation80.png


Pidiendo ayuda
--------------

Recuerda que cada componente de ``pilas`` está documentado
como un módulo de python. Por lo tanto puedes
ejecutar una sentencia cómo:

.. code-block:: python

    help(mono)

y aparecerán en pantalla todos los instructivos de
la funcionalidad del actor.


Eliminando a un actor
---------------------

Para eliminar un actor de la escena tienes que llamar
al método ``kill``:


.. code-block:: python

    mono.kill()

Conclusión
----------

Hemos visto los pasos principales para gestionar
actores. Ten en cuenta que el módulo ``pilas.actors`` es
donde se guardarán todos los actores. Un buen ejercicio
es mirar ahí, buscar nuevos actores y comenzar a utilizarlos.
