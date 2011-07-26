import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
boton = pilas.interfaz.Boton("Hola mundo")

pilas.avisar("Creando un boton con texto.")
pilas.ejecutar()
