import pilas
pilas.iniciar()


deslizador = pilas.actores.Deslizador()
print deslizador.progreso
# retorna 0

# si el usuario mueve el deslizador al centro,
# progreso tendria que ser de 50, y si
# completa todo el valor tendria que ser
# de 100.





pilas.ejecutar()