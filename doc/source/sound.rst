Cargar sonidos
==============

Los sonidos se pueden cargar usando el módulo
``sonidos`` de la siguiente manera:

.. code-block:: python

    sonido_de_grito = pilas.sonidos.cargar('shout.wav')

donde ``shout.wav`` es el nombre del archivo de audio
que pilas buscará en el directorio ``data``.

Reproducir
----------

La función ``sound.cargar`` nos retorna un objeto de tipo
``Sound`` que tiene un método para reproducirse llamado
``Play()``.

Entonces, para reproducir un sonido solamente tienes
que llamar al método ``Play``:

.. code-block:: python

    sonido_de_grito.Play()


Referencias
-----------

Actualmente estamos usando varias llamadas al módulo
de sonido de la biblioteca SFML, que es la capa multimedia
que usamos en pilas. De ahí que tenemos algunas funciones
en inglés y otras no...

Nuestro deseo en pilas es que poco a poco podamos ir
escribiendo funciones para el manejo de recursos sea mas
sencillo que ahora.
