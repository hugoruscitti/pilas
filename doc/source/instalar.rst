Instalación
===========

Existen 3 formas de instalar la biblioteca, así
que veremos cada una por separado.

Instalación fácil, para cada sistema operativo
----------------------------------------------

La forma mas sencilla de instalar pilas es
siguiendo alguno de los tutoriales del sitio
web de pilas:

http://www.pilas-engine.com.ar/documentacion


Instalación para distribuir con un juego
----------------------------------------

Si quieres que la biblioteca esté en un juego pero
no quieres instalarla en cada equipo, puedes
simplemente copiar todo el contenido del directorio
``pilas`` dentro del directorio del juego.

Entonces, cuando ejecutes una sentencia 
como ``import pilas``, la biblioteca se 
leerá desde el directorio.


Instalación luego de la descarga
--------------------------------

Si realizas videojuegos, pero no quieres tener la biblioteca
como directorio físico en todos y cada uno de los juegos
que realices, una buena idea es instalar la biblioteca en
tu sistema.

Primero tienes que instalar ``setuptools`` usando el
siguiente comando::

    sudo apt-get install python-setuptools

Luego, ingresa en el directorio en donde se encuentra
tu copia de pilas y ejecuta un comando cómo::

    sudo python setup.py install

o bien::

    sudo python setup.py develop

En el primer caso la biblioteca se instala y pasa
a estar completamente instalada en tu sistema. No importa
que borres el directorio que has descargado, la biblioteca
quedará instalada en un directorio del sistema para bibliotecas
de python.

El segundo caso es el favorito por los desarrolladores, porque
te permite actualizar mas fácilmente la biblioteca. Ya que
no está complemente instalada en el equipo, si no que hace
referencia al directorio en donde se ha descargado pilas. Si actualizas
el directorio origen, los cambios se reflejarán en
tu sistema sin necesidad de repetir el comando de instalación.

