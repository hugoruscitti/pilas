.. _ref_migrar_al_gestor_de_escenas:

Como migrar mi juego al nuevo Gestor de Escenas
===============================================

Antes de migrar tu juego al nuevo sistema de gestión de escenas, es mejor que
le des un vistazo a :ref:`ref_gestor_de_escenas` para comprender mejor el 
apilamiento de escenas.

Ahora pasamos a explicar los sencillos pasos a seguir para hacer la migración de tu juego.

Iniciar el juego
----------------

Tu juego debe tener una estructura de inicio parecida a la siguiente:

.. code-block:: python

    import pilas
    import escena_menu

    pilas.iniciar(titulo='Mi titulo')

    escena_menu.EscenaMenu()

    pilas.ejecutar()


Lo único que deberás cambiar aquí es la línea que llama a la escena.
Tendrá que quedar de la siguiente forma:

.. code-block:: python

    import pilas
    import escena_menu

    pilas.iniciar(titulo='Mi titulo')

    # Esta es la línea que debemos cambiar
    pilas.cambiar_escena(escena_menu.EscenaMenu())

    pilas.ejecutar()


Escenas del juego
-----------------

Todas las escenas de tu juego deben heredar ahora de `pilas.escena.Base`.

.. code-block:: python

    class MiEscena(pilas.escena.Base):

Y el otro cambio que debes realizar en las escenas es que el método ``__init__(self)`` no debe
contener nada más que la llamada al ``__init__`` de la escena Base

.. code-block:: python
    
    def __init__(self):
        pilas.escena.Base.__init__(self)


Luego debes definir un método ``iniciar(self)`` donde podrás crear los
nuevos actores y lo necesario para iniciar tu escena.

.. code-block:: python

    def iniciar(self):
        pilas.fondos.Pasto()
        mono = pilas.actores.Mono()
        
        
Aquí un ejemplo de como debería ser el cambio.

**Escena antigua**

.. code-block:: python

    class MiEscena(pilas.escenas.Escena):
    
        def __init__(self):
            pilas.escenas.Escena.__init__(self)
        
            pilas.fondos.Pasto()
            mono = pilas.actores.Mono()
            
            
**Escena nueva**

.. code-block:: python

    class MiEscena(pilas.escena.Base):
    
        def __init__(self):
            pilas.escena.Base.__init__(self)

        def iniciar(self):
            pilas.fondos.Pasto()
            mono = pilas.actores.Mono()


Cambio de Escena
----------------

En algún punto de tu juego, llamarías a otra escena para cambiarla.

.. code-block:: python
    
    escena_juego.Escena_Juego()
    
Debes sustituir esta llamada a la nueva escena por esta otra forma:

.. code-block:: python
    
    pilas.cambiar_escena(escena_juego.Escena_Juego())


Eventos
-------

Ahora los eventos son individuales por cada escena.
Si quieres conectar a algún evento, como `mueve_mouse`, `actualizar`, `pulsa_tecla`, puedes
hacerlo de cualquiera de las dos siguientes formas:

.. code-block:: python

    def mi_metodo(evento):
        # Hace algo
    
    pilas.eventos.actualizar.conectar(mi_metodo())

    # Otra forma de conectar    
    pilas.escena_actual().actualizar.conectar(mi_metodo())
    
Ambas formas conectan a los eventos de la escena actualmente activa.

Si deseas crear tu propio evento, lo deberás hacer de la siguiente forma:

.. code-block:: python
    
    pilas.eventos.mi_evento_personalizado = pilas.evento.Evento("mi_evento_personalizado")
    pilas.eventos.mi_evento_personalizado.conectar(self._mi_evento_personalizado)


Fin de la migración
-------------------

Con estos simples pasos, tu juego debe funcionar sin problemas con el nuevo
sistema de gestión de escenas.

Ante cualquier problema no tengas dudas en ponerte en contacto con nosotros
mediante el `foro de losersjuegos <http://www.losersjuegos.com.ar/foro/viewforum.php?f=24>`_.
