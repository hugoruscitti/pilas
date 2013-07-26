# -*- encoding: utf-8 -*-
# pilas engine - a video game framework.
#
# copyright 2010 - hugo ruscitti
# license: lgplv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# website - http://www.pilas-engine.com.ar


'''
pilas.dev
=========

Utilidades de desarrollo para Pilas.

Sobre Atributos Desaconsejados
------------------------------

Por defecto la ``PendingDeprecationWarning`` en pilas esta en modo *once* y
``DeprecationWarning`` en *error*.

Si se desea que todos los metodos desaconsejados puedan utilizarse, puede
llamar a la funcion ``pilas.dev.utilizar_desaconsejados(True)``
con lo cual los ``DeprecationWarning`` pasan a estado *once*.

Para manejo avanzado de estas carasterísticas dirijase a documentación
del módulo  `warnings <http://docs.python.org/2/library/warnings.html>`_


'''


import functools
import warnings
import inspect

from pilas import pilasversion


# ATRIBUTOS DESACONSEJADOS

# Seteamos todos los warnings en el estado por defecto
warnings.simplefilter("error", DeprecationWarning)
warnings.simplefilter("once", PendingDeprecationWarning)


def deprecated(se_desactiva_en, se_elimina_en, reemplazo=None, nombre=None):
    """Decorador utilizado para marcar una función como deprecada

    Las excepciones que puede lanzar este decorador son:

    - Si la versión actual de pilas es mayor o igual que ``se_elimina_en``
      y por descuido de los desarrolladores se olvidaron de eliminar
      la llamada a esta función, Siempre se lanza un ``AttributeError``.
    - Si la versión actual de pilas es mayor o igual que ``se_desactiva_en``
      se emite un ``DeprecationWarning``.
    - Si la versión actual de pilas es menor que ``se_desactiva_en``
      se emite un ``PendingDeprecationWarning``.

    :param elemento_deprecado: Cual el nombre del elemento desaconsejado.
    :type elemento_deprecado: str
    :param se_desactiva_en: Indica en que versión de pilas el atributo
                            estará desactivado por defecto. De todas
                            maneras se podran activar con
                            ``pilas.dev.utilizar_desaconsejados(True)``
    :type se_desactiva_en: str
    :param se_elimina_en: Indica en que versión de pilas el atributo
                          se eliminara completamente.
    :type se_elimina_en: str
    :param reemplazo: Indica cuales son las  alternativas a este
                      atributo
    :type reemplazo: str
    :param nombre: Si se desea cambiar el nombre de la función
                   desaconsejada.
    :type nombre: str

    """
    def outer(func):

        @functools.wraps(func)
        def _wraps(*args, **kwargs):

            deprecated_warning(nombre or func.__name__,
                               se_desactiva_en,
                               se_elimina_en,
                               reemplazo)

            return func(*args, **kwargs)
        return _wraps

    return outer


def deprecated_warning(elemento_deprecado, se_desactiva_en,
                       se_elimina_en, reemplazo=None):
    """Lanza la correcta exception/warning de anuncio de que *algo* está en desuso.

    Las excepción/warning que puede lanzar esta función son:

    - Si la versión actual de pilas es mayor o igual que ``se_elimina_en``
      y por descuido de los desarrolladores se olvidaron de eliminar
      la llamada a esta función, Siempre se lanza un ``AttributeError``.
    - Si la versión actual de pilas es mayor o igual que ``se_desactiva_en``
      se emite un ``DeprecationWarning``.
    - Si la versión actual de pilas es menor que ``se_desactiva_en``
      se emite un ``PendingDeprecationWarning``.

    :param elemento_deprecado: Cual el nombre del elemento desaconsejado.
    :type elemento_deprecado: str
    :param se_desactiva_en: Indica en que versión de pilas el atributo
                            estará desactivado por defecto. De todas
                            maneras se podran activar con
                            ``pilas.dev.utilizar_desaconsejados(True)``
    :type se_desactiva_en: str
    :param se_elimina_en: Indica en que versión de pilas el atributo
                          se eliminara completamente.
    :type se_elimina_en: str
    :param reemplazo: Indica cuales son las  alternativas a este
                      atributo
    :type reemplazo: str

    """

    frame, filename, line_number, function_name, lines, index = inspect.getouterframes(inspect.currentframe())[2] if 'deprecated_warning' in inspect.getouterframes(inspect.currentframe())[0][3] else inspect.getouterframes(inspect.currentframe())[1]

    msg_line = "\n+------------------------------------------------+\n"
    msg_line += "La excepcion se produjo en la siguiente llamada:\n"
    msg_line += "Archivo:  %s\nNº Linea: %s\nMetodo:   %s\nLinea:    %s" % (filename, line_number, function_name, lines[index].strip())
    msg_line += "\n+------------------------------------------------+\n\n"


    if pilasversion.compareactual(se_elimina_en) >= 0:
        msg = u"El atributo '{}' no puede utilizarse desde la version {}"
        msg = msg.format(elemento_deprecado, se_elimina_en)
        raise AttributeError(msg)

    msg = "CUIDADO: Utilizar '{}' esta desaconsejado"
    msg = msg.format(elemento_deprecado)

    if reemplazo is not None:
        msg += "; utilice en su lugar: {}".format(reemplazo)

    msg += msg_line

    if pilasversion.compareactual(se_desactiva_en) >= 0:
        warnings.warn(msg, DeprecationWarning, stacklevel=2)
    else:
        warnings.warn(msg, PendingDeprecationWarning, stacklevel=2)


def utilizar_desaconsejados(usar):
    """Permite que se utilicen atributos, métodos y funciones que estan
    desaconsejados en esta versión.

    NOTA: si usted habilita los desaconsejados, los utiliza y luego los
    deshabilita; estos ya estaran disponibles. Esta función debería
    llamarse lo mas temprano posible es un juego y una sola ves.

    :param usar: Si se debe o no permitir que los atributos deprecados
                 puedan utilizarse. Si el *usar* es ``False``, todo lo
                 desaconsejado lanza una excepción; de lo contrario,
                 si *usar* es ``True`` solo se lanza un warning.
    :type usar: bool

    """
    action = "once" if usar else "error"
    warnings.simplefilter(action, DeprecationWarning)
