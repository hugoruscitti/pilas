from pilasengine import habilidades

class AumentarConRueda(habilidades.Habilidad):
	def iniciar(self, receptor):
		super(AumentarConRueda, self).iniciar(receptor)
		self.pilas.eventos.mueve_rueda.conectar(self.cambiar_de_escala)

	def cambiar_de_escala(self, evento):
		self.receptor.escala += evento.delta/4.0
