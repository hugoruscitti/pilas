# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import os
import sys
import inspect
import utils

class Complementos():
    
    def __init__(self, pilas):
        self.pilas = pilas
        lista_de_plugins = self.__cargar_plugins()
        
        if lista_de_plugins:
            cantidad = len(lista_de_plugins)
            if cantidad == 1:
                print("Se encontro un plugin.")
            else:
                print("Se econtraron %d plugins." %(cantidad))
        else:
            print("No se encontraron plugins.")
            
        self.__aplicar_plugins(lista_de_plugins)

    def __obtener_ruta_de_plugins(self):
        """Returna el path a los plugins de Pila."""
        CONFIG_DIR = self.pilas.utils.obtener_directorio_de_configuracion()
        pilas_home = os.path.join(CONFIG_DIR, '.pilas-engine')
        ruta_de_plugins = os.path.join(pilas_home, 'plugins')
        if not os.path.exists(ruta_de_plugins):
            os.makedirs(ruta_de_plugins)
            self.__crear_ayuda(ruta_de_plugins)

        return ruta_de_plugins

    def __crear_ayuda(self, ruta):
        ruta_al_archivo = os.path.join(ruta, "COMO_CREAR_PLUGINS.txt")
        archivo = open(ruta_al_archivo, 'wt')
        archivo.write("""Para crear plugins tienes construir archivos
terminados en .py con el contenido que quieres ejecutar.

Cada plugin tiene que contener una o mas clases. Una vez que pilas
se inicialice con el argumentos "cargar_plugins=True", todos los
nombres de clases estaran disponibles para utilizar.

Mira el manual para mas detalles: 

 - http://hugoruscitti.github.io/pilas-manual/complementos/index.html
""")
        archivo.close()

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