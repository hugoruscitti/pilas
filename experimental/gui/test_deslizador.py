import pilas
from pilas.actores import Actor
pilas.iniciar()


    

# mono
mono = pilas.actores.Mono()
mono.x = -94
mono.y = -100
mono.escala = 0.5


# deslizador
deslizador = pilas.interfaz.Deslizador(x = 0, y = 0)

deslizador.set_x(-94)
deslizador.set_y(50)
deslizador.set_transparencia(0)

# texto
texto = pilas.actores.Texto('0')
texto.fuente = 'sans'
texto.magnitud = 20
texto.color = pilas.colores.negro


def mono_movimiento(valor):
    # (valor) toma de 0 a 1
    # (valor * 100) de 0 a 100
    # ...

    mono.x = ((valor)* 200) - 94
    texto.definir_texto(str(int(valor * 100)) + ' %')

deslizador.conectar(mono_movimiento)

pilas.fondos.Blanco()

pilas.ejecutar()
