# -*- encoding: utf-8 -*-

import os
import sys
import inspect
from pilas import (
    habilidades,
)


if sys.platform == 'win32':
    # won't find this in linux; pylint: disable=F0401
    from win32com.shell import shell, shellcon
    CONFIG_DIR = shell.SHGetFolderPath(0, shellcon.CSIDL_PROFILE, None, 0)
    del shell, shellcon
else:
    from xdg import BaseDirectory
    CONFIG_DIR = BaseDirectory.xdg_config_home
    del BaseDirectory


def obtener_ruta_de_plugins():
    """Returna el path a los plugins de Pila."""
    pilas_home = os.path.join(CONFIG_DIR, 'pilas')
    ruta_de_plugins = os.path.join(CONFIG_DIR, pilas_home, 'plugins')
    if not ruta_de_plugins:
        os.makedirs(ruta_de_plugins)
    return ruta_de_plugins


def lista_de_plugins_encontrados():
    """Retorna una lista de plugins encontrados de Pilas."""
    directorio_de_plugins = obtener_ruta_de_plugins()
    lista_de_plugins = list()
    for archivo in os.listdir(directorio_de_plugins):
        if not archivo.endswith('.py'):
            continue
        nombre_del_plugin, _ = archivo.split('.py')
        lista_de_plugins.append(nombre_del_plugin)
    return lista_de_plugins


def cargar_plugins(cargar_plugins):
    """Importa la lista de plugins dado. Retorna una lista
    de modulos de plugins importados."""

    # agrego el directorio de plugin al sys.path
    ruta_de_plugins = obtener_ruta_de_plugins()
    if not ruta_de_plugins in sys.path:
        sys.path.append(ruta_de_plugins)
    if not cargar_plugins:
        return

    plugins_encontrados = lista_de_plugins_encontrados()
    for plugin in plugins_encontrados:
        if es_plugin_de_habilidad(plugin):
            cargar_plugin_de_habilidad(plugin)


def es_plugin_de_habilidad(plugin):
    """Retorna True si el plugin dado es una clase qeu hereda de
    Habilidad."""
    return issubclass(plugin, habilidades.Habilidad)


def cargar_plugin_de_habilidad(plugin):
   """Agrega un nuevo plugin a las habilidades de pilas."""
   _ = __import__(plugin)
   setattr(habilidades, _.__name__, _.__class__)
