# -*- encoding: utf-8 -*-
import pilasengine

pilas = pilasengine.iniciar(titulo='Reloj')
paso_un_segundo = pilas.evento.Evento(['x', 'y'])


class RelojDigital(pilasengine.actores.ActorInvisible):

    def iniciar(self):
        self.color = pilas.colores.negro
        self.contador = 0
        self.y = -100
        self.x = -10
        self.actor_texto = self.pilas.actores.Texto(cadena_de_texto='')

    def avanzar_segundero(self, evento):
        self.contador += 1
        self.actor_texto.texto = str(self.contador)


class RelojAnalogico(pilasengine.actores.Actor):

    def iniciar(self):
        self.imagen = 'flecha.png'
        self.centro = ("izquierda", "centro")
        self.rotacion = 90

    def avanzar_segundero(self, evento):
        self.rotacion -= 360 / 60
        pass

pilas.actores.vincular(RelojAnalogico)
pilas.actores.vincular(RelojDigital)

reloj1 = pilas.actores.RelojDigital()
reloj2 = pilas.actores.RelojAnalogico()

paso_un_segundo.conectar(reloj1.avanzar_segundero)
paso_un_segundo.conectar(reloj2.avanzar_segundero)


def funcion_pasa_un_segundo():
    paso_un_segundo.emitir(argumento1=1, argumento2=0)

pilas.tareas.siempre(1, funcion_pasa_un_segundo)

pilas.avisar("Dos actores asociados al mismo evento personalizado.")
pilas.ejecutar()
