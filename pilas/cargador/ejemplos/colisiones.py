import pilas

# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()
pilas.avisar("Usa el mouse para mover al mono y ayudarlo a comer.")

# Creamos al mono que se puede arrastrar con el mouse
mono = pilas.actores.Mono()
mono.aprender(pilas.habilidades.Arrastrable)
mono.z = 1


# Creamos las bananas y las colocamos en una lista.
b1 = pilas.actores.Banana()
b1.x = 200

b2 = pilas.actores.Banana()
b2.y = 200

b3 = pilas.actores.Banana()
b3.y = -200

bananas = [b1, b2, b3]

# Creamos una bomba y la colocamos en una lista.
bomba = pilas.actores.Bomba()
bomba.x = -200

bombas = [bomba]


def comer_banana(mono, banana):
    banana.eliminar()
    mono.sonreir()

def hacer_explotar_una_bomba(mono, bomba):
    bomba.explotar()
    mono.gritar()

# Le indicamos a pilas que funcion tiene que ejecutar cuando
# se produzca una colision.
pilas.mundo.colisiones.agregar(mono, bananas, comer_banana)
pilas.mundo.colisiones.agregar(mono, bombas, hacer_explotar_una_bomba)

pilas.ejecutar()
