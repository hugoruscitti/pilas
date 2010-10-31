.. image::
    logo.png
    :align: left
    :width: 7cm

Guía de referencia
==================

Pilas es un motor de videojuegos sencillo, escrito en python
y orientado a principiantes.

Iniciar
-------

Para empezar puedes escribir ``import pilas``, y luego usar alguna
de las siguientes funciones:

iniciar(ancho=640, alto=480, titulo='Pilas', usar_motor='sfml')
    inicia la biblioteca y la ventana principal. Los valores de usar_motor pueden ser 'sfml' o 'pygame'.
pilas.pausa()
    para detener el juego (lo mismo que hace la tecla 'p').
pilas.terminar()
    para cerrar la ventana (su atajo es la tecla 'q')
pilas.ejecutar()
    para poner en funcionamiento la biblioteca desde script.
pilas.fabricar(clase, cantidad=1)
    genera muchos objetos de una clase particular asignandolo una posicion aleatoria.

Uso básico de Actores
---------------------

Los actores te permiten representar personajes fácilmente y comenzar
rápidamente.

Para crear un actor tienes que escribir algo cómo:


.. code-block:: python

    mono = pilas.actores.Mono()

y cada actor tiene atributos cómo: x, y, z, rotacion, escala.

Por ejemplo:

.. code-block:: python

    mono.escala = 2
    mono.x = 200

Y como cada actor es un objeto, también entienden
mensajes cómo:

.. code-block:: python

    mono.sonreir()

usa el comando ``help(mono)`` para conocer mas de
este actor.


Otros actores
-------------

Mono, Bomba, Tortuga, Banana, Pingu, Animacion ... 

Atajos de teclado
-----------------

La pantalla principal de pilas tiene algunos atajos útiles:

    **F12**  Habilita el modo depuración.

    **P**    Pone la simulación en pausa.

Movimientos
-----------

Para simular movimientos puedes usar la función ``interpolar``:

pilas.interpolar(valor_o_valores, duracion=1, demora=0, tipo='lineal')
    busca todos los valores intermedios entre los valores que se le indican
    como parámetro y el atributo que recibirá modificaciones.

Por ejemplo:

.. code-block:: python
    
    mono.rotacion = pilas.interpolar(360)
    mono.x = pilas.interpolar([-200, 200, 0], duracion=2)

Habilidades
-----------

Las habilidades permite dotar a los actores de características
que le permite interactuar con el usuario.

Algunas habilidades son:

- SeguirAlMouse
- AumentarConRueda
- SeguirClicks
- Arrastrable
- MoverseConElTeclado

y se pueden anexar a los actores así:

.. code-block:: python

    mono.aprender(pilas.habilidades.Arrastrable)

Colisiones
----------

Primero tienes que hacer la función de respuesta a la colisión:

.. code-block:: python

    def toca_bomba(mono, bomba):
        mono.gritar()
        bomba.explotar()

y luego crear los actores en una lista y asociarlos al
sistema de colisiones:

.. code-block:: python

    mono = pilas.actores.Mono()
    bomba = pilas.actores.Bomba()
    bomba2 = pilas.actores.Bomba()
    bomba2.x = 200

    bombas = [bomba, bomba2]

    pilas.colisiones.agregar(mono, bombas, toca_bomba)



Referencias
-----------

 * http://www.pilas-engine.com.ar
 * http://www.losersjuegos.com.ar
