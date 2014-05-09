import sys
sys.path.append('.')
import pilasengine

pilas = pilasengine.iniciar()
mono = pilas.actores.Mono()
mono.x = [100], 10
aceituna = pilas.actores.Aceituna()

aceituna_grande = pilas.actores.Aceituna()
aceituna_grande.x = 100
aceituna_grande.escala = 2
aceituna_grande.fijo = True

pilas.escena_actual().camara.x = [200], 5
pilas.escena_actual().camara.aumento = [2], 5
pilas.escena_actual().camara.rotacion = [180], 5
aceituna.agregar(mono)
aceituna.rotacion = [180], 10


pilas.ejecutar()
