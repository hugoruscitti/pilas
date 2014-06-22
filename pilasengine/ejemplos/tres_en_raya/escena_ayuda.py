# -*- encoding: utf-8 -*-
from pilasengine.escenas import normal
from pilasengine.fondos import fondo


class FondoEscenaAyuda(fondo.Fondo):

    def iniciar(self):
        self.imagen = './data/ayuda.png'


class EscenaAyuda(normal.Normal):
    """Escena que entrega instrucciones de como jugar."""

    def iniciar(self):
        self.fondo = FondoEscenaAyuda(self.pilas)
        self.pulsa_tecla_escape.conectar(self.cuando_se_presione_escape)

    def cuando_se_presione_escape(self, evento):
        """Regresa al menu principal"""
        import escena_menu
        self.pilas.escenas.definir_escena(escena_menu.EscenaMenu(self.pilas))