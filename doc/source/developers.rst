Guía para desarrolladores
=========================

Para contribuir en el desarrollo de pilas
necesitas una cuenta en ``bitbucket``, nuestros
proveedores del servicio de repositorios.

El servicio de ``bitbucket`` es gratuito, aunque
tienes que tomarte un poco de tiempo en crear
la cuenta y comenzar a utilizarla.


Mensajes
--------

Cuando un commit tiene que cambiar el estado de alguno
de los bugs que cargamos en el sistema, tienes que
usar alguno de los siguientes mensajes::

    "... fixes #4711 ..."                  # marks issue as resolved
    "... reopening bug 4711..."            # marks issue as open
    "... refs ticket 4711..."              # links changeset to issue as comment
    "... refs bug #4711 and #4712..."      # links to multiple issues
