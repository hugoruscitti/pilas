import pilas
# Permite que este ejemplo funcion incluso si no has instalado pilas.
import sys
sys.path.insert(0, "..")

pilas.iniciar()

class DibujoDeLineas:

    def __init__(self):
        self.mouse_x = 0
        self.mouse_y = 0
        self.boton_pulsado = False
        self.pizarra = pilas.actores.Pizarra()
        pilas.escena_actual().click_de_mouse.conectar(self.cuando_pulsa_el_boton)
        pilas.escena_actual().mueve_mouse.conectar(self.cuando_mueve_el_mouse)
        pilas.escena_actual().termina_click.conectar(self.cuando_deja_de_pulsar_el_boton)

    def cuando_pulsa_el_boton(self, evento):
        self.boton_pulsado = True

    def cuando_deja_de_pulsar_el_boton(self, evento):
        self.boton_pulsado = False

    def cuando_mueve_el_mouse(self, evento):
        if self.boton_pulsado:
            self.pizarra.linea(self.mouse_x, self.mouse_y, evento.x, evento.y, grosor=2)

        self.mouse_x = evento.x
        self.mouse_y = evento.y
    
a = DibujoDeLineas()

pilas.avisar("Use el mouse para dibujar.")
pilas.ejecutar()
