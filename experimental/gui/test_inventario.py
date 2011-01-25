import pilas
from pilas.actores import Boton
from pilas.actores import Actor
pilas.iniciar()

class variables:
    usando_herramienta = False
    estado = True
    sobre = False


class cursor(Actor):
    def __init__(self, x = 0, y = 0): 
        self.imagen_cursor1 = pilas.imagenes.cargar("gui/cursor_1.png")
        self.imagen_cursor2 = pilas.imagenes.cargar("gui/cursor_2.png")
        self.imagen_cursor3 = pilas.imagenes.cargar("gui/cursor_3.png")
        self.imagen_cursor4 = pilas.imagenes.cargar("gui/cursor_4.png")
        
        Actor.__init__(self, self.imagen_cursor1)
        self.x = x
        self.y = y

        pilas.eventos.mueve_mouse.conectar(self.mov_mouse)
        self.aprender(pilas.habilidades.SeguirAlMouse)
        self.centro = ("izquierda", "arriba")
        self.z = -100
        
        pilas.motor.ocultar_puntero_del_mouse()
        
    def mov_mouse(self, evento):
        if variables.sobre == False:
            if variables.usando_herramienta == False:
                self.pintar_cursor(1)
            else:
                self.pintar_cursor(3)
        else:
            if variables.usando_herramienta == False:
                self.pintar_cursor(2)
            else:
                self.pintar_cursor(4)

        variables.sobre = False
        
    def pintar_cursor(self, n):

        def pintar_c1():
            self.definir_imagen(self.imagen_cursor1)

        def pintar_c2():
            self.definir_imagen(self.imagen_cursor2)

        def pintar_c3():
            self.definir_imagen(self.imagen_cursor3)

        def pintar_c4():
            self.definir_imagen(self.imagen_cursor4)
            
        switch = {1:pintar_c1,
                  2:pintar_c2,
                  3:pintar_c3,
                  4:pintar_c4}

        switch[n]()




class elemento(Boton):
    def __init__(self, x = 0, y = 0, ruta_imagen = "null", ruta_i = "null", funcion_arg = "null"):
        Boton.__init__(self, ruta_normal = ruta_imagen,ruta_press = ruta_i, x = x, y = y)

        if funcion_arg == "null":
            self.funcion = self.funcion_vacia
        else:
            self.funcion = funcion_arg

        self.primera_vez_presionado = False
        self.conectar_sobre(self.sobre_elemento)
             

    def funcion_vacia(self):
        pass

    def sobre_elemento(self):
        variables.sobre = True
          


class Inventory(Boton):

    def __init__(self, x=0, y=0):
        Boton.__init__(self,ruta_normal = "gui/flecha.png",x=x, y=y)
        self.escala = 0.8
        self.conectar_presionado(self.click_caja)

        self.elements = []
        self.n_elements = 0
        
        self.inventory = []
        self.n_inventory = 0

        self.open_inventory = False
        self.herramienta_actual = -1
        self.estado = True

        self.n_press = 0 

    def al_presionar_elements_in_inventory(self, i):
        if variables.estado == True:
        
            if self.herramienta_actual == -1:
                self.herramienta_actual = i  
                self.inventory[self.herramienta_actual].pintar_presionado()
                self.inventory[self.herramienta_actual].funcion()
                variables.usando_herramienta = True

            elif self.herramienta_actual == i:
                self.inventory[i].pintar_normal()
                variables.usando_herramienta = False
                self.herramienta_actual = -1
                

    def activar_estado(self):
        self.estado = True


    def click_caja(self):
        def activar_estado_var():
            variables.estado = True
        # salida
        if self.open_inventory == False:
            if self.estado == True:                
                variables.estado = False
                for i in range(self.n_inventory):
                    pos_x = ((self.x + 40) + (self.inventory[0].obtener_ancho() + 20) * i)
                    self.inventory[i].x = pilas.interpolar([pos_x], duracion = 0.5)
                    self.inventory[i].transparencia = 0
                    pilas.mundo.agregar_tarea(0.5, self.activar_estado)
                    pilas.mundo.agregar_tarea(0.5, activar_estado_var)
                    self.estado = False                    
                self.open_inventory = True

        # entrada
        else:
            if self.estado == True:
                for i in range(self.n_inventory):                    
                    variables.estado = False
                    self.inventory[i].x = pilas.interpolar([self.x], duracion = 0.5)
                    pilas.mundo.agregar_tarea(0.5, self.activar_estado)
                    self.inventory[i].transparencia = pilas.interpolar([100], duracion = 0.5)
                    self.estado = False
                self.open_inventory = False


        self.escala = pilas.interpolar([1.5, 0.8], duracion = 0.2)
            
    
    def presionar_elemento(self, n):

        if self.elements[n].primera_vez_presionado == False:
            self.open_inventory = False
            self.elements[n].primera_vez_presionado = True

            self.inventory.append(self.elements[n])

            self.n_inventory += 1
            
            self.click_on_elements()

        
    def click_on_elements(self):
        for i in range(self.n_inventory):
           self.inventory[i].y = pilas.interpolar([self.y], duracion = 0.5)
           self.inventory[i].escala = [0.5]
           self.inventory[i].x = pilas.interpolar([self.x], duracion = 0.5)
           self.inventory[i].transparencia = pilas.interpolar([100], duracion = 0.5)
           pilas.mundo.agregar_tarea(0.5, self.activar_estado)
           self.inventory[i].desconectar_presionado_todo()
           self.inventory[i].desconectar_normal_todo()
           self.inventory[i].desconectar_sobre_todo()
           self.inventory[i].conectar_presionado(self.al_presionar_elements_in_inventory, i)
           variables.estado = False

    
    def agregar_elemento(self, ruta, ruta_i, x = 0, y = 0, funcion = "null"):

        
        e = elemento(ruta_imagen = ruta, ruta_i = ruta_i, x = x, y = y, funcion_arg = funcion)
        e.conectar_presionado(self.presionar_elemento, self.n_elements)
        self.elements.append(e)
        
        self.n_elements += 1
        
    
        
        






mouse = cursor()

herramientas = Inventory(- 280, - 210)

def imprimir_mensaje_1():
    print "herramienta en uso: banana"

def imprimir_mensaje_2():
    print "herramienta en uso: mono"

def imprimir_mensaje_3():
    print "herramienta en uso: bomba"

def imprimir_mensaje_4():
    print "herramienta en uso: llave"
    
herramientas.agregar_elemento("gui/banana.png","gui/banana_i.png", 100, funcion = imprimir_mensaje_1)
herramientas.agregar_elemento("gui/mono.png","gui/mono_i.png", -50, funcion = imprimir_mensaje_2)
herramientas.agregar_elemento("gui/bomba.png","gui/bomba_i.png", -200, funcion = imprimir_mensaje_3)
herramientas.agregar_elemento("gui/llave.png","gui/llave_i.png", 200, funcion = imprimir_mensaje_4)



pilas.fondos.Blanco()

pilas.ejecutar()
