import pilasengine

pilas = pilasengine.iniciar()

teclas = {
            pilas.simbolos.a: 'izquierda',
            pilas.simbolos.d: 'derecha',
            pilas.simbolos.w: 'arriba',
            pilas.simbolos.s: 'abajo',
            pilas.simbolos.ESPACIO: 'boton',
        }


mono = pilas.actores.Mono(x = 200)
aceituna = pilas.actores.Aceituna()


# La aceituna se mueve con las teclas: W, A, S y D
mi_control = pilas.control.Control(teclas)
aceituna.aprender(pilas.habilidades.MoverseConElTeclado, control=mi_control)

# El mono se mueve con los direccionales.
mono.aprender(pilas.habilidades.MoverseConElTeclado)


pilas.avisar("Para mover la aceituna pulsa las teclas W, A, S o D.")
pilas.ejecutar()
