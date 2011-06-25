Superficies
===========

Anteriormente vimos que los actores podían
tener un aspecto visual, ya sea gracias a
una imagen completa, una grilla o un dibujo
de pizarra.

Pero hay situaciones donde realmente necesitamos
algo mas. En muchas ocasiones necesitamos que
los actores se puedan tener una apariencia que
constuimos programáticamente (si existe la palabra...).


Por ejemplo, imagina que queremos hacer un indicador
de energía, un cronómetro, un indicador de vidas, un
botón etc...

Dibujando sobre superficies
---------------------------

En pilas una superficie es una imagen, pero que no
se carga directamente desde el disco, sino que se
construye en memoria de la computadora, se puede
dibujar sobre ella y luego se le puede aplicar
a un actor como apariencia.

Comencemos con un ejemplo sencillo, imagina que
queremos hacer un actor muy feo, de color "verde"
y con dos ojitos. Lo primero que tenemos que hacer
es crear una superficie, dibujar sobre ella, y luego
crear un actor con esa apariencia:

.. code-block:: python

    import pilas

    pilas.iniciar()

    superficie = pilas.imagenes.cargar_superficie(100, 100)

    # dibujamos el cuerpo
    superficie.circulo(50, 50, 40, color=pilas.colores.verdeoscuro, relleno=True)

    # un ojo
    superficie.circulo(35, 35, 10, color=pilas.colores.blanco, relleno=True)
    superficie.circulo(32, 35, 5, color=pilas.colores.negro, relleno=True)
            
    # el otro ojo
    superficie.circulo(67, 35, 10, color=pilas.colores.blanco, relleno=True)
    superficie.circulo(64, 35, 5, color=pilas.colores.negro, relleno=True)

    pilas.actores.Actor(superficie)

    pilas.ejecutar()


Es decir, una vez que creamos la superficie, en realidad lo que obtenemos
es un objeto que se comporta cómo una imagen, pero con la diferencia
que podemos dibujar sobre ella libremente y crear desde el código la
imagen que queramos.

Ten en cuenta que también estamos mostrando la superficie gracias a un
actor, así que si rotamos el actor o cambiamos su escala la superficie
se observará de forma transformada.

Vamos a ver con mas detalle este recurso de pilas, porque ofrece muchas
mas funcionalidades de las que vemos en este ejemplo.


Creación de una superficie
--------------------------

Para crear una superficie tenemos que invocar a la función ``pilas.imagenes.cargar_superficie``
como vimos mas arriba. Esta función admite dos parámetros que indican
el ancho y el alto de la superficie.

A partir de ese momento, la superficie será completamente transparente, y lo
que dibujemos sobre ella hará que no se note que en realidad es 
un rectángulo. Vale aclarar que efectivamente todas las imágenes de los videojuegos
son rectangulares aunque se disimule...


Coordenadas de las superficies
------------------------------

Las coordenadas que se tienen que especificar para dibujar
sobre una superficie son diferentes a las coordenadas cartesianas
que usamos en la ventana de pilas.

El motivo de este cambio es que las superficies están en la memoria
de la computadora, y es mas sencillo tratar con ellas si usamos
el mismo sistema de coordenadas que se usa en casi todas las aplicaciones
gráficas. Ten en cuenta que estas son funciones avanzadas y
que generalmente se trabaja sobre estas funciones unas pocas veces
para lograr lo que ya no está implementado como un actor...

El sistema de coordenadas de las superficies tiene su origen
en la esquina superior izquierda (0, 0), luego el eje ``x`` crece
hacia la derecha y el eje ``y`` crece hacia abajo.

