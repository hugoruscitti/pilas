import pilasengine

pilas = pilasengine.iniciar()
ingreso_de_texto = pilas.interfaz.IngresoDeTexto("Hola")

def mueve_barra(grado):
    ingreso_de_texto.transparencia = grado * 100

b = pilas.interfaz.Deslizador(y=100)
b.conectar(mueve_barra)

pilas.avisar("Mueve el deslizador para cambiar la transparencia")
pilas.ejecutar()
