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
hacen juegos... Por ese motivo que gran parte de las decisiones de
desarrollo se tomaron reflexionando sobre cómo
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

El objeto ``Mundo``, que mantiene en ejecución al juego, tiene
una instancia de objeto ``Depurador`` que se encarga de
hacer estos dibujos.

Las clases mas importantes a la hora de investigar el depurador
están en el archivo ``depurador.py``:

.. image:: images/comofunciona/depurador.png


El Depurador tiene dos atributos, tiene una pizarra para dibujar y
una lista de modos. Los modos pueden ser cualquiera de los que están
en la jerarquía de ModoDepuracion, por ejemplo, podría tener
instancias de ModoArea y ModoPuntoDeControl.



Sistema de eventos
------------------

Hay varios enfoques para resolver el manejo de eventos
en los videojuegos.

Pilas usa un modelo conocido y elaborado
llamado ``Observator``, un patrón de diseño. Pero que
lamentablemente no es muy intuitivo a primera vista.

En esta sección intentaré mostrar por qué usamos
esa solución y qué problemas nos ayuda a resolver.

Comenzaré explicando sobre el problema de gestionar eventos
y luego cómo el modelo ``Observator`` se volvió
una buena solución para el manejo de eventos.

El problema: pooling de eventos
_______________________________

Originalmente, en un modelo muy simple de aplicación multimedia,
manejar eventos de usuario es algo sencillo, pero con el
tiempo comienza a crecer y se hace cada vez mas difícil de
mantener.

Resulta que las bibliotecas multimedia suelen entregar un
objeto ``evento`` cada vez que ocurre algo y tu responsabilidad
es consultar sobre ese objeto en búsqueda de datos.

Imagina que quieres crear un actor ``Bomba`` cada
vez que el usuario hace click en la pantalla. El
código podría ser algo así:

.. code-block:: python

    evento = obtener_evento_actual()

    if evento.tipo == 'click_de_mouse':
        crear_bomba(evento.x)
        crear_bomba(evento.x)
    else:
        # el evento de otro tipo (teclado, ventana ...)
        # lo descartamos.


A esta solución podríamos llamarla **preguntar** y **responder**, 
porque efectivamente así funciona el código, primero
nos aseguramos de que el evento nos importa y luego
hacemos algo. En algunos sitios suelen llamar a esta
estrategia *pooling*.

Pero este enfoque tiene varios problemas, y cuando hacemos
juegos o bibliotecas se hace mas evidente. El código, a medida
que crece, comienza a mezclar manejo de eventos y lógica
del juego.

Para ver el problema de cerca, imagina que en determinadas
ocasiones quieres deshabilitar la creación de bombas, ¿cómo
harías?. ¿Y si quieres que las bombas creadas se puedan
mover con el teclado?.


Otro enfoque, en pilas usamos 'Observator'
__________________________________________

Hay otro enfoque para el manejo de eventos que me parece
mas interesante, y lo he seleccionado para el motor
``pilas``:

En lugar de administrar los eventos uno a uno por
**consultas**, delegamos esa tarea a un sistema que nos
permite **suscribir** y **ser notificado**.

Aquí no mezclamos nuestro código con el sistema de eventos, si
queremos hacer algo relacionado con un evento, escribimos
una función y le pedimos al evento que llame a nuestra
función cuando sea necesario.

Veamos el ejemplo anterior pero usando este enfoque, se
creará una ``Bomba`` cada vez que el usuario 
hace ``click`` en la pantalla:

.. code-block:: python

    def crear_bomba(evento):
        pilas.actores.Bomba(x=evento.x, y=evento.y)
        return true

    pilas.eventos.click_de_mouse.conectar(crear_bomba)

Si queremos que el mouse deje de crear bombas podemos
ejecutar la función ``desconectar``:

.. code-block:: python

    pilas.eventos.click_de_mouse.conectar(crear_bomba)

o simplemente retornar ``False`` en la función ``crear_bomba``.

Nuestro código tendrá *bajo acoplamiento* con los eventos
del motor, y no se nos mezclarán.

De hecho, cada vez que tengas dudas sobre las funciones
suscritas a eventos pulsa F7 y se imprimirán en pantalla.

¿Cómo funciona?
_______________

Ahora bien, ¿cómo funciona el sistema de eventos por dentro?:

El sistema de eventos que usamos es una ligera adaptación
del sistema de señales de django (un framework para desarrollo
de sitios web) dónde cada evento es un objeto que puede
hacer dos cosas:

- suscribir funciones.
- invocar a las funciones que se han suscrito.

1 Suscribir
___________

Por ejemplo, el evento ``mueve_mouse`` es un objeto, y cuando
invocamos la sentencia ``pilas.eventos.mueve_mouse.conectar(mi_funcion)``, 
le estamos diciendo al objeto "quiero que guardes una referencia
a ``mi_funcion``".

Puedes imaginar al evento como un objeto contenedor (similar
a una lista), que guarda cada una de las funciones que le enviamos
con el método ``conectar``.

2 Notificar
___________

La segunda tarea del evento es notificar a todas
las funciones que se suscribieron.

Esto se hace, retomando el ejemplo anterior, cuando el usuario
hace click con el mouse.

Los eventos son objetos ``Signal`` y se inicializan en el
archivo ``eventos.py``, cada uno con sus respectivos
argumentos o detalles:


.. code-block:: python

    click_de_mouse = dispatch.Signal(providing_args=['button', 'x', 'y'])
    pulsa_tecla = dispatch.Signal(providing_args=['codigo'])
    [ etc...]

Los argumentos indican información adicional del evento, en
el caso del click observarás que los argumentos con el botón pulsado
y la coordenada del puntero.

Cuanto se quiere notificar a las funciones conectadas a
un eventos simplemente se tiene que invocar al método ``emitir``
del evento y proveer los argumentos que necesita:

.. code-block:: python

    click_de_mouse.emitir(button=1, x=30, y=50)

Eso hará que todas las funciones suscritas al evento ``click_de_mouse``
se invoquen con el argumento ``evento`` representando esos detalles:

.. code-block:: python

    def crear_bomba(evento):

        print evento.x
        # imprimirá 30

        print evento.y
        # imprimirá 50

        [ etc...]


La parte de pilas que se encarga de llamar a los métodos ``emitir``
es el método ``procesar_y_emitir_eventos`` del
motor, por ejemplo en el archivo ``motores/motor_sfml.py``.

