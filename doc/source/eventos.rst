Eventos, conexiones y respuestas
================================

En el desarrollo de videojuegos es muy importante
poder comunicarse con el usuario. Lograr que los
personajes del juego puedan interactuar con él y
exista una fuerte interacción.

En pilas usamos una estrategia llamada ``eventos, conexiones
y respuestas``, no solo porque es muy sencilla de usar, sino
también porque es una solución conocida y muy utilizada
en otros lugares como en la web.

¿Que es un Evento?
------------------

Los eventos representan algo que esperamos que ocurra
dentro de un juego, por ejemplo un ``click`` del mouse, la
``pulsación`` de una tecla, el ``cierre`` de la
ventana o la ``colisión`` entre un enemigo y nuestro
protagonista.

Lo interesante de los eventos, es que pueden ocurrir en
cualquier momento, y generalmente no lo controlamos, solamente
los escuchamos y tomamos alguna respuesta predefinida.

Pilas representa a los eventos como objetos, y nos brinda
funciones para ser avisados cuando un evento ocurre e incluso
emitir y generar eventos nuevos.

Veamos algunos ejemplos:

Conectando la emisión de eventos a funciones
---------------------------------------------

Los ``eventos`` no disparan ninguna acción automática, nosotros
los programadores somos los que tenemos que elegir los
eventos importantes y elegir que hacer al respecto.

Para utilizar estas señales, tenemos que vincularlas a funciones, de
forma que al emitirse la señal podamos ejecutar código.

La función ``conectar``
_______________________

La función ``conectar`` nos permite conectar una señal de
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

    def mover_mono_a_la_posicion_del_mouse(evento):
        mono.x = evento.x
        mono.y = evento.y

    pilas.eventos.mueve_mouse.conectar(mover_mono_a_la_posicion_del_mouse)

    # O puedes utilizar el método abreviado del actor.
    mono.mueve_mouse(mover_mono_a_la_posicion_del_mouse)



Es decir, la señal de evento que nos interesa es ``mueve_mouse`` (que se emite
cada vez que el usuario mueve el mouse). Y a esta señal le conectamos
la función que buscamos ejecutar cada vez que se mueva el mouse.

Ten en cuenta que pueden existir tantas funciones conectadas a una señal como
quieras.

Las coordenadas que reporta el mouse son relativas al escenario y no
de la ventana. Por lo tanto puedes asignar directamente el valor
de las coordenadas del mouse a los actores sin efectos colaterales
con respecto a la cámara.


Observando a los eventos para conocerlos mejor
----------------------------------------------

Como puedes ver en la función ``mover_mono_a_la_posicion_del_mouse``, hemos
definido un parámetro llamado ``evento`` y accedimos a sus valores
``x`` e ``y``.

Cada evento tiene dentro un conjunto de valores que nos resultará
de utilidad conocer. En el caso del movimiento de mouse usamos
``x`` e ``y``, pero si el evento es la pulsación de una tecla, seguramente
vamos a querer saber exactamente qué tecla se pulsó.

Entonces, una forma fácil y simple de conocer el estado de un
objeto es imprimir directamente su contenido, por ejemplo, en
la función de arriba podíamos escribir:

.. code-block:: python

    def mover_mono_a_la_posicion_del_mouse(evento):
        print evento

y en la ventana de nuestra computadora tendríamos que ver
algo así::

    {'y': 2.0, 'x': -57.0, 'dx': 0.0, 'dy': -1.0}


donde claramente podemos ver todos los datos que vienen asociados
al evento.

Por último, ten en cuenta que este argumento ``evento``, en realidad,
es un diccionario de python como cualquier otro, solo
que puedes acceder a sus valores usando sentencias cómo
``diccionario.clave`` en lugar de ``diccionario['clave']``.

Desconectando señales
---------------------

Las señales se desconectan por cuenta propia cuando dejan de existir
los objetos que le conectamos. En la mayoría de los casos podemos
conectar señales y olvidarnos de desconectarlas, no habrá problemas, 
se deconectarán solas.

De todas formas, puede que quieras conectar una señal, y por
algún motivo desconectarla. Por ejemplo si el juego cambia
de estado o algo así...

Si ese es tu caso, simplemente asígnale un identificador único
al manejador de la señal y luego usa la función ``desconectar_por_id`` indicando
el identificador.

Por ejemplo, las siguientes sentencias muestran eso:

.. code-block:: python

    pilas.eventos.mueve_mouse.conectar(imprimir_posicion, id='drag')
    pilas.eventos.mueve_mouse.desconectar_por_id('drag')
    
En la primera sentencia conecté la señal del evento a una función y le di
un valor al argumento ``id``. Este valor será el identificador
de ese enlace. Y en la siguiente linea se utilizó el identificador
para desconectarla.

Consultado señales conectadas
-----------------------------

Durante el desarrollo es útil poder observar qué
eventos se han conectado a funciones.

Una forma de observar la conexión de los eventos
es pulsar la tecla ``F6``. Eso imprimirá sobre
consola los nombres de las señales conectadas
junto a las funciones.


Creando tus propios eventos
---------------------------

Si tu juego se vuelve mas complejo y hay interacciones entre
varios actores, puede ser una buena idea hacer que exista algo
de comunicación entre ellos usando eventos.

Veamos cómo crear un evento:

Primero tienes que crear un objeto que represente a tu evento
y darle un nombre:

.. code-block:: python

    evento = pilas.evento.Evento("Nombre")

luego, este nuevo objeto ``evento`` podrá ser utilizado como
canal de comunicación: muchos actores podrán ``conectarse`` para
recibir alertas y otros podrán ``emitir`` alertas:

.. code-block:: python

    def ha_ocurrido_un_evento(datos_evento):
        print "Hola!!!", datos_evento

    evento.conectar(ha_ocurrido_un_evento)

    # En otra parte...
    evento.emitir(argumento1=123, argumento2=123)

Cuando se emite un evento se pueden pasar muchos argumentos, tantos
como se quiera. Todos estos argumentos llegarán a la función de
respuesta en forma de diccionario.

Por ejemplo, para este caso, cuando llamamos al método ``evento.emitir``,
el sistema de eventos irá automáticamente a ejecutar la función ``ha_ocurrido_un_evento``
y ésta imprimirá::

    Hola!!! {argumento1: 123, argumento2: 123}

.. note::
    Para entender mejor cómo se han implementado los eventos, visita este link
    http://hugoruscitti.github.com/2012/03/01/redisenando-el-sistema-de-eventos-pilas/

Referencias
-----------

El concepto que hemos visto en esta sección se utiliza
en muchos sistemas. Tal vez el mas conocido de estos es
la biblioteca ``GTK``, que se utiliza actualmente para construir
el escritorio ``GNOME`` y ``Gimp`` entre otras aplicaciones.

El sistema de señales que se utiliza en pilas es una
adaptación del siguiente sistema de eventos:

http://stackoverflow.com/questions/1092531/event-system-in-python

Anteriormente usábamos parte del código del sistema ``django``, pero
luego de varios meses lo reescribimos para que sea mas sencillo
de utilizar y no tenga efectos colaterales con los métodos y
el módulo ``weakref``.

Si quieres obtener mas información sobre otros sistemas de
eventos te recomendamos los siguientes documentos:

- http://pydispatcher.sourceforge.net/
- http://www.mercurytide.co.uk/news/article/django-signals/
- http://www.boduch.ca/2009/06/sending-django-dispatch-signals.html
- http://docs.djangoproject.com/en/dev/topics/signals/
