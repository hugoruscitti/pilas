# -*- encoding: utf-8 -*-
import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
ejes = pilas.actores.Ejes()

pilas.avisar("Mostrando el actor eje. Usa F12 para ver la posicion del mouse.")
pilas.ejecutar()
