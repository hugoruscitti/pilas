Cargar sonidos
==============

Los sonidos se pueden cargar usando el módulo
``sound`` de la siguiente manera:

.. code-block:: python

    sonido_de_grito = pilas.sound.load('shout.wav')

donde ``shout.wav`` es el nombre del archivo de audio
que pilas buscará en el directorio ``data``.

Reproducir
----------

La función ``sound.load`` nos retorna un objeto de tipo
``Sound`` que tiene un método para reproducirse llamado
``Play()``.

Entonces, para reproducir un sonido solamente tienes
que llamar al método ``Play``:

.. code-block:: python

    sonido_de_grito.Play()
