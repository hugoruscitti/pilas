# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas
pilas.iniciar()

pilas.actores.CursorMano()
pilas.fondos.Pasto()
caja = pilas.actores.Caja() * 10
caja.aprender(pilas.habilidades.Arrastrable)

pelota = pilas.actores.Pelota() * 10
pelota.aprender(pilas.habilidades.Arrastrable)

pilas.avisar("Use el puntero del mouse para arrastrar las figuras.")
pilas.ejecutar()
