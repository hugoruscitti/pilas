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
``Sonido`` que tiene un método para reproducirse llamado
``reproducir()``.

Entonces, para reproducir un sonido solamente tienes
que llamar al método ``reproducir``:

.. code-block:: python

    sonido_de_grito.reproducir()


