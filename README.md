# Pilas Engine

Pilas es un motor para realizar videojuegos de manera rápida y sencilla.

Es una herramienta orientada a programadores casuales o principiantes, es ideal para quienes quieran aprender a realizar sus primeros videojuegos.


![](http://www.pilas-engine.com.ar/images/slides/slide1.jpg)


## ¿Cómo empezar?

Una buena forma de comenzar con pilas es instalar todo el kit de desarrollo siguiendo las intrucciones de nuestra web:

- http://www.pilas-engine.com.ar

Y una vez instalada la biblioteca, se puede invocar al comando ``pilas -e`` para ver una lista completa de ejemplos y minijuegos.


## Dependencias

- pyqt4
- pybox2d
- python
- lanas (subrepo)
- kanzen (subrepo)


## Obtener desde repositorio

    git clone http://github.com/hugoruscitti/pilas
    cd pilas
    git submodule init
    git submodule update
    cd lanas
    git submodule init
    git submodule update
    cd ..

## Licencia

Pilas es software libre, y se distribuye bajo la licencia GPLv3.
