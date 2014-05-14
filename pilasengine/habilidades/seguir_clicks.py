from pilasengine import habilidades

class SeguirClicks(habilidades.Habilidad):
	def iniciar(self, receptor):
		super(SeguirClicks, self).iniciar(receptor)
		self.pilas.eventos.click_de_mouse.conectar(self.moverse_a_este_punto)

	def moverse_a_este_punto(self, evento):
		self.receptor.x = [evento.x], 0.5	
		self.receptor.y = [evento.y], 0.5		
