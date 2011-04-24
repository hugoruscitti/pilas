import pilas

pilas.iniciar()
un = pilas.video.DeCamara()
un.escala = [0.5], 4
un.rotacion = [360], 4

def crear_otro_video():
    un = pilas.video.DeCamara()
    un.escala = 0.2
    rec = pilas.fisica.Rectangulo(200, 200, 128, 96)
    un.imitar(rec)

def hacer_que_rebote():
    rec = pilas.fisica.Rectangulo(0, 0, 320, 240)
    un.imitar(rec)


pilas.mundo.agregar_tarea_una_vez(5, hacer_que_rebote)
pilas.mundo.agregar_tarea_una_vez(7, crear_otro_video)

pilas.ejecutar()
