import pilas

pilas.iniciar()

mono = pilas.actores.Mono()

dialogo = pilas.actores.Dialogo()
dialogo.decir(mono, "Hola, podrias hacer click?")
dialogo.decir(mono, "Perfecto!!, gracias...")
dialogo.decir(mono, "Haciendo clicks avanzan los dialogos.")
dialogo.decir(mono, "eh ...")
dialogo.decir(mono, "m ...")
dialogo.decir(mono, "no se me ocurre que decir...")

dialogo.iniciar()


pilas.ejecutar()
