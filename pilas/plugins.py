# -*- encoding: utf-8 -*-

import os
import sys
import inspect


def obtener_ruta_de_plugins():
    """Returna el path a los plugins de Pila."""
    return os.path.expanduser('~/.pilas/plugins')


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


def cargar_plugins(lista_de_plugins_por_cargar):
    """Importa la lista de plugins dado. Retorna una lista
    de modulos de plugins importados."""

    # agrego el directorio de plugin al sys.path
    ruta_de_plugins = obtener_ruta_de_plugins()
    if not ruta_de_plugins in sys.path:
        sys.path.append(ruta_de_plugins)

    lista_de_plugins_importados = list()
    plugins_encontrados = lista_de_plugins_encontrados()

    # lista 'flag' para importar todos los plugins
    TODOS_LOS_PLUGINS = ['todos']

    if lista_de_plugins_por_cargar == TODOS_LOS_PLUGINS:
        for plugin in plugins_encontrados:
            plugin_importado = __import__(plugin)
            lista_de_plugins_importados.append(plugin_importado)
    else:
        for plugin in lista_de_plugins_por_cargar:
            if plugin not in plugins_encontrados:
                raise Exception('Plugin %s no encontrado.' % plugin)
            plugin_importado = __import__(plugin)
            lista_de_plugins_importados.append(plugin_importado)
    return lista_de_plugins_importados


def aplicar_plugins_en_habilidades(lista_de_plugins, habilidades):
    """Aplica los modulos de plugins dados a las habilidades."""

    for modulo_de_plugin in lista_de_plugins:
        miembros_del_plugin = inspect.getmembers(modulo_de_plugin)
        for miembro in miembros_del_plugin:
            nombre_de_clase, clase = miembro
            if not inspect.isclass(clase):
                continue
            setattr(habilidades, nombre_de_clase, clase)
    return habilidades

