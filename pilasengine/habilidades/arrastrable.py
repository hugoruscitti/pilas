# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar
from pilasengine import habilidades

class Arrastrable(habilidades.Habilidad):
	def iniciar(self, receptor):
		super(Arrastrable, self).iniciar(receptor)
		self.pilas.eventos.click_de_mouse.conectar(self.comenzar_a_arrastrar)
		self.pilas.eventos.termina_click.conectar(self.termina_de_arrastrar)
		self.pilas.eventos.mueve_mouse.conectar(self.arrastrando)

		self.arrastrando = False

	def comenzar_a_arrastrar(self, evento):
		if evento.boton == 1:
			if self.receptor.colisiona_con_un_punto(evento.x, evento.y):
				self.arrastrando = True

	def arrastrando(self, evento):
		if self.arrastrando:
			self.receptor.x = evento.x
			self.receptor.y = evento.y

	def termina_de_arrastrar(self, evento):
		self.arrastrando = False
