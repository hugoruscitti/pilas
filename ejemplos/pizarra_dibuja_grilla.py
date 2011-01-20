import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
pizarra = pilas.actores.Pizarra()

grilla = pilas.imagenes.cargar_grilla("pingu.png", 10)
pizarra.pintar_grilla(grilla, 0, 0)

grilla.definir_cuadro(2)
pizarra.pintar_grilla(grilla, 100, 100)

grilla.definir_cuadro(3)
pizarra.pintar_grilla(grilla, 200, 200)

pilas.avisar("Muestra algunos cuadros de animacion sobre una pizarra")
pilas.ejecutar()
