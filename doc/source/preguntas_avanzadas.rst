Guía de preguntas avanzadas
===========================


¿Cómo puedo personalizar el dibujado de un actor?
-------------------------------------------------

Cada vez que se actualiza el bucle de juego
se llama al método ``dibujar`` de cada actor.

Si quieres personalizar por completo la forma en
que se dibuja un actor puedes redefinir el
método ``dibujar`` y listo.

Para mas referencias puedes ver el método ``dibujar``
de la clase ``Actor`` o el método ``dibujar`` de
la clase ``escena.Normal``, que en lugar
de pintar una imagen borra todo el fondo de pantalla.



¿A veces los sonidos no se reproducen?
--------------------------------------

sip... a veces los sonidos no se reproducen porque
python los libera de memoria mientras están sonando.

Entonces, para solucionar el problema tienes que
mantener viva la referencia al objeto ``Sonido`` cuando
quieras reproducir algo. Por ejemplo:

:Ejemplo incompleto: 

    .. code-block:: python

        def reproducir_sonido():
            mi_sonido_que_no_suena = pilas.sonidos.cargar("sonido.wav.")
            mi_sonido_que_no_suena.reproducir()

        reproducir_sonido()

:Ejemplo correcto:

    .. code-block:: python

        sonido = None

        def reproducir_sonido():
            sonido = pilas.sonidos.cargar("sonido.wav")
            sonido.reproducir()

        reproducir_sonido()
    
¿Cual es la diferencia?, en el primer ejemplo el sonido no
se reproducirá porque la referencia ``mi_sonido_que_no_suena`` se
eliminará cuando termine de ejecutar la función ``reproducir_sonido``, mientras
que en el segundo la referencia ``sonido`` seguirá existiendo mientras
el sonido esté reproduciéndose.
