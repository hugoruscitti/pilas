Manejo de imágenes
==================

En los videojuegos 2D las imágenes suelen estar en formatos
gráficos como **png** o **jpg** ya diseñados con anterioridad.

En ``pilas`` se pueden cargar estos recursos usando
el módulo ``imagenes``. Por ejemplo, si tenemos una
imagen llamada ``hola.png`` podríamos incorporarla a
nuestro juego así:

.. code-block:: python

    import pilas

    hola = pilas.imagenes.cargar('hola.png')


Las imágenes no se imprimen directamente en pantalla, en
su lugar tienes que crear un Actor y asignarle la
imagen.

Por ejemplo, el siguiente código muestra la imagen
en pantalla:

.. code-block:: python

    import pilas

    imagen = pilas.imagenes.cargar("mi_personaje.png")
    actor = pilas.actores.Actor(imagen)


Grillas de imágenes
-------------------

Un forma conveniente de almacenar las imágenes de tus
personajes es usar una grilla.

La siguiente imagen es una grilla de 10 columnas
que utilizamos para crear al personaje "pingu":

.. image:: images/pingu.png


Internamente la imagen se almacena así, pero a la
hora de mostrarse en pantalla se puede seleccionar
el cuadro.


Este es un ejemplo que carga la grilla de mas arriba
y genera un actor para mostrar el cuadro 1:

.. code-block:: python

    actor = pilas.actores.Actor()
    animacion = pilas.imagenes.Grilla("pingu.png", 10)
    animacion.asignar(actor)

Luego, una vez que tienes asociado la grilla al actor, puedes
cambiar el cuadro de animación ejecutando las sentencias:

.. code-block:: python

    animacion.avanzar()
    animacion.asignar(actor)

Ten en cuenta que siempre tienes que llamar a al método
``asignar`` luego de hacer algo con la animación. De otra forma
no verás reflejado el cambio en el actor...


Mas detalles sobre grillas
__________________________

En el ejemplo anterior usamos una grilla sin dar muchos detalles
sobre la grilla, pero resulta que en python tienes la oportunidad
de ser mas preciso y obtener mas funcionalidad de las grillas.

El objeto grilla recibe mas parámetros, por ejemplo si tu grilla
tiene filas y columnas puedes especificar las filas
y columnas de esta forma:

.. code-block:: python

    animacion = pilas.imagenes.Grilla("pingu.png", 10, 5)

donde 10 es el número de columnas en la grilla y 5 es la
cantidad de filas.


Haciendo animaciones sencillas
______________________________

En muchas oportunidades nos interesa hacer animaciones simples
y que se repitan todo el tiempo sin mucho esfuerzo. Pilas
incluye un actor llamado ``Animacion`` precisamente para
estos casos.

Por ejemplo, imagina que tienes una animación de un fuego
que te gustaría repetir todo el tiempo:

.. image:: images/grilla_fuego.png

Esta imagen de grilla tiene ``6`` cuadros de animación organizada
mediante columnas.

Una forma sencilla de convertir esta animación en un actor
simple es crear la grilla, construir un actor ``Animacion`` e
indicarle a pilas que será una animación cíclica, es decir, que
se tendrá que repetir indefinidamente:


.. code-block:: python

    grilla = pilas.imagenes.Grilla("fuego.png", 6)
    actor = pilas.actores.Animacion(grilla, ciclica=True)


El resultado en la ventana será una animación de fuego que
no terminará nunca. Cuando el actor termine de mostrar el
cuadro 6 de la animación regresará al primero para comenzar
nuevamente.

Otra posibilidad es especificar el argumento ``ciclica=False``. En
ese caso el actor comenzará a mostrar la animación desde el cuadro
1 y cuanto termine eliminará al actor de la ventana. Esto es útil
para hacer efectos especiales, como explosiones o destellos, cosas
que quieres tener en la ventana un instante de tiempo.


Haciendo actores con animación
------------------------------

Puede que quieras hacer un actor que tenga múltiples animaciones, y
que las muestre en determinados momentos. Por ejemplo, si tienes
una nave con motores, es probable que quieras mostrar una animación
de motores en funcionamiento cuando la nave avanza y detener la
animación de motores cuando finaliza el movimiento.

Una forma de lograr esto de manera sencilla es crear tu propio
actor, y que este tenga dos atributos, uno para cada animación:


.. code-block:: python

    class MiNave(pilas.actores.Actor):

        def __init__(self, x=0, y=0):
            Actor.__init__(self, x=x, y=y)
            self.animacion_detenida = pilas.imagenes.Grilla("nave_detenida.png", 1)
            self.animacion_movimiento = pilas.imagenes.Grilla("nave_en_movimiento.png", 3)


Luego, en el método ``actualizar`` del propio actor podrías
avanzar la animación actual y permitirle al programador invocar
métodos para intercambiar animaciones:


.. code-block:: python

    class MiNave(...)

        [...] # codigo anterior
    
        def poner_en_movimiento(self):
            self.animacion_actual = self.animacion_movimiento
            self.animacion_movimiento.asignar(self)

        def poner_en_reposo(self):
            self.animacion_actual = self.animacion_detenida
            self.animacion_detenida.asignar(self)

        def actualizar(self):
            self.animacion_actual.avanzar()
            self.animacion_detenida.asignar(self)


