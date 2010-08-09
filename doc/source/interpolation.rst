Interpolaciones
===============

Las interpolaciones nos pemiten lograr movimientos
de los actores de manera sencilla.

Por ejemplo, si queremos cambiar la posición
de un actor en pantalla podemos usar estas
sentencias::

    actor.x = 10
    actor.x = 20
    actor.x = 30
    etc ...

o directamente usar una interpolación:

    actor.x = pilas.interpolate(0, 100)

donde ``0`` es la posición inicial y ``100`` es el
valor final.

La función ``interpolate`` también admite un tercer
parámetro que indica la cantidad de segundos que
se tienen que utilizar para lograr la animación.


Girando un actor
----------------

Esta herramienta se puede aplicar a muchas situaciones distintas, por
ejemplo si quieresmos hacer girar un personaje
podemos hacer algo como::

    actor.rotation = pilas.interpolate(0, 360, 5)

con lo que estaríamos diciendo al personaje que dé un
giro completo (de ``0`` a ``360`` grados) en ``5`` segundos.


Escalando un actor
------------------

De manera similar a lo que hicimos anteriormente, podemos
aplicarla a la propiedad ``scale`` una nueva
interpolación::

    actor.scale = pilas.interpolate(0, 2, 5)

esto duplicará el tamaño del actor en ``5`` segundos.
