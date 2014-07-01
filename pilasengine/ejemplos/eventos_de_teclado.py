import pilasengine
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas = pilasengine.iniciar()

tecla_que_se_pulsa = pilas.actores.Texto("",  y=0,  ancho=300)
tecla_que_se_suelta = pilas.actores.Texto("", y=-30, ancho=300)

def cuando_pulsa_tecla(evento):
    tecla_que_se_pulsa.texto = "Tecla pulsada: %s" %(evento.texto)

def cuando_suelta_tecla(evento):
    tecla_que_se_pulsa.texto = "Tecla pulsada: "
    tecla_que_se_suelta.texto = "Tecla que se suelta: %s" %(evento.texto)
		
pilas.eventos.pulsa_tecla.conectar(cuando_pulsa_tecla)
pilas.eventos.suelta_tecla.conectar(cuando_suelta_tecla)

pilas.avisar("Pulsa el teclado para visualizar las teclas pulsadas.")
pilas.ejecutar()
