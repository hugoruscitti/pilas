import pilas

# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

# Dos pinguinos:
pingu1 = pilas.actores.Pingu(x=-100)
pingu2 = pilas.actores.Pingu(x=+100)

# El pinguino de la derecha tendra el punto de control en los pies.
pingu2.centro = ('centro', 'arriba')

pilas.avisar("Dos actores con distintos centros (puntos de control), pulsa F12.")
pilas.ejecutar()
