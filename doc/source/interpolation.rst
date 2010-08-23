Interpolaciones
===============

Las interpolaciones nos pemiten lograr movimientos
de los actores de manera sencilla.

Por ejemplo, traducionalmente si quisieramos cambiar
posición de un actor en pantalla podemos usar estas
sentencias::

    actor.x = 10
    actor.x = 20
    actor.x = 30
    etc ...

pero es mas sencillo usar una interpolación::

    actor.x = pilas.interpolar(100)

donde el valor inicial será la posición x del actor y el valor
final será ``100``.

La función ``interpolar`` también admite un parámetro llamado
``duration`` que indica
la cantidad de segundos que
se tienen que utilizar para lograr la animación.


Girando un actor
----------------

Esta herramienta se puede aplicar a muchas situaciones distintas, por
ejemplo si queremos hacer girar un personaje
podemos hacer algo como::

    actor.rotacion = pilas.interpolar(360, duration=5)

con lo que estaríamos diciendo al personaje que dé un
giro completo (de ``0`` a ``360`` grados) en ``5`` segundos.

También existe un argumento ``delay`` para demorar el
inicio de la interpolación.


Escalando un actor
------------------

De manera similar a lo que hicimos anteriormente, podemos
aplicarla a la propiedad ``escala`` una nueva
interpolación::

    actor.escala = pilas.interpolar(2, duration=5)

esto duplicará el tamaño del actor en ``5`` segundos.


Interpolaciones en cadena
-------------------------

Si queremos que una interpolación pase por distintos
valores podemos hacer algo como esto::

    actor.x = pilas.interpolar(300, 0, 300, duration=3)

lo que llevará al actor de su posición ``x`` actual, a 300
en un segundo, y luego a ``0`` en 1 segundo y por último
de nuevo a ``300`` en un segundo.

En total, ha consumido 3 segundos en pasar por todos los
valores que le indicamos.
