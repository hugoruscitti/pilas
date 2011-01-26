import pilas
pilas.iniciar()


grilla = pilas.imagenes.cargar_grilla("grillas/plataformas_10_10.png", 10, 10)
mapa = pilas.actores.Mapa(grilla)
mapa2 = pilas.actores.Mapa(grilla)
mapa2.x = mapa2.x + mapa.obtener_ancho() 

texto = pilas.actores.Texto("Presiona las flechas para mover el escenario")
texto.color = pilas.colores.negro
texto.magnitud = 20
texto.y = 200



# plataforma 1
for i in range(5):
    mapa.pintar_bloque(4, i + 10, 1)

# plataforma 2
for i in range(5):
    mapa.pintar_bloque(10, i + 14, 1)

# plataforma 3
for i in range(5):
    mapa.pintar_bloque(10, i, 1)

# plataforma 4
for i in range(5):
    mapa2.pintar_bloque(10, i + 14, 1)

# plataforma 5
for i in range(5):
    mapa2.pintar_bloque(4, i + 2, 1)



for i in range(20):
    mapa.pintar_bloque(14, i, 1)
    
for i in range(20):
    mapa2.pintar_bloque(14, i, 1)

def press(evento):        
    if pilas.mundo.control.derecha:
       pilas.mundo.camara.x += 3
            

    if pilas.mundo.control.izquierda:
        pilas.mundo.camara.x -= 3

pilas.eventos.actualizar.conectar(press)
    

pilas.ejecutar()
