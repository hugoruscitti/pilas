Integrando Pilas a una Aplicación Qt
======================================

En esta sección vamos a mostrar como integrar Pilas como un widget dentro de tu
aplicación desarrollada con *PyQt*.

**Nota: En este capitulo asumimos que el programador ya conoce PyQt y Pilas.**


Antes de empezar vamos a establecer algunos objetivos:

    * Trataremos que la programación de la parte *Pilas* sea lo mas
      *Pilas-Like*.
    * Pilas nos brinda un solo widget; por el objetivo anterior intentaremos
      mantener esto.
    * La programación de la parte PyQt trataremos que se mantenga lo mas
      *PyQt-Like*.


Con esto en mente vamos a proponernos un proyecto:

    Desarrollaremos una aplicación PyQt que muestre algunos actores en pantalla
    y al hacerle click sobre alguno nos permita seleccionar una imagen desde
    un archivo para reemplazar a la del actor.

La estructura de objetos que manejaremos sera la siguiente:

.. image:: images/pilasqtclass.png

Donde el objetivo de cada clase es el siguiente:

    * ``MainWindow``: Es un widget PyQt4 que hereda de
      ``PyQt4.QtGui.QMainWindow``. Se encargara de recibir el evento de cuando
      un ``ActorVacio`` fue "clickeado" y mostrara la ventana emergente para
      seleccionar la imagen que luego sera asignada en el actor que lanzo el
      evento.

    * ``PilasProxy``: Esta clase es un *singleton* que cada vez que es destruida
      *finje* su destrucción y solo limpia el widget principal de Pilas, para
      que cuando sea reutilizada, parezca que esta como nueva. Tendrá 3
      métodos/propiedades imporantes implementara:

          - ``widget``: Propiedad que referencia al widget principal de Pilas.
          - ``__getattr__``: Método que delegara todas las llamadas que no
            posea el proxy al widget principal de Pilas.
          - ``destroy``: Método que ocultara la implementación de ``destroy``
            del widget principal de Pilas.
          - ``actor_clickeado``: *evento* de pilas que enviara como parámetro
            el actor que fue clickeado.
          - ``agregar_actor``: permitirá agregar un actor al proxy y conectará
             las señales del actor con la señal del proxy.
          - ``borrar_actor``: borra un actor de los manejados por el proxy

    * ``ActorVacio``: Subclase de ``pilas.actores.Actor`` que emitirá un evento
      al ser clickeada sobre si misma.


Código
------


.. code-block:: python

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    #===============================================================================
    # IMPORTS
    #===============================================================================

    import sys
    import os
    import random

    # importamos todos los modulos necesarios de PyQt
    from PyQt4 import QtGui, QtCore


    #===============================================================================
    # CONFIGURACIÓN INICIAL
    #===============================================================================

    # antes de importar pilas creamos la app QT del programa
    # si tenemos los componentes pilas en otro modulo puede llegar a ser conveniente
    # importar ese modulo (el que usa pilas) dentro de un metodo de clase o una
    # funcion. Tambien para que phonon no se queje es bueno setearle una nombre a
    # nuestro QApplication
    app = QtGui.QApplication(sys.argv[1:])
    app.setApplicationName(__name__)


    # Importamos pilas con un motor que sirva para embeber
    # 'qt' y 'qtgl' crean y auto-arrancan la aplicacion
    # mientras que 'qtsugar' y 'qtsugargl' solo crean
    # los widget necesarios para embeber pilas
    import pilas
    pilas.iniciar(usar_motor="qtsugar")


    #===============================================================================
    # CLASE ACTOR
    #===============================================================================

    # nuestra clase actor
    class ActorVacio(pilas.actores.Actor):

        def __init__(self, *args, **kwargs):
            super(ActorVacio, self).__init__(*args, **kwargs)

            # El evento que emitiremos cuando clickean al actor
            self.me_clickearon = pilas.evento.Evento("me_clickearon")

            # Conectamos el evento genérico de click del mouse con un
            # validador que se encargara de determinar si el click
            # sucedió sobre el actor
            pilas.eventos.click_de_mouse.conectar(self._validar_click)

        def _validar_click(self, evt):
            # extraemos las coordenadas donde sucedió el click
            x, y = evt["x"], evt["y"]

            # vemos si el actor colisiona con el punto donde
            # se hizo click y de ser asi se lanza el evento
            # me_clickearon pasando como parámetro al mismo
            # actor
            if self.colisiona_con_un_punto(x, y):
                self.me_clickearon.emitir(actor=self)


    #===============================================================================
    # PROXY CONTRA PILAS
    #===============================================================================

    class PilasProxy(object):

        # esta variable de clase guardara la única instancia que genera esta clase.
        _instance = None

        # redefinimos __new__ para que solo haya una instancia de pilas proxy
        @staticmethod
        def __new__(cls, *args, **kwargs):
            if not PilasProxy._instance:
                PilasProxy._instance = super(PilasProxy, cls).__new__(cls, *args, **kwargs)
            return PilasProxy._instance

        def __init__(self):
            self._actores = set() # aca almacenaremos todos los actores
            self.click_en_actor = pilas.evento.Evento("click_en_actor")


        def __getattr__(self, k):
            # todo lo que no pueda resolver la clase se lo delega al widget.
            # Con esto el proxy puede ser usado trasparentemenente
            return getattr(self.widget, k)

        def agregar_actor(self, actor):
            # Validamos que el actor sea un ActorVacio
            assert isinstance(actor, ActorVacio)

            # conectamos la señal del actor con la señal del proxy
            actor.me_clickearon.conectar(
                self._clickearon_actor
            )

            # agregamos el actor a la coleccion de actores
            self._actores.add(actor)

        def _clickearon_actor(self, evt):
            # método que recibe a que actor clickearon y emite la señal
            # de que clickearon al actor desde el proxy
            self.click_en_actor.emitir(**evt)


        def borrar_actor(self, actor):
            if actor in self._actores:
                # si el actor exist en los manejados por el proxy
                # deconectamos las señales y destruimos el actor
                actor.me_clickearon.desconectar(self.click_en_actor)
                self._actores.remove(actor)
                actor.destruir()

        # prevenimos que al ejecutarse destroy sobre el widget subyacente
        def destroy(self):
            self.widget.setParent(None)
            for act in self._actores:
                self.borrar_actor(act)

        @property
        def widget(self):
            return pilas.mundo.motor.ventana


    #===============================================================================
    # VENTANA PRINCIPAL
    #===============================================================================

    class MainWindow(QtGui.QMainWindow):

        def __init__(self):
            super(QtGui.QMainWindow, self).__init__()
            self.pilas = PilasProxy() # traemos nuestro proxy
            self.setCentralWidget(self.pilas.widget) # lo agregamos a la ventana
            self.resize(self.pilas.widget.size())

            # creamos entre 5 y 10 actores
            actores = ActorVacio() * random.randint(5,10)
            for a in actores:
                self.pilas.agregar_actor(a)

            # conectamos el evento click en el actor
            self.pilas.click_en_actor.conectar(self.on_actor_clickeado)

        def on_actor_clickeado(self, evt):
            # este slot va a abrir el selector de archivos de imagen
            # y asignar esa imagen al actor que llego como parametro
            actor = evt["actor"]
            filename = QtGui.QFileDialog.getOpenFileName(
                self, self.tr("Imagen de Actor"),
                os.path.expanduser("~"),
                self.tr("Imagenes (*.png *.jpg)")
            )
            if filename:
                actor.imagen = pilas.imagenes.cargar_imagen(
                    unicode(filename)
                )

    #===============================================================================
    # PONEMOS A CORRER TODO
    #===============================================================================

    win = MainWindow()
    win.show()
    sys.exit(app.exec_())


Resultado
---------

.. only:: latex

    .. image:: images/pilasqtrun.png

    Si quieren ver en video: http://www.youtube.com/watch?v=DA1DFTHJ-rE&feature=youtu.be


.. only:: html

    .. raw:: html

        <iframe width="560"
                height="315"
                src="http://www.youtube.com/embed/DA1DFTHJ-rE"
                frameborder="0"
                allowfullscreen>
        </iframe>
