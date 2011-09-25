============
Pilas Engine
============

Pilas es un motor para realizar videojuegos de manera
rápida y sencilla.

Es una herramienta orientada a programadores casuales
o principiantes, que quiera comenzar a realizar sus
primeros videojuegos.


¿Cómo empezar?
==============

Una buena forma de comenzar con pilas es instalar todo
el kit de desarrollo siguiendo las intrucciones de
nuestra web: http://www.pilas-engine.com.ar


Y una vez instalada la biblioteca, se puede invocar
al comando ``pilas -e`` para ver una lista completa
de ejemplos y minijuegos.


¿Cómo generar la documentación del proyecto?
============================================

Para generar la documentación del proyecto
usamos ``Sphinx``, el sistema de documentación
mas utilizado en los proyectos de python.

Para generar los archivos PDF o HTML usamos el comando
``make`` dentro del directorio ``doc``. El archivo que
dispara todas las acciones que sphinx sabe hacer están
definidas en el archivo ``Makefile``.

Recuerda instalar ``sphinx`` antes de continuar, si solo
quieres generara la documentación HTML alcanza con
ejecutar este comando::

    apt-get install python-sphinx

y en caso de que quieras generar la documentación PDF::

    apt-get install texlive-lang-spanish


Otros recursos en la web
========================

Existen varios sitios web importantes dentro
de proyecto pilas, la web principal
es:

    - http://www.pilas-engine.com.ar

y los sitios para desarrolladores, donde se encuentran
las tareas y el repositorio de código son:

    - http://www.dev-losersjuegos.com.ar
    - http://bitbucket.org/hugoruscitti/pilas


También tenemos una lista de correo en
la siguiente dirección:

    - http://groups.google.com/group/pilas-engine

Dependencias
============

- pygame
- pyqt4
- pybox2d
- python


Licencia
========

Pilas es software libre, y se distribuye bajo la
licencia GPLv3.


Test de unidad
==============

Para realizar pruebas de unidad estamos usando ``py.test``. Para
ello tienes que instalar una nueva dependencia con el
comando::

    sudo easy_install pytest

y luego correr todas las pruebas con los siguientes comandos::

    make test

Créditos y agradecimientos
==========================

Pilas está principalmente desarrollada por Hugo Ruscitti, y
cuenta con varios dibujos realizados por Walter Velazquez. Ambos
fundadores de Losersjuegos (http://www.losersjuegos.com.ar).

A continuación se incluye una lista de otros desarrolladores
y proyectos que sumaron a pilas:

PyTweener
---------

Las interpolaciones dentro del motor se realizan
mediante la biblioteca pyTweener, distribuida
bajo la licencia M.I.T. por Ben Harling.

Dispatch
--------

El modulo ``pilas.dispatch`` se adoptó del
core de Django, y estába basado en el proyecto pydispatch.


PyQt4
-----

Todo el manejo multimedia se realiza gracias a la biblioteca
Qt4:

- http://qt.nokia.com/


pygame
------

Como biblioteca multimedia secundaria usamos
pygame, que además nos permite seleccionarla
en casos donde no hay soporte para OpenGL (como
en los equipos OLPC por ejemplo).

Box2d
-----

Para el manejo multimedia estamos usando
la biblioteca box2d:

- http://code.google.com/p/pybox2d/

GFXLib
------

He utilizado los siguientes gráficos del proyecto
gfxlib:

- pilas/data/moneda.png

Estos gráficos se distribuyen bajo la licencia "Common Public License", y
puedes obtener mas información en: http://www.spicypixel.net

¡ Gracias Marc !


DANC, de lostgarden.com
-----------------------

En pilas utilizamos algunos gráficos que DANC publicó
en su sitio web:

- www.lostgarden.com


a "arboris"
-----------

Por sus gráficos de naves que se pueden
descargar desde la siguiente web:

- http://arboris.deviantart.com/art/Spaceship-sprites-43030167
