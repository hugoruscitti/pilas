import pilas
from PySFML import sf
from weakref import ref



pilas.iniciar()
nave = pilas.actores.Nave()


piedras = pilas.atajos.fabricar(pilas.actores.Piedra, 10, tamano='media')
piedras.aprender(pilas.habilidades.PuedeExplotar)
piedras.aprender(pilas.habilidades.RebotaComoPelota)

nave.definir_enemigos(piedras)

pilas.atajos.definir_gravedad(1, 1)




pilas.ejecutar()
