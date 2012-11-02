import pilas

pilas.iniciar()

def eliminar_aceituna(proyectil, aceituna):
    aceituna.eliminar()

def disparo_simple():
    nave.aprender(pilas.habilidades.Disparar,
                  municion=pilas.actores.proyectil.Bala,
                  offset_disparo=(0, 30),
                  grupo_enemigos=aceitunas,
                  cuando_elimina_enemigo=eliminar_aceituna)

def disparo_doble():
    nave.aprender(pilas.habilidades.Disparar,
                  municion=pilas.municion.BalaDoble,
                  offset_disparo=(0, 30),
                  grupo_enemigos=aceitunas,
                  cuando_elimina_enemigo=eliminar_aceituna)

def disparo_desviado():
    nave.aprender(pilas.habilidades.Disparar,
                  municion=pilas.municion.BalasDoblesDesviadas,
                  offset_disparo=(0, 30),
                  grupo_enemigos=aceitunas,
                  cuando_elimina_enemigo=eliminar_aceituna)

def cuando_selecciona(opcion_seleccionada):
    if (opcion_seleccionada == 'Simple'):
        disparo_simple()
    elif (opcion_seleccionada == 'Doble'):
        disparo_doble()
    else:
        disparo_desviado()

opciones = pilas.interfaz.ListaSeleccion(['Simple', 'Doble', 'Desviados'], cuando_selecciona)
opciones.x = -280
opciones.y = 200

aceitunas = pilas.actores.Aceituna() * 20

nave = pilas.actores.NaveKids(velocidad=4)
disparo_simple()

pilas.ejecutar()
