import pilas

pilas.iniciar()

pilas.fondos.Tarde()

rectangulos = []
aceitunas = pilas.actores.Aceituna() * 15
aceitunas.aprender(pilas.habilidades.Arrastrable)

rectangulo_fijo = pilas.fisica.Rectangulo(0,200,50,10,dinamica=False)

for i in range(0,15):
	rectangulos.append(pilas.fisica.Rectangulo(200,200-i,25,5))
	aceitunas[i].imitar(rectangulos[i])


for i in range(0,14):
	pilas.fisica.ConstanteDeGiro(rectangulos[i],rectangulos[i+1])

pilas.fisica.ConstanteDeGiro(rectangulo_fijo,rectangulos[0])

pilas.ejecutar()