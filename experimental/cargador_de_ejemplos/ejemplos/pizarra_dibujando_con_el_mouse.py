import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

pizarra = pilas.actores.Pizarra()

def cuando_pulsa_el_boton(evento):
    pizarra.bajar_lapiz()

def cuando_deja_de_pulsar_el_boton(evento):
    pizarra.levantar_lapiz()

def cuando_mueve_el_mouse(evento):
    pizarra.mover_lapiz(evento.x, evento.y)
    
pizarra.levantar_lapiz()

pilas.eventos.click_de_mouse.conectar(cuando_pulsa_el_boton)
pilas.eventos.mueve_mouse.conectar(cuando_mueve_el_mouse)
pilas.eventos.termina_click.conectar(cuando_deja_de_pulsar_el_boton)

pilas.avisar("Use el mouse para dibujar.")
pilas.ejecutar()
