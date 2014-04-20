Motores
=======

Internamente pilas delega toda la tarea de dibujar,
manejo de eventos y multimedia en general a un
motor llamado Qt.

Actualmente pilas soporta dos motores, y permite
que los programadores puedan seleccionar el motor
que mejor se adapta a los sistemas que se van
a utilizar para ejecutar el juego.

Para indicarle a pilas el motor que tiene que
utilizar puede usar la siguiente sentencia:

.. code-block:: python

    pilas.iniciar(usar_motor='qt')

es decir, solamente tienes que cambiar la inicialización
de la biblioteca, el resto funcionará normalmente.

Ten en cuenta que generalmente en los tutoriales de
pilas o en las presentanciones solamente llamamos a ``pilas.iniciar``
pero sin indicarle el motor a utilizar. Cuando no le decimos
a pilas "qué" motor utilizar, pilas seleccionará a ``qtgl``.
