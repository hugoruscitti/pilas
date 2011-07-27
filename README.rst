Pilas
=====

Un motor de videojuegos que presenta una manera sencilla (y algo experimental)
de hacer videojuegos.


Recursos en la web
==================

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
- pybox
- python


Licencia
========


- GPLv3.


Créditos
========

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


a Anthony Long
--------------

Por realizar la biblioteca ``assertlib``, que se encuentra
en el directorio ``pilas/test/assertlib``, y que se utiliza
para simplificar los tests de unidad.

- http://www.antlong.com/

a arboris
---------

Por sus gráficos de naves que se pueden
descargar desde la siguiente web:

- http://arboris.deviantart.com/art/Spaceship-sprites-43030167
