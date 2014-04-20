# -*- encoding: utf-8 -*-

class Grupo(object):
    """
    Representa un grupo que puede almacenar actores.

    Los grupos pueden ser útiles para clasificar y organizar
    _actores dentro de un juego. Por ejemplo, todas las naves
    en un grupo, los enemigos en otro grupo y las estrellas
    en otro etc.

    Para crear un grupo y asignarle un actor podemos escribir:

        >>> grupo = pilas.actores.Grupo()
        >>> actor = pilas.actores.Actor()
        >>> grupo.agregar(actor)

    """

    def __init__(self, pilas):
        self.pilas = pilas
        self.pilas.log("Creando el grupo", self)
        self._actores = []
        self._actores_a_eliminar = []

    def obtener_cantidad_de_actores(self):
        return len(self._actores)

    def eliminar(self, actor):
        """Agrega el actor a una lista para eliminarlo mas tarde."""
        self.pilas.log("Eliminando el actor", actor, "del grupo", self)

        if actor in self._actores_a_eliminar:
            self.pilas.log("El actor solicitado ya fue eliminado")
        elif actor in self._actores:
            self._actores_a_eliminar.append(actor)
            actor.eliminar_del_grupo(self)
        else:
            raise Exception("No se puede eliminar el actor porque no está en el grupo.")

    def agregar(self, actor):
        self.pilas.log("Agregando el actor", actor, "al grupo", self)
        self._actores.append(actor)
        self.pilas.log("Haciendo que el actor", actor, "tenga una referencia al", self)
        actor.agregar_al_grupo(self)

    def obtener_actores(self):
        return list(self._actores)

    def actualizar_eliminados(self):
        self.pilas.log("Actualizando el grupo", self, "en busca de actores para eliminar.")

        for x in self._actores_a_eliminar:
            self._actores.remove(x)

        self._actores_a_eliminar = []