Señales, callbacks y eventos
============================

En el desarrollo de videojuegos es muy importante
tener herramientas para que el usuario pueda
interactuar con el juego.

En pilas se usa una estrategia llamada
``señales y callbacks``, que se utiliza ampliamente en el
desarrollo de interfaces gráficas, la web y sistemas de tiempo
real.

¿Que es un Evento?
------------------

Un evento es un mensaje que emite algún componente
del juego, y que pueden captar o escuchar distintos
objetos para tomar una acción.

Por ejemplo, el componente ``pilas`` emite señales
de eventos cada vez que el usuario hace algo dentro del juego. Por
ejemplo, si el usuario mueve el mouse, ``pilas`` emite
la señal de evento ``mueve_mouse``.

Veamos un ejemplo de esto en la siguiente sección.

Conectando eventos a funciones
------------------------------

Las señales de ``eventos`` solo representan un aviso de que algo
ha ocurrido, pero no toman ninguna acción al respecto.

Entonces, para darle utilidad a estas señales tenemos
que vincularlas, de forma que puedan disparar acciones
dentro de nuestro juego.

La función ``connect``
______________________

La función ``connect`` nos permite conectar una señal de
evento a un método o una función.

De esta forma, cada vez que se emita una determinada
señal, se avisará a todos los objectos que hallamos
conectado.

Por ejemplo, si queremos que un personaje se mueva
en pantalla siguiendo la posición del puntero
del mouse, tendríamos que escribir algo como
esto:


.. code-block:: python

    import pilas

    mono = pilas.actores.Mono()

    def mover_mono_a_la_posicion_del_mouse(sender, x, y):
        mono.x = x
        mono.y = y

    pilas.eventos.mueve_mouse.connect(mover_mono_a_la_posicion_del_mouse)


Es decir, la señal de evento que nos interesa es ``mueve_mouse`` (que se emite
cada vez que el usuario mueve el mouse). Y a esta señal le conectamos
la función que buscamos ejecutar cada vez que se mueva el mouse.

Nota que pueden existir tantas funciones conectadas a una señal como
quieras. Y que si la función deja de existir no hace falta desconectarla.


Las coordenadas que reporta el mouse son relativas al escenario y no
de la ventana. Por lo tanto puedes asignar directamente el valor
de las coordenadas del mouse a los actores sin efectos colaterales.

Desconectando señales
---------------------

Las señales se desconectan solas cuando dejan de existir
los objetos que le conectamos. Así que no suele ser un problema que
la señal se halla conectado a objetos que dejarán de existir.

Pero, de todas formas, puede que quieras conectar una señal, y por
algún motivo desconectarla.

Si ese es tú caso, simplemente asignarle un identificador único
al manejador de la señal y luego usa la función ``disconnect`` indicando
el identificador.

Por ejemplo, las siguientes sentencias muestran eso:

.. code-block:: python

    pilas.eventos.mueve_mouse.conectar(imprimir_posicion, uid='drag')
    pilas.eventos.mueve_mouse.desconectar(dispatch_uid='drag')
    
En la primer sentencia conecté la señal del evento a una función y le di
un valor al argumento ``uid``. Este valor será el identificador
de ese enlace.

En la siguiente linea pude usar el identificador para desconectarla.



Referencias
-----------

El concepto que hemos visto en esta sección se utiliza
en muchos sistemas. Tal vez el mas conocido de estos es
la biblioteca ``GTK``, que se utiliza actualmente para construir
el escritorio GNOME y Gimp entre otras aplicaciones.

El sistema de señales que se utiliza en pilas se obtuvo
(gentilmente) del núcleo del sistema ``django``, dado que
es brillante y se adapta muy bien a las necesidades de nuestro
motor.

Si quieres obtener mas información sobre los sistemas de señales
y en particular sobre el que usamos aquí (el de django) puedes
ver los siguientes documentos:

- http://www.mercurytide.co.uk/news/article/django-signals/
- http://www.boduch.ca/2009/06/sending-django-dispatch-signals.html
- http://docs.djangoproject.com/en/dev/topics/signals/
