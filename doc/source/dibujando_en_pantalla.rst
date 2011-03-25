Dibujando en pantalla
=====================

Pilas te permite dibujar figuras en la ventana
de muchas formas. En esta sección veremos las
posibilidades de ofrece pilas desde lo mas
simple a lo mas complejo.


Usando la Tortuga
=================

El actor ``Tortuga`` está inspirado en una de
las actividades mas divertidas y representativas
del lenguaje de programación logo, creado
por Seymour Papert.

La ``Tortuga`` básicamente es un actor que sabe
dibujar sobre la ventana de pilas. Para ello el
programador tiene que indicarle a la tortuga qué
movimiento tiene que hacer.

La siguiente imagen muestra lo que podría
dibujar la tortuga con algunas sentencias de
movimientos:

.. image:: images/tortuga_dibuja_triangulo.png

Como puedes ver en la imagen, el código que he
utilizado para crear la tortuga es el siguiente:

.. code-block:: python

    tortuga = pilas.actores.Tortuga()

    for x in range(36):
        tortuga.avanzar(5)
        tortuga.giraizquierda(10)

    tortuga.color = pilas.colores.verde
    tortuga.avanzar(200)


Inspeccionando a la tortuga
---------------------------

Para manejar a este actor tienes varios comandos
inspirados en logo.

Esta es una lista de los comandos mas utilizados:


+------------------+--------------+--------------------------------------+------------------------------------------------+
| Método completo  | nombre corto | ejemplo                              | ¿que hace?                                     |
+==================+==============+======================================+================================================+
| avanzar          | av           | tortuga.av(10)                       | avanza en dirección a donde mira la tortuga.   |
+------------------+--------------+--------------------------------------+------------------------------------------------+
| giraderecha      | gd           | tortuga.gd(45)                       | gira hacia la derecha los grados indicados.    |
+------------------+--------------+--------------------------------------+------------------------------------------------+
| giraizquierda    | gi           | tortuga.gi(45)                       | gira hacia la izquierda los grados indicados.  |
+------------------+--------------+--------------------------------------+------------------------------------------------+
| subelapiz        | sl           | tortuga.sl()                         | deja de dibujar cuando se mueve la tortuga.    |
+------------------+--------------+--------------------------------------+------------------------------------------------+
| bajalapiz        | bl           | tortuga.bl()                         | comienza a dibujar cuando la tortuga se mueve. |
+------------------+--------------+--------------------------------------+------------------------------------------------+
| pon_color        | pc           | tortuga.pc(pilas.colores.rojo)       | dibuja con el color indicado.                  |
+------------------+--------------+--------------------------------------+------------------------------------------------+
| pintar           | <<no tiene>> | tortuga.pintar(pilas.colores.blanco) | pinta toda la pantala del mismo color.         |
+------------------+--------------+--------------------------------------+------------------------------------------------+


Usando una Pizarra
==================


Si quieres dibujar sobre la pantalla pero
de forma inmediata y con mas posibilidades puedes
usar un actor llamado ``Pizarra``. Este
actor es cómo un lienzo invisible sobre
el que podemos pintar imágenes, figuras
geométricas y trazos de cualquier tipo.

A diferencia de la tortuga, la ``Pizarra``
te permite hacer muchos trazos rápidamente
y mostrarlos en pantalla todos a la vez. Además
te permite acceder a funciones avanzadas de dibujo
gracias a la biblioteca ``cairo``.

Comencemos con algo sencillo: para crear la pizarra y
dibujar un punto en el centro de la
pantalla se puede usar el siguiente
código:

.. code-block:: python

    pizarra = pilas.actores.Pizarra()
    pizarra.dibujar_punto(0, 0)


Dibujando usando lapices
------------------------

La pizarra tiene un componente interno que se
parece a un lápiz de color. Este lápiz
lo utilizaremos para dibujar sobre la
pizarra.

Este código es un ejemplo que imprime sobre
la pizarra una linea de color negro en diagonal:

.. code-block:: python

    pizarra = pilas.actores.Pizarra()
    pizarra.bajar_lapiz()
    pizarra.mover_lapiz(100, 0)
    pizarra.mover_lapiz(100, 100)
    pizarra.mover_lapiz(0, 0)

Así se verá:

.. image:: images/pizarra_dibuja_triangulo.png


De hecho, ahora que tienes el triangulo puedes
pulsar la tecla F12 y observar con mas claridad
dónde están situadas las puntas del triangulo:

.. image:: images/pizarra_dibuja_triangulo_modo_depuracion.png



Pintando imágenes
-----------------

Las pizarras también pueden dibujar imágenes sobre la superficie,
y esto es útil cuando quieras crear pinceles especiales sobre
la pizarra o construir un escenario usando bloques tipo
ladrillos.

Para pintar una imagen solo tienes que cargarla e
indicarla a la pizarra que la dibuje.

.. code-block:: python

    imagen = pilas.imagenes.cargar("pelota.png")
    pizarra.pintar_imagen(imagen, 0, 0)


Así se verá:

.. image:: images/pizarra_imagen.png


Ten en cuenta que la coordenada de la imagen es un poco
diferente a las coordenadas que vimos antes, cuando pintas
una imagen sobre una pizarra las coordenadas se dicen coordenadas
de pantalla. Eso significa que la posición (0, 0) es la esquina
superior izquierda. Los valores positivos de "x" son hacia la derecha
y los valores positivos de "y" van hacia abajo.


Pintando grillas de imágenes
----------------------------

De manera similar a las imágenes normales, sobre las pizarras
también se pueden pintar grillas.

Solamente tenemos que crear la grilla, seleccionar el
cuadro de animación y después decirle a la pizarra
que pinte el cuadro actual de la grilla:

.. code-block:: python

    grilla = pilas.imagenes.Grilla("pingu.png", 10)
    pizarra.pintar_grilla(grilla, 0, 0)

    grilla.definir_cuadro(2)
    pizarra.pintar_grilla(grilla, 100, 100)

    grilla.definir_cuadro(3)
    pizarra.pintar_grilla(grilla, 200, 200)

Así se verá:

.. image:: images/pizarra_grilla.png

Esto es útil cuando se quieren pintar bloques de un escenario
completo, por ejemplo podríamos tener una grilla con distintos
tipos de suelos (pasto, piedra, tierra) y luego ir
imprimiendo sobre una pizarra para formar un escenario completo.

Ten en cuenta que al igual que la impresión de imágenes, aquí también
las coordenadas se comportan un poco distinto, tienes que
usar coordenadas de pantalla. Observa la sección anterior
para tener mas detalle de las coordenadas de pantalla.


La pizarra como actor
---------------------

Recuerda que la pizarra también es un actor, así que puedes enseñarle
habilidades, cambiar su posición, rotación o lo que quieras.


Dibujo avanzado sobre la pizarra usando Cairo
---------------------------------------------

El actor pizarra tiene varios métodos para dibujar, y
son simples de utilizar. Pero en algunas oportunidades
puede que quieras hacer algo mas complejo, que la pizarra
no sabe hacer.

Por ejemplo, imagina que quieres imprimir un gráfico vectorial, o
pintar un rectángulo con esquinas redondeadas o un degradé circular.

Para operaciones de dibujo complejas, puedes usar la biblioteca
``cairo``, la biblioteca que usa ``pilas`` para representar a la
pizarra y permitirte dibujar una imagen sobre otra.


Entonces, para dibujar de manera avanzada sobre la pizarra
tienes que incorporar la biblioteca cairo, dibujar sobre el
contexto de la pizarra y luego invocar al método ``actualizar_imagen``.

Lo que sigue es un ejemplo que dibujar sobre la pizarra
usando cairo:

.. code-block:: python

    
    # paso 1: crear la pizarra
    pizarra = pilas.actores.Pizarra()

    # paso 2: comienza el dibujo personalizado con cairo:
    import cairo

    x1, y1 = (100, 100)
    x2, y2 = (600, 300)
    x3, y3 = (100, 400)

    pizarra.canvas.context.curve_to(x1, y1, x2, y2, x3, y3)
    pizarra.canvas.context.set_line_width(50)
    pizarra.canvas.context.set_dash([10])
    pizarra.canvas.context.stroke()

    # paso 3: Decirle a la pizarra que se actualice.
    pizarra.actualizar_imagen()

Es decir, el resultado será una curva que pasa por los
puntos (x1, y1), (x2, y2) y por último (x3, y3):

.. image:: images/pizarra_avanzado_cairo.png


Si quieres obtener mas información sobre las posibilidades
que te ofrece cairo, puedes consultar los siguientes sitios
web:

- http://cairographics.org/pycairo/
- http://cairographics.org/samples/
- http://www.tortall.net/mu/wiki/CairoTutorial

Y si encuentras algo útil que se pueda simplificar mejorando
la pizarra avísanos!.



Dibujando mas rápido
--------------------

Si quieres hacer dibujos complejos, con muchos trazos o formas,
seguramente notarás que la pizarra no es tan rápida como
debería.

Resulta que la pizarra, cuando se utiliza normalmente, muestra
en cada momento el trazo que realizamos o cualquier dibujo
que realicemos. Esto funciona así porque la mayoría de los
usuarios quieren dibujar y observar su resultado inmediatamete, 
de forma interactiva.

Si quieres dibujar mas rápidamente puedes hacer lo siguiente: dile
a la pizarra que deshabilite el dibujado interactivo, realiza
todos los trazos que quieras, y luego habilita nuevamente el
dibujado interactivo. Esto producirá resultados mas rápidos
y directos.

Aquí hay un ejemplo de dibujado rápido.

.. code-block:: python

    pizarra.deshabilitar_actualizacion_automatica()

    # dibuja 64 puntos sobre la pizarra.
    for i in range(0, 640, 10):
        pizarra.dibujar_punto(x=i, y=i)

    pizarra.habilitar_actualizacion_automatica()


Ten en cuenta que la pizarra pasará, de un instante a otro, a
tener los 64 puntos que dibujamos. Así que si usas este
código desde la consola interactiva, solo verás los
resultados cuando ejecutes la sentencia
``pizarra.habilitar_actualizacion_automatica``.
