import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
pilas.depurador.definir_modos(fisica=True, info=True)

mono = pilas.actores.Mono(200, 0)
mono.aprender(pilas.habilidades.Arrastrable)

mono.aprender(pilas.habilidades.RebotarComoPelota)

mono.figura.sensor = True

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

pilas.ejecutar()
