# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")
import pilas
pilas.iniciar()


def eliminar_caja(caja, pelota):
    caja.eliminar()
    
pilas.actores.CursorMano()
pilas.fondos.Pasto()
caja = pilas.actores.Caja(x=200)
caja.radio_de_colision = 1
caja.aprender(pilas.habilidades.Arrastrable)
caja.aprender(pilas.habilidades.PuedeExplotar)


pelota = pilas.actores.Pelota(x=-200)
pelota.radio_de_colision = 1
pelota.aprender(pilas.habilidades.Arrastrable)

pilas.mundo.colisiones.agregar(caja, pelota, eliminar_caja)

pilas.ejecutar()
