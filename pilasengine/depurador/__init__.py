# -*- encoding: utf-8 -*-
from pilasengine.depurador.modo_info import ModoInformacionDeSistema

class Depurador(object):

    def __init__(self, pilas):
        self.pilas = pilas
        self._modos = []
        self.lienzo = pilas.imagenes.crear_superficie(500, 500)

    def desactivar_todos_los_modos(self):
        self._modos = []

    def realizar_dibujado(self, painter):
        """Realiza un dibujado de los modos depuración habilitados.

        Hay dos rutinas de dibujado en cada modo, una dibujado general
        que se suele utilizar para pintar textos o estadísticas y otra
        rutina que se llama cada vez que se inspecciona un actor.
        """
        if self._modos:
            actores_de_la_escena = self.pilas.obtener_escena_actual()._actores.obtener_actores()

            # Dibujado depuración de cada modo.
            for a in actores_de_la_escena:
                for m in self._modos:
                    m.dibujar_actor(a, painter)

            # Dibujado general del modo.
            for m in self._modos:
                m.realizar_dibujado(painter)

    def obtener_modos_habilitados(self):
        """Retorna una lista con los nombres de los modos habilitados."""
        modos = [x.__class__.__name__ for x in self._modos]
        return modos

    def definir_modos(self, info=False, radios=False, posiciones=False,
                      puntos_de_control=False, areas=False,
                      fisica=False):
        """Permite habilitar o deshabilitar los modos depuración.

        Cada uno de los argumentos representa un modo depuración, el valor True
        habilita el modo, False lo deshabilita.
        """

        modos_habilitados = self.obtener_modos_habilitados()
        modos_solicitados = []

        if info:
            modos_solicitados.append('ModoInformacionDeSistema')

        if radios:
            modos_solicitados.append('ModoRadiosDeColision')

        if posiciones:
            modos_solicitados.append('ModoPosicion')

        if puntos_de_control:
            modos_solicitados.append('ModoPuntosDeControl')

        if areas:
            modos_solicitados.append('ModoArea')

        if fisica:
            modos_solicitados.append('ModoFisica')

        modos = set(modos_habilitados).symmetric_difference(modos_solicitados)

        if 'ModoInformacionDeSistema' in modos:
            self._alternar_modo(ModoInformacionDeSistema)

        if 'ModoPuntosDeControl' in modos:
            self._alternar_modo(ModoPuntosDeControl)

        if 'ModoRadiosDeColision' in modos:
            self._alternar_modo(ModoRadiosDeColision)

        if 'ModoArea' in modos:
            self._alternar_modo(ModoArea)

        if 'ModoFisica' in modos:
            self._alternar_modo(ModoFisica)

        if 'ModoPosicion' in modos:
            self._alternar_modo(ModoPosicion)

    def _alternar_modo(self, clase_del_modo):
        clases_activas = self.obtener_modos_habilitados()

        if clase_del_modo.__name__ in clases_activas:
            self._desactivar_modo(clase_del_modo)
        else:
            self._activar_modo(clase_del_modo)

    def _activar_modo(self, clase_del_modo):
        instancia_del_modo = clase_del_modo(self.pilas, self)
        self._modos.append(instancia_del_modo)
        self._modos.sort(key=lambda x: x.orden_de_tecla())

    def _desactivar_modo(self, clase_del_modo):
        instancia_a_eliminar = [x for x in self._modos
                                if x.__class__ == clase_del_modo]
        self._modos.remove(instancia_a_eliminar[0])
        instancia_a_eliminar[0].sale_del_modo()