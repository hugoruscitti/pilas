import pilas
pilas.iniciar()

s1 = pilas.interfaz.Selector("Me gusta este selector !", x=0, y=90)
entrada = pilas.interfaz.IngresoDeTexto()
entrada.texto = "Texto inicial"

entrada2 = pilas.interfaz.IngresoDeTexto()
entrada2.texto = "Texto inicial"
entrada2.y = -150

pilas.avisar("Escribe en la caja de texto o pulsa el selector.")
pilas.ejecutar()
