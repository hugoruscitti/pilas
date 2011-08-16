Manejo de tiempo con tareas
===========================

Una necesidad muy común en los videojuegos
es poder planificar tareas para ser ejecutadas
por tiempo.

Por ejemplo, en un juego de naves podríamos
querer que aparezcan naves enemigas cada
dos segundos.


Tareas
------

Las tareas son acciones que elegimos ejecutar
en un determinado momento.

Al momento de crear la tarea tenemos que
pensar "en qué momento se tiene que ejecutar
la tarea", y dependiendo de lo que queramos
tenemos que escribir algo cómo:

.. code-block:: python

    pilas.mundo.agregar_tarea(tiempo, funcion, parametros)


Hay tres tipos de creaciones de tareas:

    - tareas que se ejecutan una vez.
    - tareas que se ejecutan siempre.
    - tareas condicionales.


las tareas condicionales se ejecutarán siempre y cuando
la función que las representa retorna True. Si la función
retorna False la tareas dejará de ejecutarse.


Eliminar tareas
---------------

Una forma sencilla de detener una tarea es iniciarla
cómo condicional, y que la función que le asignamos
retorne False.

Otra forma es simplemente capturar el retorno de
la función que ha creado la tarea y detenerla.

Por ejemplo:

.. code-block:: python

    una_tarea = pilas.mundo.agregar_tarea_siempre(5, funcion)

y luego, cuando queramos que la tarea finalice
y no se vuelva a ejecutar, tendríamos que ejecutar
una sentancia cómo ésta:

.. code-block:: python

    una_tarea.terminar()

