Comportamientos
===============

En el desarrollo de videojuegos es conveniente
tener una forma de indicarle a los actores
una rutina o tarea para que la realicen.

En pilas usamos el concepto de comportamiento. Un
comportamiento es un objeto que le dice a
un actor qué debe hacer en todo momento.

La utilidad de usar componentes es que puedes
asociarlos y intercambiarlos libremente para
lograr efectos útiles.

Por ejemplo: un guardia de un juego de acción puede ir de
un lado a otro en un pasillo:

    - caminar hacia la izquierda hasta el fin del pasillo.
    - dar una vuelta completa.
    - caminar hacia la derecha hasta el fin del pasillo.
    - dar una vuelta completa.

En este caso hay 4 comportamientos, y queda en nuestro
control si queremos que luego de los 4 comportamientos
comience nuevamente.


Un ejemplo, ir de un lado a otro
--------------------------------

Veamos un ejemplo sencillo, vamos a crear un actor Mono
y decirle que se mueva de izquierda a derecha una
sola vez:

.. code-block:: python

    import pilas

    pilas.iniciar()
    mono = pilas.actores.Mono()

    pasos = 200

    moverse_a_la_derecha = pilas.comportamientos.Avanzar(pasos)
    mono.hacer_luego(moverse_a_la_derecha)

    mono.rotacion = [180] # Dar la vuelta.

    moverse_a_la_izquierda = pilas.comportamientos.Avanzar(pasos)
    mono.hacer_luego(moverse_a_la_izquierda)
    
    pilas.ejecutar() # Necesario al ejecutar en scripts.

De hecho, tenemos una variante que puede ser un poco
mas interesante; decirle al mono que repita estas tareas todo
el tiempo:

.. code-block:: python

    mono.hacer_luego(moverse_a_la_derecha, True)

Donde el segundo argumento indica si el comportamiento
se tiene que repetir todo el tiempo o no.
