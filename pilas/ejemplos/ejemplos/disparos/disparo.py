import pilas

pilas.iniciar()

def eliminar_aceituna(proyectil, ovni):
    ovni.eliminar()
    proyectil.eliminar()

def disparo_simple():
    nave.aprender(pilas.habilidades.Disparar,
                  municion=pilas.actores.proyectil.Bala,
                  offset_disparo=(0, 30),
                  grupo_enemigos=ovnis,
                  cuando_elimina_enemigo=eliminar_aceituna)

def disparo_doble():
    nave.aprender(pilas.habilidades.Disparar,
                  municion=pilas.municion.BalaDoble,
                  offset_disparo=(0, 30),
                  grupo_enemigos=ovnis,
                  cuando_elimina_enemigo=eliminar_aceituna)

def disparo_desviado():
    nave.aprender(pilas.habilidades.Disparar,
                  municion=pilas.municion.BalasDoblesDesviadas,
                  parametros_municion={"angulo_desvio" : 15},
                  offset_disparo=(0, 30),
                  grupo_enemigos=ovnis,
                  cuando_elimina_enemigo=eliminar_aceituna)

def cuando_selecciona(opcion_seleccionada):
    if (opcion_seleccionada == 'Simple'):
        disparo_simple()
    elif (opcion_seleccionada == 'Doble'):
        disparo_doble()
    else:
        disparo_desviado()

opciones = pilas.interfaz.ListaSeleccion(['Simple', 'Doble', 'Desviados'], cuando_selecciona)
opciones.x = -200
opciones.y = 200

ovnis = pilas.actores.Ovni(y=100) * 10


nave = pilas.actores.NaveKids(velocidad=4)
disparo_simple()

pilas.fondos.Color(pilas.colores.negro)

pilas.avisar("Selecciona el tipo de disparo.")

pilas.ejecutar()
