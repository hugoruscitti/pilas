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

``iniciar(ancho, alto, titulo, usar_motor, gravedad)``
    inicia la biblioteca y la ventana principal. Todos los argumentos son
    opcionales, los valores de ``usar_motor`` pueden ser 'qt' o 'qtgl'.

``iniciar_con_lanzador(ancho, alto, titulo, rendimiento,``
``modo, gravedad, imagen, permitir_depuracion)``

    similar a la función 'iniciar', pero muestra una ventana para que el usuario
    seleccione algunos parametros como pantalla completa.

``pilas.terminar()``

    para cerrar la ventana (su atajo es la tecla 'alt+q')

``pilas.ejecutar(ignorar_errores)``

    para poner en funcionamiento la biblioteca desde script, no hace falta
    llamarla en modo interactivo.

``pilas.avisar(mensaje)``

    dibuja un mensaje al pie de la ventana.

``pilas.ver(objeto)``

    muestra el codigo de un objeto o modulo.

``help(objeto)``

    muestra ayuda sobre un objeto o modulo.


Uso básico de Actores
---------------------

Los actores te permiten representar personajes con facilidad.

Para crear un actor tienes que escribir algo cómo:

.. code-block:: python

    mono = pilas.actores.Mono()

cada actor tiene atributos cómo: x, y, z, rotacion, escala, espejado, centro.

Por ejemplo:

.. code-block:: python

    mono.escala = 2
    mono.x = 200

Y como cada actor es un objeto, también entienden
mensajes cómo:

.. code-block:: python

    mono.sonreir()
    mono.decir("Hola!")

usa el comando ``help(mono)`` para conocer mas de
este actor, o bien ``pilas.ver(mono)``.

Los atributos también pueden recibir listas para
realizar animaciones, por ejemplo, esta sentencia
duplica el tamaño del actor en 5 segundos:

.. code-block:: python

    mono.escala = [2], 5


Imágenes
--------

Si la imagen es todo lo que representará el actor, asignala como una
simple cadena o usá la función ``cargar``:

.. code-block:: python

    imagen = pilas.imagenes.cargar("mi_personaje.png")
    actor = pilas.actores.Actor(imagen)

y si la imagen es una grilla, hay que definir las filas y columnas:

.. code-block:: python

    grilla = pilas.imagenes.cargar_grilla("pingu.png", 10, 1)
    actor = pilas.actores.Actor(grilla)

y luego, para avanzar la animación:

.. code-block:: python

    grilla.avanzar()

o bien:

.. code-block:: python

    actor.imagen.avanzar()


Sonidos y música
----------------

Puedes reproducir sonidos y música de manera similar:

.. code-block:: python

    sonido = pilas.sonidos.cargar("sonido.wav")
    sonido.reproducir(repetir=True) # repite eternamente vez el sonido
    sonido.detener() # frena la reproducción

si cambias ``pilas.sonido`` por ``pilas.musica`` podrás obtener el mismo
comportamiento.


Otros actores
-------------

Mono, Pelota, Caja, Bomba, Tortuga, Banana, Pingu, Animacion, etc.

Puedes ver todos los actores disponibles en *pilas* ejecutando:
``pilas.actores.listar_actores()``


Atajos de teclado
-----------------

La pantalla principal de pilas tiene algunos atajos útiles:

- **F7** Ver información de sistema
- **F8** Ver puntos de control (centros)
- **F9** Ver radios de colisión
- **F10** Ver áreas de imágenes originales.
- **F11** Ver figuras físicas.
- **F12** Ver posiciones.


Movimientos
-----------

Para simular movimientos puedes usar la función ``interpolar`` o simplemente
asignar listas:

``pilas.interpolar(valor_o_valores, duracion=1,``
``demora=0, tipo='lineal')``

    busca todos los valores intermedios entre los valores que se le indican
    como parámetro y el atributo que recibirá modificaciones.

Por ejemplo:

.. code-block:: python

    mono.rotacion = pilas.interpolar(360)
    mono.x = pilas.interpolar([-200, 200, 0], duracion=2)
    mono.y = [200, 0]


Habilidades
-----------

Las habilidades permite dotar a los actores de características
que le permite interactuar con el usuario.

Algunas habilidades son:

- ``SeguirAlMouse``
- ``AumentarConRueda``
- ``SeguirClicks``
- ``Arrastrable``
- ``MoverseConElTeclado``
- ``RebotarComoPelota``
- ``RebotarComoCaja``

y se pueden anexar a los actores así:

.. code-block:: python

    mono.aprender(pilas.habilidades.RebotarComoPelota)
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

    bombas = bomba * 10

    pilas.colisiones.agregar(mono, bombas, toca_bomba)


Eventos
-------

Eventos mas utilizados:

- ``actualizar`` sin argumentos.
- ``click_de_mouse`` con los argumentos ``button``, ``x``, ``y``
- ``mueve_mouse`` con los argumentos ``x``, ``y``, ``dx``, ``dy``
- ``termina_click`` con los argumentos ``button``, ``x``, ``y``
- ``mueve_camara``con los argumentos ``x``, ``y``, ``dx``, ``dy``
- ``pulsa_tecla`` con los argumentos ``codigo``, ``texto``
- ``suelta_tecla``con los argumentos ``codigo``, ``texto``
- ``pulsa_tecla_escape`` sin argumentos.



.. code-block:: python

    mono = pilas.actores.Mono()

    def mover_al_mono(evento):
        mono.x = evento.x
        mono.y = evento.y

    pilas.eventos.mueve_mouse.conectar(mover_al_mono)


Crear un evento personalizado
-----------------------------

Los eventos personalizados se pueden usar para comunicar
partes de un juego. Son cómo canales de comunicación en donde
se puede escribir y recibir mensajes.

.. code-block:: python

    pilas.eventos.cuando_golpean = pilas.eventos.Evento("cuando golpean")

    def cuando_golpean(evento):
        print "han golpeado a ", evento.quien

    # conectar una función observadora...
    pilas.eventos.cuando_golpean.conectar(cuando_golpean)
    # emitir el evento
    pilas.eventos.cuando_golpean.emitir(quien=self)


Tareas
------

Mediante tareas podemos programar funciones para que se ejecuten
luego de un determinado tiempo. Ya sea una vez, o de manera frecuente.

Ejemplos:

.. code-block:: python

    # ejecutar una tarea luego de 3 segundos
    pilas.escena_actual().tareas.una_vez(3, saludar)

    # repetir la ejecución de la función 1 vez por segundo
    tarea_con_frecuencia = pilas.escena_actual().tareas.siempre(1, saludar)
    tarea_con_frecuencia.terminar()


Actor personalizado y manejo de teclado
---------------------------------------

Para crear un actor personalizado, es conveniente crear
una clase que herede de ``Actor`` y sobreescribir el método
``actualizar`` (se se llamará 60 veces por segundo).

.. code-block:: python

    class Patito(pilas.actores.Actor):

        def __init__(self):
            pilas.actores.Actor.__init__(self)
            self.imagen = "patito.png"

        def actualizar(self):
            if pilas.mundo.control.izquierda:
                self.x -= 5
                self.espejado = True
            elif pilas.mundo.control.derecha:
                self.x += 5
                self.espejado = False

Escenas
-------

Hay algunas cosas a tener en cuenta a la hora de manejar escenas, porque
simplifican mucho el trabajo posterior:

- La escena actual siempre está señalada por el atributo
  ``pilas.escena_actual()``.
- Solo puede existir una escena activa a la vez.

para cambiando el fondo de las escena actual podrías ejecutar la siguiente
sentencia de código:

.. code-block:: python

    pilas.fondos.Volley()

Si quieres crear tu propia escena puedes escribir:

.. code-block:: python

    class PantallaBienvenida(pilas.escena.Normal):

        def iniciar(self):
            pilas.fondos.Pasto()
            texto = pilas.actores.Texto("Bienvenido a pilas!!!")

Si quieres salir de la escena, simplemente tendrías que hacer un
objeto de otra clase que represente otra escena y llamar a uno de estos
tres metodos:

.. code-block:: python

    mi_escena = PantallaBienvenida()
    pilas.almacenar_escena(mi_escena)
    pilas.recuperar_escena()
    pilas.cambiar_escena(mi_escena) # esto borra las escenas almacenadas



Referencias
-----------

 * http://www.pilas-engine.com.ar
 * http://www.losersjuegos.com.ar
