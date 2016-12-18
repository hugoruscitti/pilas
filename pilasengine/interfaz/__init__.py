# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine import colores

class Interfaz(object):
    """Representa la propiedad pilas.fondos

    Este objeto se encarga de hacer accesible
    la creación de fondos para las escenas.
    """

    def __init__(self, pilas):
        self.pilas = pilas

    def Boton(self, texto='Sin texto', x=0, y=0):
        import boton
        return boton.Boton(self.pilas, texto, x=x, y=y)

    def Deslizador(self, x=0, y=0):
        import deslizador
        return deslizador.Deslizador(self.pilas, x=x, y=y)

    def Selector(self, texto='Sin texto', x=0, y=0):
        import selector
        return selector.Selector(self.pilas, texto, x=x, y=y)

    def IngresoDeTexto(self, texto='Sin texto', x=0, y=0, ancho=300, limite_de_caracteres=20, icono=None):
        import ingreso_de_texto
        return ingreso_de_texto.IngresoDeTexto(self.pilas, texto, x=x, y=y, ancho=ancho, limite_de_caracteres=limite_de_caracteres, icono=icono)

    def ListaSeleccion(self, opciones=['primer opcion'], funcion_a_ejecutar=None, x=0, y=0):
        import lista_seleccion
        return lista_seleccion.ListaSeleccion(self.pilas, opciones=opciones,
                               funcion_a_ejecutar=funcion_a_ejecutar, x=x, y=y)
