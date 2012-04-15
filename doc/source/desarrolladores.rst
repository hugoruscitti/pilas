Guía para desarrolladores
=========================

En esta sección veremos como contribuir
en el desarrollo de pilas.

Actualmente se utiliza un control de versiones 
mercurial [#]_ y
un sistema de tickets.

.. [#] http://mercurial.selenic.com

Repositorio
-----------

Para contribuir en el desarrollo de pilas
necesitas una cuenta en ``bitbucket``, nuestros
proveedores del servicio de repositorios.

La dirección de acceso web al respositorio
es:

- http://bitbucket.org/hugoruscitti/pilas

Ten en cuenta que el servicio ``bitbucket`` es
gratuito, aunque tienes que tomarte un poco de
tiempo en crear la cuenta y comenzar a utilizarla.




Obteniendo la última versión del repositio
------------------------------------------

Para obtener la última versión tienes que ejecutar
el siguiente comando desde un terminal::

    hg clone http://bitbucket.org/hugoruscitti/pilas
    
El resultado del comando creará un nuevo directorio
en la carpeta actual llamada ``pilas``.


Primer prueba
-------------

Ingresa en el directorio ``pilas``, ejecuta el comando::

    python

y una vez abierto el intérprete escribe estas dos sentencias::

    import pilas
    pilas.iniciar()

lo que tendrías que ver en la pantalla es una ventana de color
gris. Esa ventana te indicará que todo funciona bien.

Si en lugar de la ventana ves un error de video, lo que tendrías
que ejecutar es la sentencia::

    pilas.iniciar(usar_motor='qt')



Instalación en modo desarrollo
------------------------------

Si sos desarrollador, la forma de instalación mas recomendable
es mediante el comando ``develop``. Esta opción es útil porque te
permite mentener actualizada la biblioteca en todo momento.

Para usar esta opción de instalación tienes que ejecutar el siguiente
comando::

    sudo python setup.py develop

Ten en cuenta que a partir de ahora, cuando uses ``pilas`` en el
sistema, se leerá el código directamente desde ese directorio
en donde has clonado la biblioteca.


Mantenerse actualizado, siempre...
----------------------------------

Dado que ``pilas`` está creciendo, es una buena idea mantener
tu copia del motor actualizada.


Para ello tienes que ingresar en el directorio ``pilas`` y
ejecutar el siguiente comando de manera periódica::

    hg pull
    hg update

De hecho, si usas un lector de noticias sería recomendable
que agregues este ``feed`` a tus marcadores:

- http://bitbucket.org/hugoruscitti/pilas/rss

Ahí se publicarán todas las actualizaciones que se realicen
sobre el repositorio.


Mas detalles
------------

Usamos el modelo de trabajo de bitbucket, haciendo clones
del repositorio principal para luego elaborar los parches.

Si quieres obtener mas detalles te recomiendo ver el artículo
`programando en pilas <http://www.pilas-engine.com.ar/doc/tutoriales/pilas_desarrolladores/pilas_desarrolladores.rst>`_.
