Dibujando en pantalla
=====================

Para dibujar en la pantalla se pude usar
un actor denominado ``Pizarra``. Este
actor es cómo un lienzo invisible sobre
el que podemos pintar imágenes, figuras
geométricas y trazos de cualquier tipo.

Por ejemplo, para crear la pizarra y
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
