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

Nuestro repositorio se encuentra bajo el control
de versiones ``mercurial``.

Para obtener la última versión tienes que ejecutar
el comando::

    hg clone http://bitbucket.org/hugoruscitti/pilas
    
El resultado del comando creará un nuevo directorio
en tu sistema llamado ``pilas``.


Primer prueba
-------------

Ingresa en el directorio ``pilas``, ejecuta el comando::

    python

y una vez dentro del intérprete ejecuta la sentencia::

    import pilas

entonces, si aparece una ventana de color gris significa que
todo ha funcionado correctamente. Ahora puedes proceder a
instalar la biblioteca en tu sistema.

Instalación en modo desarrollo
------------------------------

La opción de instalación mas recomendada, es la instalación en
modo desarrollo. Ya que te permite mantener actualizada todo
el tiempo tu versión de la biblioteca.

Para usar esta opción de instalación tienes que ejecutar el siguiente
comando::

    sudo python setup.py develop


Mantenerse actualizado, siempre...
----------------------------------

Dado que ``pilas`` está creciendo, es una buena idea mantener
tu copia del motor actualizada.

Para ello tienes que ingresar en el directorio ``pilas`` y
ejecutar el siguiente comando de manera periódica::

    hg pull
    hg update

De hecho, si usas un lector de noticias sería recomendable
que agregues este ``feed``:

- http://bitbucket.org/hugoruscitti/pilas/rss

Ahí se publicarán todas las actualizaciones que se realicen
sobre el repositorio.


Mas detalles
------------

Usamos el modelo de trabajo de bitbucket, haciendo clones
del repositorio principal para luego elaborar los parches.

Si quieres obtener mas detalles te recomiendo ver el artículo
`programando en pilas <http://www.pilas-engine.com.ar/doc/tutoriales/pilas_desarrolladores/pilas_desarrolladores.rst>`_.
