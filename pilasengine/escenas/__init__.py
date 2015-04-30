# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

import traceback
import inspect

from pilasengine.escenas.normal import Normal
from pilasengine.escenas.escena import Escena
from pilasengine.escenas.error import Error


class Escenas(object):
    """Representa la propiedad pilas.escenas

    Este objeto se encarga de hacer accesibles
    todas las escenas que incluye pilas.

    Por ejemplo, cuando un programador escribe
    "pilas.escenas.Normal()", en realidad está
    llamando a un método llamado Normal() que
    retorna un objeto escena listo para
    utilizar.
    """

    _lista_escenas_personalizadas = []

    def __init__(self, pilas=None):
        self.pilas = pilas
        self.pila_de_escenas = []
        self.escena_actual = None
        self.iteraciones = 0

    def definir_escena(self, escena):
        mensaje = "El método definir_escena está en desuso..."
        raise Error(mensaje)

    def obtener_escena_actual(self):
        return self.escena_actual

    def realizar_actualizacion_logica(self):
        escena = self.obtener_escena_actual()

        # Resuelve un bug raro que activaba todos los callbacks de colisiones
        # cuando se usaba pilas desde un script. Resulta que en el instante
        # inicial de armar la escena todas las figuras fisicas están en la
        # coordenada (0, 0), y se necesita iterar al menos dos veces para
        # asegurarse que la fisica actualice las coordenadas y recién ahí
        # analizar colisiones.
        if self.iteraciones < 2:
            escena.colisiones.limpiar()
            self.iteraciones += 1
        else:
            escena.colisiones.actualizar()

        escena.cuando_actualiza.emitir()
        escena.actualizar_fisica()
        escena.actualizar_actores()
        escena.actualizar_interpolaciones()
        escena.tareas.actualizar(1/60.0)
        escena.actualizar()

    def realizar_actualizacion_logica_en_modo_pausa(self):
        escena = self.obtener_escena_actual()
        escena.actualizar_interpolaciones_en_modo_pause()

    def forzar_actualizacion_de_interpolaciones(self):
        escena = self.obtener_escena_actual()
        escena.forzar_actualizacion_de_interpolaciones()

    def simular_actualizacion_logica(self):
        escena = self.obtener_escena_actual()
        escena.cuando_actualiza.emitir()
        escena.actualizar_actores()
        escena.tareas.actualizar(1/60.0)
        escena.actualizar_interpolaciones(1/60.0)
        escena.actualizar()

    def realizar_dibujado(self, painter):
        escena = self.obtener_escena_actual()
        escena.dibujar_actores(painter)

    def vincular(self, clase_de_la_escena):
        """Permite vincular una escena personalizada a las escenas de pilas.

        Esto permite de después la escena se pueda crear directamente
        desde el módulo "pilas.escenas".

        Por ejemplo, si tengo una clase ``MiEscena`` la puedo
        vincular son las siguientes sentencias:

            >>> pilas.escenas.vincular(MiEscena)
            >>> mi_escena = pilas.escenas.MiEscena()

        y si necesito especificar opciones de inicio, tengo que definirlas
        en el método iniciar de la clase y luego invocarlas al crear la
        escena:

            >>> mi_escena_con_argumentos = pilas.escenas.MiEscena(ejemplo=123)

        """

        # Se asegura de que la clase sea una escena.
        if not issubclass(clase_de_la_escena, Escena):
            mensaje = "Solo se pueden vincular clases que heredan de pilasengine.escenas.Escena"
            raise Exception(mensaje)

        def metodo_crear_escena(self, *k, **kw):
            try:
                nueva_escena = clase_de_la_escena(self.pilas)
            except TypeError, error:
                print traceback.format_exc()
                mensaje_extendido = "\n\t(en la clase %s solo se deberia esperar el argumento pilas" %(str(clase_de_la_escena.__name__))
                raise TypeError(str(error) + mensaje_extendido)

            self.sustituir_escena_actual(nueva_escena)

            try:
                nueva_escena.iniciar(*k, **kw)
            except TypeError, error:
                print traceback.format_exc()
                nombre = clase_de_la_escena.__name__
                argumentos_esperados = str(inspect.getargspec(clase_de_la_escena.iniciar))
                argumentos = str(k) + " " + str(kw)
                mensaje_extendido = "\nLa clase %s arrojó un error al ser inicializada, asegurá que el método %s.iniciar (que solo admite los argumetos: %s) en realidad fue invocada con los argumentos: %s" %(nombre, nombre, argumentos_esperados, argumentos)
                raise TypeError(str(error) + mensaje_extendido)


            return nueva_escena


        # Se asegura de que la escena no fue vinculada anteriormente.
        nombre = clase_de_la_escena.__name__
        existe = getattr(self.__class__, nombre, None)

        if existe:
            mensaje = "Lo siento, ya exista una escena vinculada con el nombre: " + nombre
            raise Exception(mensaje)

        # Vincula la clase anexando el metodo constructor.
        setattr(self.__class__, nombre, metodo_crear_escena)
        Escenas._lista_escenas_personalizadas.append(nombre)

    def obtener_escenas_personalizadas(self):
        "Retorna una lista con todos los nombres de actores personalizados."
        return Actores._lista_escenas_personalizadas

    def eliminar_escenas_personalizadas(self):
        "Recorre todos los actores personalizados y los elimina."
        for x in Escenas._lista_escenas_personalizadas:
            delattr(self.__class__, x)

        Escenas._lista_escenas_personalizadas = []
        self.vincular(Normal)
        self.vincular(Error)

    def sustituir_escena_actual(self, escena):
        if self.escena_actual:
            self.escena_actual.eliminar_el_motor_de_fisica()
            del self.escena_actual
            import gc
            gc.collect()

        self.pilas.log("Definiendo como activa la escena", escena)
        self.escena_actual = escena
        return escena

    def es_escena_vinculada(self, nombre_de_la_escena):
        return nombre_de_la_escena in self._lista_escenas_personalizadas
