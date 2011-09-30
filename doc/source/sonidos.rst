Cargar sonidos
==============

Los sonidos se pueden cargar usando el módulo
``sonidos`` de la siguiente manera:

.. code-block:: python

    sonido_de_explosion = pilas.sonidos.cargar('explosion.wav')

donde ``explosion.wav`` es el nombre del archivo de audio.

Ten en cuenta que esta función para cargar sonidos
se comporta muy parecido a la función que nos permite
cargar imagenes o grillas. El archivo se buscará en
el directorio principal de nuestro juego, luego en el
directorio ``data`` y por último en la biblioteca de
sonidos que trae pilas.


Reproducir
----------

La función ``sound.cargar`` nos retorna un objeto de tipo
``Sonido`` que tiene un método para reproducirse llamado
``reproducir()``.

Entonces, para reproducir un sonido solamente tienes
que llamar al método ``reproducir``:

.. code-block:: python

    sonido_de_explosion.reproducir()
