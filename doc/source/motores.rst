Motores
=======

Internamente pilas delega toda la tarea de dibujar,
manejo de eventos y multimedia en general a un
motor llamado PySFML.

Pero como PySFML no funciona en todos los equipos, pilas
implementa una capa intermedia que le permite funcionar
con otras bibliotecas, por ejemplo ``pygame``, que
funciona en muchos equipos y plataformas distintas (como
OLPC).

Para indicarle a pilas el motor que tiene que
utilizar puede usar la siguiente sentencia:

.. code-block:: python

    pilas.iniciar(usar_motor='pygame')

es decir, solamente tienes que cambiar la inicialización
de la biblioteca, el resto funcionará normalmente.

Ten en cuenta que generalmente en los tutoriales de
pilas o en las presentanciones solamente llamamos a ``pilas.iniciar``
pero sin indicarle el motor a utilizar. Cuando no le decimos
a pilas "qué" motor utilizar, pilas seleccionará a ``PySFML``.
