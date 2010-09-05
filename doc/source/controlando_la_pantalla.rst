Controlando la pantalla
=======================


La ventana principal de pilas tiene varias
propiedades interesantes y


Modo depuración
---------------

Pulse F12



Sistema de referencias
----------------------


Orden de impresión: atributo z
------------------------------

Cuando tienes varios actores en pantalla notaras
que a veces unos aparecen sobre otros. 

Para cambiar este comportamiento tienes que modificar
el atributo ``z`` de cada actor.

Los valores altos de ``z`` indican mucha distancia
entre el observador y el escenario. Mientras que
valores pequeños ``z`` harán que los actores tapen
a los demás (porque aparecerán mas cerca del
usuario).

Este es un ejemplo de dos configuraciones distintas
de atributos ``z``:

.. image:: images/atributo_z.png

Ten en cuenta que inicialmente todos los actores
tienen un atributo ``z=0``.
