Manejo de Cámara
================

En ocasiones queremos que el escenario de
nuestro juego sea muy extenso, un bosque, una
ciudad repleta de objetos etc...

Nuestros juegos con pilas no están limitados
a lo que podemos ver en la ventana, el espacio
del escenario puede ser tan grande como queramos. Aquí
es donde la ``cámara`` toma protagonismo.


El objeto ``cámara`` nos permite desplazar el punto
de vista en cualquier parte del escenario, dado que nos
brinda dos coordenadas: ``x`` e ``y``, para que le
indiquemos qué parte del escenario tenemos que observar.


Las coordenadas de la cámara
----------------------------

Inicialmente la cámara estará mostrando el punto ``(0, 0)``
del escenario, el punto central de la ventana.

Si queremos que muestre otra parte del escenario 
podemos ejecutar una sentencia como la que sigue:

.. code-block:: python

    pilas.escena_actual().camara.x = [200]
    pilas.escena_actual().camara.y = [200]


Con esto le estaríamos diciendo a la cámara que nos
muestre el punto ``(200, 200)`` del escenario. Así
observaríamos que podemos explorar la parte superior
derecha del escenario de forma gradual.



Objetos sensibles a la cámara
-----------------------------

Hay casos en donde queremos que los actores no
se desplacen junto con el escenario, es decir,
puede ocurrir que necesitemos que un actor permanezca
fijo en su posicion de pantalla aunque la cámara cambie
de lugar.

Este es el caso de los contadores de vidas, los textos
que vé un usuario o cualquier marcador auxiliar.

Para que un actor no se vea afectado por la cámara, tienes
que guardar el valor ``True`` dentro del atributo ``fijo``:

.. code-block:: python

    actor.fijo = True

Por lo general, todos los actores tienen este atributo a ``False``, porque
viven en el escenario de juego y no se quedan fijos a la pantalla. Excepto
los textos que siempre permanecen en la parte superior de la ventana.
