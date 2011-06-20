# -*- encoding: utf-8 -*-
import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")


pilas.iniciar()
pilas.fondos.Pasto()

# Genera un texto que dice "bienvenido a pilas"
saludo = pilas.actores.Texto(u"¡Bienvenido a pilas!")

# Realiza una animacion
saludo.escala = 0.1
saludo.escala = [1]
saludo.rotacion = [360]

saludo.aprender(pilas.habilidades.MoverseConElTeclado)

pilas.avisar("Ejemplo de texto, pulse las teclas para desplazar el texto.")
pilas.ejecutar()
