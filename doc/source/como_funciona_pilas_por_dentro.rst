Cómo funciona pilas por dentro
==============================

Pilas es un proyecto con una arquitectura de objetos
grande. Tiene mucha funcionalidad, incluye un
motor de física, muchos personaje pre-diseñados y soporta (hasta
el momento) dos motores multimedia opcionales (pygame
y sfml).

Mediante este capítulo quisiera explicar a grandes
rasgos los componentes de pilas. Cómo están estructurados
los módulos, qué hacen las clases mas importantes.

El objetivo es orientar a los programadores mas
avanzados para que puedan investigar pilas
por dentro.

Filosofía de desarrollo
-----------------------

Pilas es un proyecto de software libre, orientado a facilitar
el desarrollo de videojuegos a personas que generalmente no
hacen juegos... así que gran parte de las decisiones de
desarrollo comenzaron reflexionando sobre cómo
diseñar una interfaz de programación simple y fácil
de utilizar.

Un ejemplo de ello, es que elegimos el lenguaje de
programación python, y tratamos de aprovechar al máximo
su modo interactivo.


API en español
--------------

Dado que pilas está orientado a principiantes, docentes y
programadores de habla hispana. Preferimos hacer el motor
en español, permitirle a los mas chicos usar su idioma
para hacer juegos es alentador, tanto para ellos que
observan que el idioma no es una barrera, como
para los que enseñamos y queremos entusiasmar.

Esta es una decisión de diseño importante, porque al
mismo tiempo que incluye a muchas personas, no coincide
con lo que acostumbran muchos programadores (escribir
en inglés).

Posiblemente en el futuro podamos ofrecer una
versión de pilas alternativa en inglés, pero
actualmente no es una prioridad.

Objetos y módulos
-----------------

Pilas incluye muchos objetos y es un sistema complejo. Pero
hay una forma sencilla de abordarlo, porque hay solamente
3 componentes que son indispensables, y han
sido los pilares desde las primeras versiones de pilas
hasta la fecha:

- Mundo
- Actor
- Motor

Si puedes comprender el rol y las características
de estos 3 componentes el resto del motor es mas
fácil de analizar.

Veamos los 3 componentes rápidamente:

``Mundo`` es un objeto ``singleton``, hay una sola instancia
de esta clase en todo el sistema y se encarga de
mantener el juego en funcionamiento e interactuando con
el usuario.

Los actores (clase ``Actor``) representan a los personajes de los
juegos, la clase se encarga de representar todos sus atributos
como la posición y comportamiento como "dibujarse en la ventana". Si
has usado otras herramientas para hacer juegos, habrás notado
que se los denomina ``Sprites``.

Luego, el ``Motor``, permite que pilas sea un motor
multimedia portable y multiplaforma. Básicamente
pilas delega la tarea de dibujar, emitir sonidos y controlar
eventos a una biblioteca externa. Actualmente esa biblioteca
puede ser pygame o SFML, y ambas reciben en nombre 'Motor'
dentro de pilas.


Ahora que lo he mencionado, veamos con un poco mas
de profundidad lo que hace cada uno.

Inspeccionando: Mundo
_____________________

El objeto de la clase Mundo se construye cuando se invoca a la
función ``pilas.iniciar``. Su implementación está en el
archivo ``mundo.py``:

.. image:: images/comofunciona/mundo.png

Su responsabilidad es inicializar varios componentes de pilas, como
el sistema de controles, la ventana, etc.

Uno de sus métodos mas importantes es ``ejecutar_bucle_principal``. Un
método que se invoca directamente cuando alguien escribe
la sentencia ``pilas.ejecutar()``.

Si observas el código, notarás que es el responsable de mantener a todo
el motor en funcionamiento.

Esta es una versión muy simplificada del
método ``ejecutar_bucle_principal``:

.. code-block:: python

    def ejecutar_bucle_principal(self, ignorar_errores=False):

        while not self.salir:
            pilas.motor.procesar_y_emitir_eventos()

            if not self.pausa_habilitada:
                self._realizar_actualizacion_logica(ignorar_errores)

            self._realizar_actualizacion_grafica()

Lo primero que debemos tener en cuenta es que este método contiene
un bucle ``while`` que lo mantendrá en ejecución. Este bucle
solo se detendrá cuando alguien llame al método ``terminar`` (que
cambia el valor de la variable ``salir`` a ``True``).

Luego hay tres métodos importantes:

- ``procesar_y_emitir_eventos`` analiza el estado de los controles y avisa al resto del sistema si ocurre algo externo, como el movimiento del mouse..
- ``_realizar_actualizacion_logica`` le permite a los personajes realizar una fracción muy pequeña de movimiento, poder leer el estado de los controles o hacer otro tipo de acciones.
- ``_realizar_actualizacion_logica`` simplemente vuelca sobre la pantalla a todos los actores y muestra el resultado del dibujo al usuario.


Otra tarea que sabe hacer el objeto ``Mundo``, es administrar
escenas. Las escenas son objetos que representan una
parte individual del juego: un menú, una pantalla de opciones, el
momento de acción del juego etc...


Modo interactivo
----------------

Pilas soporta dos modos de funcionamiento, que técnicamente son
muy similares, pero que a la hora de programar hacen una gran
diferencia.

- **modo normal**: si estás haciendo un archivo ``.py`` con el código de tu juego usarás este modo, tu programa comienza con una sentencia como ``iniciar`` y la simulación se inicia cuando llamas a ``pilas.ejecutar`` (que se encarga de llamar a ``ejecutar_bucle_principal`` del objeto mundo).

- **modo interactivo**: el modo que generalmente se usa en las demostraciones o cursos es el modo interactivo. Este modo funciona gracias a una estructura de hilos, que se encargan de ejecutar la simulación pero a la vez no interrumpe al programador y le permite ir escribiendo código mientras la simulación está en funcionamiento.


Motores multimedia
------------------

Al principio pilas delegaba todo el manejo multimedia a una
biblioteca llamada
SFML. Pero esta biblioteca requería que todos los equipos
en donde funcionan tengan aceleradoras gráficas (al menos con
soporte OpenGL básico).

Pero como queremos que pilas funcione en la mayor cantidad
de equipos, incluso en los equipos antiguos de algunas
escuelas, añadimos soporte alternativo para una biblioteca
mas accesible llamada pygame.

Entonces, cuanto inicializas pilas tienes la oportunidad
de seleccionar el motor a utilizar, por ejemplo la
siguiente sentencia habilita el usuario de la biblioteca
pygame:

.. code-block:: python

    pilas.iniciar(usar_motor='pygame')


Ahora bien, ¿cómo funciona?. Dado que pilas está realizado
usando orientación a objetos, usamos un concepto llamado
polimorfismo:

El objeto motor sabe que tiene que delegar el manejo multimedia
a una instancia (o derivada) de la clase ``Motor`` (ver directorio
``pilas/motores/``:

.. image:: images/comofunciona/motores.png


El motor expone toda la funcionalidad que se necesita para
hace un juego: sabe crear una ventana, pintar una imagen o
reproducir sonidos, entre tantas otras cosas.

El objeto mundo no sabe exactamente que motor está utilizando, solo
tiene una referencia a un motor y delega en él todas las
tareas multimedia.

La diferencia de funcionamiento radica en cómo está implementado
el motor. En el caso de SFML, todas las tareas se terminan
realizando sobre un contexto OpenGL (que es rápido, pero requiere
un equipo relativamente moderno), y la implementación de motor
que usa pygame es algo mas lenta, pero funciona en todos
los equipos: OLPCs, netbook, PC antiguas o nuevas.

Solo puede haber una instancia de motor en funcionamiento, y
se define cuando se inicia el motor.


Sistema de actores
------------------


Los actores permiten que los juegos cobren atractivo, porque
un actor puede representarse con una imagen en pantalla. 

La implementación de todos los actores están en
el directorio ``pilas/actores``.

Todos los actores heredan de la clase ``Actor``, que define
el comportamiento común de todos los actores.

Por ejemplo, esta sería una versión reducida de la
jerarquía de clases de los actores Mono, Pingu y Tortuga:

.. image:: images/comofunciona/actores.png


Hay dos métodos en los actores que se invocarán en
todo momento: el método ``actualizar`` se invocará
cuando el bucle de juego del mundo llame al método 
``_realizar_actualizacion_logica``, esto ocurre unas
60 veces por segundo. Y el otro método es ``dibujar``, que
se también se invoca desde el objeto mundo, pero esta
vez en el método ``_realizar_actualizacion_grafica``.



Modo depuración
---------------

Cuando pulsas teclas como F8, F9, F10, F11 o F12 durante
la ejecución de pilas, vas a ver que la pantalla comienza
a mostrar información valiosa para los desarrolladores.

Esta modalidad de dibujo la llamamos **modo depuración**, y
ayuda mucho a la hora de encontrar errores o ajustar detalles.

Estos modos están codificados en el archivo ``depurador.py``, ahí
encontrarás varias clases:

.. image:: images/comofunciona/depurador.png


El Depurador tiene dos atributos, tiene una pizarra para dibujar y
una lista de modos. Los modos pueden ser cualquiera de los que están
en la jerarquía de ModoDepuracion, por ejemplo, podría tener
instancias de ModoArea y ModoPuntoDeControl.

El Depurador se encarga de recibir órdenes desde el objeto Mundo, y
crear o eliminar la pizarra según sea necesaria o no...
