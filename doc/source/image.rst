Cargar imágenes
===============

En los videojuegos 2d las imágenes suelen estar en formatos
gráficos como png o jpg ya diseñados con anterioridad.

En ``pilas`` se pueden cargar estos recursos usando
el módulo ``image``. Por ejemplo, si tenemos una
imágen llamada ``hola.png`` podríamos incorporarla a
nuestro juego así::

    import pilas

    hola = pilas.image.load('hola.png')
