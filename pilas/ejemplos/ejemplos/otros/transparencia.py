import pilas

pilas.iniciar(usar_motor='qtgl')
ingreso_de_texto = pilas.interfaz.IngresoDeTexto("Ejemplo de transparencia")

def mueve_barra(grado):
    ingreso_de_texto.transparencia = grado * 100

b = pilas.interfaz.Deslizador(y=100)
b.conectar(mueve_barra)
        
pilas.avisar("Mueve el deslizador para cambiar la transparencia")
pilas.ejecutar()
