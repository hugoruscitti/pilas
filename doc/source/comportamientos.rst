Comportamientos
===============

En el desarrollo de videojuegos es conveniente
tener una forma de indicarle a los actores
una rutina o tarea para que la realicen.

En pilas usamos el concepto de comportamiento. Un
comportamiento es un objeto que le dice a
un actor que debe hacer en todo momento.

La utilidad de usar componentes es que puedes
asociarlos y intercambiarlos libremente para
lograr efectos útiles.


Por ejemplo, el objeto tortuga usa comportamientos
cada vez que le dices que avance o gire. Cuando
le indicas a la tortuga que avance, se genera un
objeto comportamiento que le va diciendo en cada
instante que avance un paso. Cuando el
comportamiento llega al punto que nos interesa
termina, y se desvincula del actor.
