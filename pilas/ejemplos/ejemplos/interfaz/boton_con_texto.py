import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
boton = pilas.interfaz.Boton("Hola mundo")

def cuando_hacen_click():
    boton.decir("Has pulsado el boton!")

boton.conectar(cuando_hacen_click)
pilas.avisar("Creando un boton con texto.")
pilas.ejecutar()
