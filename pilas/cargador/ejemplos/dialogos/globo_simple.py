import pilas

def ejecutar():
    globo = pilas.actores.Globo("Hola mundo")
    pilas.avisar("Mostrando un mensaje sencillo")


if __name__ == '__main__':
    pilas.iniciar()
    ejecutar()
    pilas.ejecutar()
