# -*- encoding: utf-8 -*-
import pilas

pilas.iniciar()

mi_texto = """Hola mundo
Este es un texto multilinea que se ajusta al area del texto especificada."""

texto = pilas.actores.Texto(mi_texto, y=100, ancho=100)

texto_codigo = pilas.actores.Texto("", magnitud=16)
texto_codigo.x = -150
texto_codigo.y = -150

def cuando_cambia_deslizador(valor):
    texto.ancho = 100 + valor * 200
    texto_codigo.texto = "ejecutando el codigo: texto.ancho = " + str(int(texto.ancho))

deslizador = pilas.interfaz.Deslizador(x=-100, y=-100)
deslizador.conectar(cuando_cambia_deslizador)

pilas.avisar("Utiliza el deslizador para alterar area de texto.")
pilas.ejecutar()