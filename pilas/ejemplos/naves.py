import pilas
from PySFML import sf
from weakref import ref



pilas.iniciar()
nave = pilas.actores.Nave()


pilas.fondos.Espacio()
pelotas = pilas.atajos.fabricar(pilas.actores.Caja, 30)
pelotas.aprender( pilas.habilidades.PuedeExplotar)
nave.definir_enemigos(pelotas)
pilas.atajos.definir_gravedad(1, 1)




pilas.ejecutar()
