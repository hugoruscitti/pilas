Señales, callbacks y eventos
============================

En el desarrollo de videojuegos es muy importante
tener herramientas para que el usuario pueda
interactuar con el juego.

En pilas se usa una estrategia llamada
``señales y callbacks``, que se utiliza ampliamente en el
desarrollo de interfaces gráficas, la web y sistemas de tiempo
real.

¿Que es una Señal?
------------------

Una señal es un mensaje que emite algún componente
del juego, y que pueden captar o escuchar distintos
objetos para tomar una acción.

Por ejemplo, el componente ``pilas`` emite señales
cada vez que el usuario hace algo dentro del juego. Por
ejemplo, si el usuario mueve el mouse, ``pilas`` emite
la señal ``mouse_move``.

Veamos un ejemplo de esto en la siguiente sección.

Conectando señales
------------------

Las ``señales`` solo representan un aviso de que algo
ha ocurrido, pero no toman ninguna acción al respecto.

Entonces, para darle utilidad a las señales tenemos
que vincularlas, de forma que puedan disparar acciones
dentro de nuestro juego.

La función ``connect``
______________________

La función ``connect`` nos permite conectar una señal
a un método o una función.

De esta forma, cada vez que se emita una determinada
señal, se avisará a todos los objectos que hallamos
conectado.

Por ejemplo, si queremos que un personaje se mueva
en pantalla siguiendo la posición del puntero
del mouse, tendríamos que escribir algo como
esto:


.. code-block:: python

    import pilas

    mono = pilas.actors.Monkey()

    def mover_mono_a_la_posicion_del_mouse(sender, x, y):
        mono.x = x
        mono.y = y

    pilas.signals.mouse_move.connect(mover_mono_a_la_posicion_del_mouse)

Es decir, la señal que nos interesa es ``mouse_move`` (que se emite
cada vez que el usuario mueve el mouse). Y a esta señal le conectamos
la función que buscamos ejecutar cada vez que se mueva el mouse.

Nota que pueden existir tantas funciones conectadas a una señal como
quieras. Y que si la función deja de existir no hace falta desconectarla.


Referencias
-----------

El concepto que hemos visto en esta sección se utiliza
en muchos sistemas. Tal vez el mas conocido de estos es
la biblioteca ``GTK``, que se utiliza actualmente para construir
el escritorio GNOME.

Originalmente en pilas se comenzó a crear un sistema de señales
propio, pero al poco tiempo se adoptó un sistema de señales
ya realizado. Este sistema de señales se ha obtenido del núcleo
del sistema ``django``, y sobre el cual tienes mucha
información para investigar:

- http://www.mercurytide.co.uk/news/article/django-signals/
- http://www.boduch.ca/2009/06/sending-django-dispatch-signals.html
- http://docs.djangoproject.com/en/dev/topics/signals/
