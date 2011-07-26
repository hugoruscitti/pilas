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

Si queremos que apunte a otra parte del escenario 
podemos ejecutar una sentencia como la que sigue:

.. code-block:: python

    pilas.mundo.camara.x = [200]
    pilas.mundo.camara.y = [200]


Con esto le estaríamos diciendo a la cámara que nos
muestre el punto ``(200, 200)`` del escenario. Así
observaríamos que podemos explorar la parte superior
derecha del escenario de forma gradual.


