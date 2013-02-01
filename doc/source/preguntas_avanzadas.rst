Guía de preguntas avanzadas
===========================


Obtengo errores en ingles al iniciar pilas ¿Que anda mal?
---------------------------------------------------------

Si al ejecutar pilas, ves un mensaje cómo el siguiente::

    X Error: RenderBadPicture (invalid Picture parameter) 163
    Extension: 149 (RENDER)
    Minor opcode: 8 (RenderComposite)
    Resource id: 0x4a0000e

Es muy probable que se deba al adaptador de video. Una forma
de solucionarlo es cambiar la linea de código::

    pilas.iniciar()

por::

    pilas.iniciar(usar_motor='qt')

El motivo de este problema, es que pilas usa una biblioteca llamada
OpenGL, y algunos equipos no lo tienen disponible o con algunos detalles
de configuración.


¿Que es OpenGL?, ¿Cómo se configura en mi equipo?
-------------------------------------------------

OpenGL es una biblioteca que usamos en pilas para que los gráficos
sean mucho mas rápidos y fluidos. OpenGL utiliza aceleración de hardware
y rutinas de optimización avanzadas.

El punto es, que tal vez tu equipo no lo soporte, o no esté correctamente
configurado.

Para saber si tu equipo tiene soporte para opengl, es conveniente que
ejecutes el comando::

    glxinfo | grep rende

Si tu equipo tiene soporte para opengl, tendrías que ver un mensaje
cómo el siguiente::

    direct rendering: Yes
    OpenGL renderer string: Quadro FX 570/PCI/SSE2


Luego, si no tienes soporte, puedes ejecutar el siguiente comando
y volver a intentar::

    sudo apt-get install freeglut3 freeglut3-dev




Obtengo errores de AttributeError por parte de pilas
----------------------------------------------------

El funcionamiento de pilas como módulo de python
es un poquito especial... porque sentencias
como ``pilas.actores`` no funcionarán a menos
que antes escribas ``pilas.iniciar()``.

Por lo tanto, te recomiendo que en tus programas
siempre comiences con un archivo que tenga
algo como esto:

.. code-block:: python

    import pilas
    pilas.iniciar()


es decir, tu programa principal tiene que importar
pilas y luego inicializarlo. Recién ahí podrás
usar el resto de los módulos de pilas.


¿Cómo puedo personalizar el dibujado de un actor?
-------------------------------------------------

Cada vez que se actualiza el bucle de juego
se llama al método ``dibujar`` de cada actor.

Si quieres personalizar por completo la forma en
que se dibuja un actor puedes redefinir el
método ``dibujar`` y listo.

Para mas referencias puedes ver el método ``dibujar``
de la clase ``Actor`` o el método ``dibujar`` de
la clase ``escena.Normal``, que en lugar
de pintar una imagen borra todo el fondo de pantalla.



¿A veces los sonidos no se reproducen?
--------------------------------------

sip... a veces los sonidos no se reproducen porque
python los libera de memoria mientras están sonando.

Entonces, para solucionar el problema tienes que
mantener viva la referencia al objeto ``Sonido`` cuando
quieras reproducir algo. Por ejemplo:

:Ejemplo incompleto: 

    .. code-block:: python

        def reproducir_sonido():
            mi_sonido_que_no_suena = pilas.sonidos.cargar("sonido.wav.")
            mi_sonido_que_no_suena.reproducir()

        reproducir_sonido()

:Ejemplo correcto:

    .. code-block:: python

        sonido = None

        def reproducir_sonido():
            sonido = pilas.sonidos.cargar("sonido.wav")
            sonido.reproducir()

        reproducir_sonido()
    
¿Cual es la diferencia?, en el primer ejemplo el sonido no
se reproducirá porque la referencia ``mi_sonido_que_no_suena`` se
eliminará cuando termine de ejecutar la función ``reproducir_sonido``, mientras
que en el segundo la referencia ``sonido`` seguirá existiendo mientras
el sonido esté reproduciéndose.


Como desinstalo una versión vieja de pilas
------------------------------------------

Pilas de puede desinstalar directamente borrando el cargador
e instalando una versión nueva.

Si has instalado pilas en un sistema linux, también podrías
desinstalar pilas ubicando el directorio de instalación y
borrándolo.

Por ejemplo, con el siguiente comando podemos conocer el directorio
de instalación::

    sudo easy_install -m pilas

En pantalla tendría que aparecer un mensaje cómo::

    Using /usr/lib/python2.7/dist-packages


Este mensaje significa que pilas se buscará dentro de ese
contenedor de directorio. Este directorio puede ser distinto
en tu sistema.

En mi caso, como el directorio es ``/usr/lib/python2.7/dist-packages``,
para desinstalar pilas puedo borrar el directorio ``pilas`` dentro
del directorio anterior:

    rm -r -f /usr/lib/python2.7/dist-packages/pilas

    (IMPORTANTE: puede variar en tu sistema)


Tengo una consulta puntual, ¿quien me puede ayudar?
---------------------------------------------------

Tenemos un foro de mensajes en donde puedes preguntar
lo que quieras sobre pilas, esta es la dirección
web:

http://www.losersjuegos.com.ar/foro/viewforum.php?f=22
