# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar(titulo='Reloj')
paso_un_segundo = pilas.evento.Evento(['x', 'y'])


class RelojDigital(pilas.actores.Texto):

    def __init__(self):
        pilas.actores.Texto.__init__(self, texto="")
        self.color = pilas.colores.negro
        self.contador = 0
        self.y = -100
        self.x = -10

    def avanzar_segundero(self, evento):
        self.contador += 1
        self.texto = str(self.contador)


class RelojAnalogico(pilas.actores.Actor):

    def __init__(self):
        pilas.actores.Actor.__init__(self, "flecha.png")
        self.centro = ("izquierda", "centro")
        self.rotacion -= 90

    def avanzar_segundero(self, evento):
        self.rotacion += 360 / 60
        pass

reloj1 = RelojDigital()
reloj2 = RelojAnalogico()

paso_un_segundo.conectar(reloj1.avanzar_segundero)
paso_un_segundo.conectar(reloj2.avanzar_segundero)


def funcion_pasa_un_segundo():
    paso_un_segundo.emitir(argumento1=1, argumento2=0)

pilas.escena_actual().tareas.siempre(1, funcion_pasa_un_segundo)

pilas.avisar("Dos actores asociados al mismo evento personalizado.")
pilas.ejecutar()
