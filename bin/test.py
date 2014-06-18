import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
pilas.depurador.definir_modos(fisica=False, info=True)


e = pilas.actores.Emisor(0, 0)

e.constante = True

e.dx_min = -10
e.dx_max =  10

e.dy_min = -10
e.dy_max =  10


pc = pilas.actores.Controlador()
pc.x = 230
pc.y = 200

pc.agregar(e, 'dy_min', -20, 0)
pc.agregar(e, 'dy_max', 0, 20)
pc.agregar_espacio()

pc.agregar(e, 'dx_min', -20, 0)
pc.agregar(e, 'dx_max', 0, 20)
pc.agregar_espacio()

pc.agregar(e, 'escala_min', 0.1, 4)
pc.agregar(e, 'escala_max', 0.1, 4)
pc.agregar_espacio()

pc.agregar(e, 'rotacion_min', 0, 360)
pc.agregar(e, 'rotacion_max', 0, 360)
pc.agregar_espacio()



#dh = pilas.actores.DeslizadorHorizontal(200, 0, min=-50, max=0, etiqueta='dx_min')

#def cuando_cambia_dx_min(valor):
#    e.dx_min = valor

#dh.conectar(cuando_cambia_dx_min)


#mono = pilas.actores.Mono()
#mono.figura_de_colision = pilas.fisica.Rectangulo(0, 0, 100, 100)

#mono.aprender( pilas.habilidades.MoverseConElTeclado)

#cajas = pilas.actores.Caja(y=200) * 10


#def cuando_colisionan(mono, caja):
#    caja.eliminar()

#pilas.colisiones.agregar(mono, cajas, cuando_colisionan)


"""
mono = pilas.actores.Mono(200, 0)
mono.aprender(pilas.habilidades.Arrastrable)

#mono.aprender(pilas.habilidades.RebotarComoPelota)
#mono.figura.sensor = True

caja = pilas.actores.Banana() * 60
caja.aprender(pilas.habilidades.RebotarComoPelota)


def cuando_colisionan(mo, ca):
    ca.eliminar()
    mo.sonreir()

pilas.colisiones.agregar(mono, caja, cuando_colisionan)

#sonido = pilas.sonidos.cargar('/Users/hugoruscitti/barreta.wav')

def on_click(evento):
    #sonido.reproducir()
    actores = pilas.obtener_actores_en(evento.x, evento.y)
    print actores

    for actor in actores:
        mono.gritar()

#pilas.eventos.click_de_mouse.conectar(on_click)

"""
pilas.ejecutar()
