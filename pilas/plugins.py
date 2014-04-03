# -*- encoding: utf-8 -*-

import os
import sys
import inspect
import utils

class Complementos():
    def __init__(self):
        lista_de_plugins = self.__cargar_plugins()
        self.__aplicar_plugins(lista_de_plugins)

    def __obtener_ruta_de_plugins(self):
        """Returna el path a los plugins de Pila."""
        CONFIG_DIR = utils.obtener_directorio_de_configuracion()
        pilas_home = os.path.join(CONFIG_DIR, 'pilas-engine')
        ruta_de_plugins = os.path.join(pilas_home, 'plugins')
        if not os.path.exists(ruta_de_plugins):
            os.makedirs(ruta_de_plugins)

        return ruta_de_plugins


    def __lista_de_plugins_encontrados(self):
        """Retorna una lista de plugins encontrados de Pilas."""
        directorio_de_plugins = self.__obtener_ruta_de_plugins()
        lista_de_plugins = list()
        for archivo in os.listdir(directorio_de_plugins):
            if not archivo.endswith('.py'):
                continue
            nombre_del_plugin, _ = archivo.split('.py')
            lista_de_plugins.append(nombre_del_plugin)
        return lista_de_plugins


    def __cargar_plugins(self):
        """Importa la lista de plugins dado. Retorna una lista
        de modulos de plugins importados."""

        # agrego el directorio de plugin al sys.path
        ruta_de_plugins = self.__obtener_ruta_de_plugins()
        if not ruta_de_plugins in sys.path:
            sys.path.append(ruta_de_plugins)

        plugins_encontrados = self.__lista_de_plugins_encontrados()
        lista_de_plugins_importados = list()

        for plugin in plugins_encontrados:
            plugin_importado = __import__(plugin)
            lista_de_plugins_importados.append(plugin_importado)

        return lista_de_plugins_importados


    def __aplicar_plugins(self, lista_de_plugins):
        """Aplica los modulos de plugins dados a las habilidades."""
        for modulo_de_plugin in lista_de_plugins:
            for nombre_de_clase, clase in inspect.getmembers(modulo_de_plugin):
                setattr(self, nombre_de_clase, clase)