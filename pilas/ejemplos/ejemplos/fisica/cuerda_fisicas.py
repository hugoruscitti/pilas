import pilas

pilas.iniciar()

pilas.fondos.Tarde()

elementos_de_la_cuerda = []
ancho_elemento_cuerda = 25
alto_elemento_cuerda = 5
aceitunas = pilas.actores.Aceituna() * 15
aceitunas.aprender(pilas.habilidades.Arrastrable)

rectangulo_fijo = pilas.fisica.Rectangulo(0,200,50,10,dinamica=False)

for i in range(0,15):
	elementos_de_la_cuerda.append(pilas.fisica.Rectangulo(200,200,ancho_elemento_cuerda,alto_elemento_cuerda))
	aceitunas[i].imitar(elementos_de_la_cuerda[i])

for i in range(0,14):
	pilas.fisica.ConstanteDeGiro(elementos_de_la_cuerda[i],elementos_de_la_cuerda[i+1],(ancho_elemento_cuerda/2,0),(-ancho_elemento_cuerda/2,0))

pilas.fisica.ConstanteDeGiro(rectangulo_fijo,elementos_de_la_cuerda[0],(0,0),(-ancho_elemento_cuerda/2,0))

pilas.ejecutar()