.. _ref_desarrolladores:


Guía para desarrolladores
=========================

En esta sección veremos como contribuir en el desarrollo de pilas, mostrando
las herramientas de desarrollo y dando algunas recomendaciones.

Actualmente utilizamos Git junto a los servicios de github_.

.. _github: http://github.com


Repositorio
-----------

Para contribuir en el desarrollo de pilas
necesitas una cuenta de usuario en github_, nuestros
proveedores del servicio de repositorios.

La dirección de acceso web al respositorio
es:

- http://github.com/hugoruscitti/pilas

Ten en cuenta que el servicio github_ es gratuito, y
solo lleva unos minutos registrarse.


Obteniendo la última versión del repositio
------------------------------------------

Para obtener la última versión tienes que ejecutar
el siguiente comando desde un terminal::

    git clone http://github.com/hugoruscitti/pilas
    
Luego aparecerá un directorio llamado ``pilas``, con el contenido completo
del repositorio.


Primer prueba
-------------

Ingresa en el directorio ``pilas``, ejecuta el comando::

    python bin/pilas


debería aparecer en pantalla el asistente de primer inicio.


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

    git pull

Mas detalles
------------

Usamos el modelo de trabajo de github_, haciendo ``forks`` y ``pull requests``.

Si quieres obtener mas detalles te recomiendo ver el siguiente artículo:

- http://www.cocoanetics.com/2012/01/github-fork-fix-pull-request/


Referencias para desarrolladores
--------------------------------

.. automodule:: pilas.pilasversion
   :members:

.. automodule:: pilas.dev
   :members: