.. image::
    logo.png
    :align: left
    :width: 8cm

Guía de referencia
==================

Pilas es un motor de videojuegos sencillo, escrito en python
y orientado a principiantes.

Iniciar
-------

Para empezar puedes escribir ``import pilas``, y luego usar alguna
de las siguientes funciones:

iniciar(ancho=640, alto=480, titulo='Pilas')
    inicia la biblioteca si estas usando un script.
pilas.pausa()
    para detener el juego (lo mismo que hace la tecla 'p').
pilas.terminar()
    para cerrar la ventana (su atajo es la tecla 'q')
pilas.ejecutar()
    para poner en funcionamiento la biblioteca desde script.

Uso básico de Actores
---------------------

Los actores te permiten representar personajes facilmente y comenzar
rápidamente.

Para crear un actor tienes que escribir algo cómo:

.. code-block:: python

    mono = pilas.actores.Mono()

y cada actor tiene atributos cómo:

- x
- y
- rotacion
- escala

por ejemplo:

.. code-block:: python

    mono.escala = 2
    mono.x = 200

Y como cada actor es un objeto, también entienden
mensajes cómo:

.. code-block:: python

    mono.sonreir()

usa el comando ``help(mono)`` para concer mas de
este actor.


Otros actores
-------------

- Mono
- Bomba
- Tortuga
- Banana
- Pingu

Atajos de teclado
-----------------

La pantalla principal de pilas tiene algunos atajos útiles:

F12
    Habilita el modo depuración.
P
    Pone la simulación en pausa.
Q
    Cierra la ventana y termina el programa.

Movimientos
-----------

Para simular movimientos puedes usar la función ``interpolar``:

pilas.interpolar(valor_o_valores, duracion=1, demora=0, tipo='lineal')
    busca todos los valores intermedios entre los valores que se le indican
    como parametro y el atributo que recibirá modificaciones.

Por ejemplo:

.. code-block:: python
    
    mono.rotacion = pilas.interpolar(360)
    mono.x = pilas.interpolar([-200, 200, 0], duracion=2)

Habilidades
-----------

Las habilidades permite dotar a los actores de características
que le permite interacturar con el usuario.

Algunas habilidades son:

- SeguirAlMouse
- AumentarConRueda
- SeguirClicks
- Arrastrable
- MoverseConElTeclado

Referencias
-----------

 * http://www.pilas-engine.com.ar
 * http://www.losersjuegos.com.ar
