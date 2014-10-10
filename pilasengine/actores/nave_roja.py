# -*- encoding: utf-8 -*-
# pilas engine: un motor para hacer videojuegos
#
# Copyright 2010-2014 - Hugo Ruscitti
# License: LGPLv3 (see http://www.gnu.org/licenses/lgpl.html)
#
# Website - http://www.pilas-engine.com.ar


from pilasengine.actores.actor import Actor


class NaveRoja(Actor):

    def iniciar(self):
        self.ruta_imagen_normal = "nave_roja/nave.png"
        self.ruta_imagen_izquierda = "nave_roja/nave_izquierda.png"
        self.ruta_imagen_derecha = "nave_roja/nave_derecha.png"

        self.radio_de_colision = 33
        self.velocidad_x = 0
        self.velocidad_y = 0
        self.velocidad = 5
        self.disparos = []
        self._contador_demora = 0
        self.demora_entre_disparos = 5
        self.disparo_doble = True
        self.cuando_elimina_enemigo = False

    def actualizar(self):
        control = self.pilas.control

        self.x += self.velocidad_x
        self.y += self.velocidad_y

        if control.izquierda:
            self.velocidad_x -= self.velocidad
            self.imagen = self.ruta_imagen_izquierda
        elif control.derecha:
            self.velocidad_x += self.velocidad
            self.imagen = self.ruta_imagen_derecha
        else:
            self.imagen = self.ruta_imagen_normal

        if control.arriba:
            self.velocidad_y += self.velocidad
        elif control.abajo:
            self.velocidad_y -= self.velocidad
            
        if control.boton:
            self.intenta_disparar()
            
        self._contador_demora += 1

        # Aplica una desaceleración al movimiento de la nave.
        self.velocidad_x *= 0.5
        self.velocidad_y *= 0.5

    def terminar(self):
        pass
    

    def intenta_disparar(self):
        if self._contador_demora > self.demora_entre_disparos:
            self._contador_demora = 0
            self.crear_disparo()
            
    def crear_disparo(self):
        if self.disparo_doble:
            disparo1 = self.pilas.actores.DisparoLaser(x=self.izquierda + 10, y=self.y, rotacion=90)
            self.disparos.append(disparo1)

            disparo2 = self.pilas.actores.DisparoLaser(x=self.derecha - 10, y=self.y, rotacion=90)
            self.disparos.append(disparo2)
            disparo1.z = self.z + 1
            disparo2.z = self.z + 1
        else:
            disparo1 = self.pilas.actores.DisparoLaser(x=self.x, y=self.y, rotacion=90)
            self.disparos.append(disparo1)
            disparo1.z = self.z + 1
            
    def definir_enemigos(self, grupo):
        """Hace que una nave tenga como enemigos a todos los actores del grupo."""
        self.pilas.colisiones.agregar(self.disparos, grupo, self.hacer_explotar_al_enemigo)

    def hacer_explotar_al_enemigo(self, mi_disparo, el_enemigo):
        """Es el método que se invoca cuando se produce una colisión 'tiro <-> enemigo'
        """
        mi_disparo.eliminar()
        el_enemigo.eliminar()