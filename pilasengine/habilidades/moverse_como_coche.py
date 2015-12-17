# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar

from pilasengine.habilidades import moverse_con_el_teclado


class MoverseComoCoche(moverse_con_el_teclado.MoverseConElTeclado):
    "Hace que un actor se mueva como un coche."

    def iniciar(self, receptor, control=None, velocidad_maxima=4,
                aceleracion=0.06, deceleracion=0.1,
                rozamiento=0, velocidad_rotacion=1,marcha_atras=True):
        super(MoverseComoCoche, self).iniciar(receptor,
                                              control=control,
                                              velocidad_maxima=velocidad_maxima,
                                              aceleracion=aceleracion,
                                              deceleracion=deceleracion,
                                              velocidad_rotacion=
                                              velocidad_rotacion,
                                              con_rotacion=True,
					      marcha_atras=marcha_atras)

        self._rozamiento = rozamiento
        self._velocidad_maxima_aux = self.velocidad_maxima

    def set_rozamiento(self, nivel_rozamiento):
        self._rozamiento = nivel_rozamiento
        self.velocidad_maxima = self._velocidad_maxima_aux - self._rozamiento

    def get_rozamiento(self):
        return self._rozamiento

    def set_velocidad_maxima(self, velocidad):
        self._velocidad_maxima = velocidad
        self._velocidad_maxima_aux = self._velocidad_maxima

    def get_velocidad_maxima(self):
        return self.velocidad_maxima

    rozamiento = property(get_rozamiento, set_rozamiento, doc="Define el \
                          rozamiento del coche con la superficie por \
                          donde circula.")
