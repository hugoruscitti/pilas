import pilas
pilas.iniciar()

# ejemplo de uso boton personalizado
# al iniciar no se visualiza nada pero al cliquear al centro
# aparece de pronto un circulo, has la prueba !


# pilas.actores.Boton(x, y, "imagen normal.png, imagen press.png, imagen over.png")

boton = pilas.actores.Boton(0, 0,'ficha_vacia.png', 'ficha1.png', 'ficha1.png')

# al cargar previamente nuevas imagenes
# cuando llamemos sus metodos como:
# boton.pintar_presionado() se cambiara por la imagen
# cargada en la parte de imagen_press.png

# como cargamos ficha_vacia.png en la seccion de imagen normal
# la cara principal del boton seria invisible

class contador:
    presionado_una_vez = True

def presionar():
    if (contador.presionado_una_vez == True):
        # pintamos boton seccion imagen_press
        boton.pintar_presionado()
        boton.escala = 0.8
        boton.escala = pilas.interpolar([1], duracion=0.1)
        contador.presionado_una_vez = False
        pilas.avisar("Epa!!")
        

#conectamos funcion a evento presionar boton
boton.conectar_presionado(presionar) 

pilas.avisar("Pulsa exactamente en el centro de la ventana.")

pilas.ejecutar()


# si no queremos un boton personalizado simplemente

# escribimos boton = pilas.actores.Boton()

# y le conectamos sus metodos:

# boton.conectar_presionado(boton.pintar_presionado)
# boton.conectar_normal(boton.pintar_normal)

# ...

# o podemos conectar de la forma

# def pintar_cuando_este_sobre():
#     boton.pintar_sobre()

# boton.conectar_presionado(pintar_cuando_este_sobre())















