Grupos
======

Ahora que podemos manejar a los actores de manera individual. Vamos
a ver organizarlos en grupos.

Organizar a los actores en grupo es muy útil, porque es
algo que hacemos todo el tiempo en el desarrollo de videojuegos. Por
ejemplo, en un juego de naves espaciales, podríamos hacer un
grupo de naves enemigas, o un grupo de estrellas, o un grupo
de disparos.

Creando grupos con la función fabricar
--------------------------------------

Para crear varios actores de una misma clase
podríamos ejecutar algo como lo que sigue:

.. code-block:: python

    bombas = pilas.atajos.fabricar(pilas.actor.Bomba, 30)


donde el primer argumento es la clase de la que buscamos crear
actores, y el segundo argumento es la cantidad de actores
que queremos.

Esto es lo que veríamos en la ventana de pilas:

.. image:: images/grupos_bombas.png


A partir de ahora, la referencia ``bombas`` nos servirá para
controlar a todas las bombas al mismo tiempo.

Veamos como alterar el atributo de posición horizontal:

.. code-block:: python

    bombas.x = 0

Y en la ventana obtendremos:

.. image:: images/grupos_bombas_x.png


Incluso, les podríamos enseñar a las bombas a reaccionar
como si fueran pelotas, es decir, que reboten e interactúen
con la aceleración gravitatoria:

.. code-block:: python

    bombas.aprender(pilas.habilidades.RebotaComoPelota)


.. image:: images/grupos_bombas_como_pelota.png


Un consejo, la gravedad del escenario se puede modificar
usando una sentencia como la que sigue:

.. code-block:: python

    pilas.fisica.definir_gravedad(200, 0)

donde el primer argumento es la gravedad horizontal, en este caso 200
es hacia la derecha, y la gravedad vertical, que suele ser de -90
en general.


Creando un grupo desde un actor
-------------------------------

Otra forma práctica de generar un grupo, es usando
el operador "por" junto a un actor. Por ejemplo, el resultado
que logramos usando la función ``fabricar`` se podría lograr
haciendo esto:

.. code-block:: python
    
    bomba = pilas.actores.Bomba()
    muchas_bombas = bomba * 30


Es decir, cuando tomamos un actor y lo multiplicamos por
un número, el resultado es un grupo que contiene al actor
inicial y a 29 actores mas...
