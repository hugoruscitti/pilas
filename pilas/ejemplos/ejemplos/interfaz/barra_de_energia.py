import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()


barra = pilas.actores.Energia(progreso=0, ancho=400, alto=25)

def cuando_cambia_deslizador(valor):
    barra.progreso = valor * 100

deslizador = pilas.interfaz.Deslizador(y=50)
deslizador.conectar(cuando_cambia_deslizador)


pilas.avisar("Usa el deslizador para modificar la barra de energia.")
pilas.ejecutar()
