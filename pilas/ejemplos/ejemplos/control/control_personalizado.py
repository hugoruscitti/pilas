# Permite que este ejemplo funcion incluso si no has instalado pilas.
import pilas


pilas.iniciar()

aceituna = pilas.actores.Aceituna()
mono = pilas.actores.Mono(x = 200)

# Que no salgan de la pantalla
aceituna.aprender(pilas.habilidades.SeMantieneEnPantalla, permitir_salida=False)
mono.aprender(pilas.habilidades.SeMantieneEnPantalla, permitir_salida=False)

# Mapeamos unas tecals para mover la aceituna
teclas = {pilas.simbolos.a: 'izquierda',
                      pilas.simbolos.d: 'derecha',
                      pilas.simbolos.w: 'arriba',
                      pilas.simbolos.s: 'abajo',
                      pilas.simbolos.ESPACIO: 'boton'}

# Creamos un control personalizado
mi_control = pilas.control.Control(pilas.escena_actual(), teclas)

# Hacemos que la aceituna mueva con nuestro control personalizado.
aceituna.aprender(pilas.habilidades.MoverseConElTeclado, control=mi_control)

# El mono mueve con las teclas por defecto de los cursores del teclado
mono.aprender(pilas.habilidades.MoverseConElTeclado)

pilas.avisar("Para mover la aceituna pulsa las teclas W, A, S o D.")
pilas.ejecutar()