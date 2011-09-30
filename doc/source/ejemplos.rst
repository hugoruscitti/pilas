Ejemplos
========

Pilas viene con un módulo de ejemplos muy sencillos
para que puedas investigar y jugar.

Este módulo de ejemplos es ``pilas.ejemplos`` y está
organizado como una colección de clases.

Para poner en funcionamiento alguno de los ejemplos
simplemente tienes que hacer un objeto a partir
de alguna de las clases que verás en el módulo.

Piezas
------

Hay un pequeño rompecabezas que se puede
iniciar con la siguiente sentencia:

.. code-block:: python

    pilas.ejemplos.Piezas()

inmeditamente despúes de evaluar esa sentencia, aparecerá en
pantalla un grupo de piezas para que puedas 
empezar a acomodarlas usando el mouse.

.. image:: images/piezas.png

Ten en cuenta que los ejemplos también reciben parámetros, así
podemos alterar un poco mas el funcionamiento del minijuego.

Veamos cómo podemos crear un rompecabezas distinto a partir
del ejemplo ``Piezas``.

Escribe lo siguiente:

.. code-block:: python

    pilas.ejemplos.Piezas("mono.png", 2, 2)

Si, ahora en pantalla aparece la imagen del mono pero separado
en 4 piezas. Dado que hemos especificado 2 (filas) y 2 (columnas).

.. image:: images/piezas_mono.png


Puedes usar cualquier imagen que quieras para construir tu
ejemplo de piezas.

También se admite una función cómo argumento al
crear el objeto, que se invocará cuando el usuario
complete el rompecabezas:

.. code-block:: python

    def cuando_se_complete():
        pilas.avisar("Lo has completado!!!")

    pilas.ejemplos.Piezas("mono.png", 2, 2, cuando_se_complete)


.. image:: images/piezas_completo.png

