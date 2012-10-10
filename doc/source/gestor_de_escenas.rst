.. _ref_gestor_de_escenas:

Nuevo Gestor de Escenas
=======================

Pilas contiene un nuevo gestor de escenas que permite tener más de una
escena en el juego, aunque sólo una de ellas será la activa.

Esta nueva funcionalidad nos permitiría, por ejemplo, estar jugando y en
cualquier momento pulsar una tecla y acceder a las opciones del juego.

Allí quitaríamos el sonido y luego pulsando otra tecla volveriamos al juego,
justo donde lo habíamos dejado.

Nuestros actores estarán en la misma posición y estado en el que los habíamos
dejado antes de ir a las opciones.


Escena Base
------------

Es la Escena de la cual deben heredar todas las escenas del juego en pilas.

.. code-block:: python

    pilas.escena.Base

El ``antiguo método`` para crear una escena era el siguiente:
    
.. code-block:: python

    class MiEscena(pilas.escenas.Escena):
    
        def __init__(self):
            pilas.escenas.Escena.__init__(self)
        
            pilas.fondos.Pasto()
            mono = pilas.actores.Mono()
        

Ahora el ``nuevo método`` para crear una escena es el siguiente:

.. code-block:: python

    class MiEscena(pilas.escena.Base):
    
        def __init__(self):
            pilas.escena.Base.__init__(self)

        def iniciar(self):
            pilas.fondos.Pasto()
            mono = pilas.actores.Mono()

Como puedes observar, ahora la escena hereda de 

.. code-block:: python

    pilas.escena.Base
    
Otro cambio **muy importante** es que el metodo ``__init__(self)`` no debe
contener nada más que la llamada al ``__init__`` de la escena Base.

.. code-block:: python
    
    def __init__(self, titulo):
        pilas.escena.Base.__init__(self)
        
        self._titulo = titulo
        self._puntuacion = puntuacion

Puedes almacenar unicamente parámetros que quieras pasar a la escena.
Por ejemplo así:

.. code-block:: python
    
    def __init__(self, titulo):
        pilas.escena.Base.__init__(self)
        
        self._titulo = titulo

Y por último debes definir un método ``iniciar(self)`` donde podrás crear los
nuevos actores y lo necesario para iniciar tu escena.

.. code-block:: python

    def iniciar(self):
        pilas.fondos.Pasto()
        mono = pilas.actores.Mono()
        texti = pilas.actores.Texto(self._titulo)


Iniciar pilas con una Escena
----------------------------

Para iniciar pilas, con el nuevo sistema, debemos ejecutar lo siguiente

.. code-block:: python

    pilas.cambiar_escena(mi_escena.MiEscena())
    pilas.ejecutar()

Te habrás fijado que pilas dispone de un nuevo método para realizar esta
acción.

.. code-block:: python

    pilas.cambiar_escena(escena_a_cambiar)

En el próximo punto explicarémos su función junto con otros 2 metodos nuevos.


Cambiar entre Escenas
---------------------

Antes de nada debes comprender que pilas tiene la capacidad de apilar el número
de escenas que desees en su sistema.

El método de apilamiento es FILO (First In, Last Out), la primera escena en
entrar en la pila será la última en salir.

¿Y como apilamos, recuperamos y cambiamos escenas?, muy sencillo.
Pilas dispone de 3 métodos para realizar esta operaciones:

.. code-block:: python

    pilas.cambiar_escena(mi_escena)

    pilas.almacenar_escena(mi_escena)

    pilas.recuperar_escena()


* ``pilas.cambiar_escena(mi_escena)``: VACIA por completo la pila de escenas del sistema e incorporar la escena que pasamos como parámetro. La escena incorporada será la escena activa.

* ``pilas.almacenar_escena(mi_escena)``: apila la escena actual y establece como escena activa la que le pasamos como parámetro. La escena que ha sido apilada quedará pausada hasta su recuperación.

* ``pilas.recuperar_escena()``: recupera la última escena que fué apilada mediante ``alamacenar_escena()`` y la establece como escena activa.

Por último indicar que si quieres tener acceso a la escena actualmente activa, puedes hacerlo mediante el comando:

.. code-block:: python

    pilas.escena_actual()

