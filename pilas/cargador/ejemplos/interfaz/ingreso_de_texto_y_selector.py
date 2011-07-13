import pilas
pilas.iniciar()


s1 = pilas.interfaz.Selector("Me gusta este selector !", x=0, y=90) 
entrada = pilas.interfaz.IngresoDeTexto()
entrada.texto = "Texto inicial"

pilas.avisar("Escribe en la caja de texto o pulsa el selector.")
pilas.ejecutar()
