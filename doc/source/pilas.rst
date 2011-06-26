Resumen API de pilas====================


pilas.pilasversion
-----------------



pilas.fisica
-----------




class **Fisica** (object)

- **__init__(self, area, gravedad=** (0, -90))
- **actualizar** (self)
- **_procesar_figuras_a_eliminar** (self)
- **dibujar_figuras_sobre_lienzo** (self, motor, lienzo)
- **crear_cuerpo** (self, definicion_de_cuerpo)
- **crear_suelo(self, ** (ancho, alto), restitucion=1)
- **crear_techo(self, ** (ancho, alto), restitucion=1)
- **crear_paredes(self, ** (ancho, alto), restitucion=1)
- **eliminar_suelo** (self)
- **eliminar_paredes** (self)
- **eliminar_figura** (self, figura)
- **obtener_distancia_al_suelo** (self, x, y, dy)
- **obtener_cuerpos_en** (self, x, y)
- **definir_gravedad** (self, x, y)


class **Figura** (object)

- **obtener_x** (self)
- **definir_x** (self, x)
- **obtener_y** (self)
- **definir_y** (self, y)
- **obtener_rotacion** (self)
- **definir_rotacion** (self, angulo)
- **impulsar** (self, dx, dy)
- **obtener_velocidad_lineal** (self)
- **definir_velocidad_lineal** (self, dx, dy)
- **eliminar** (self)


class **Circulo** (Figura)



class **Rectangulo** (Figura)

- **__init__** (self, figura_1, figura_2, fisica=None)
- **definir_gravedad** (x=0, y=-90)

pilas.pytweener
--------------


- **__init__** (self, duration = 0.5, tween = None)
- **hasTweens** (self)
- **addTweenNoArgs** (self, obj, function, initial_value, value, **kwargs)
- **addTween** (self, obj, **kwargs)
- **removeTween** (self, tweenObj)
- **getTweensAffectingObject** (self, obj)
- **removeTweeningFrom** (self, obj)
- **finish** (self)
- **update** (self, timeSinceLastFrame)


class **Tween** (object)

- **__init__** (self, obj, tduration, tweenType, completeFunction, updateFunction, delay, **kwargs)
- **decodeArguments** (self)
- **pause** ( self, numSeconds=-1 )
- **resume** ( self )
- **update** (self, ptime)
- **getTweenable** (self, name)
- **Remove** (self)
- **__init__** (self, start, change)
- **easeIn** (t, b, c, d, s = 1.70158)
- **easeOut ** (t, b, c, d, s = 1.70158)
- **easeInOut ** (t, b, c, d, s = 1.70158)
- **easeOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeOut ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeOut ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d, a = 0, p = 0)
- **easeOut ** (t, b, c, d, a = 0, p = 0)
- **easeInOut ** (t, b, c, d, a = 0, p = 0)
- **easeIn** (t, b, c, d)
- **easeOut** (t, b, c, d)
- **easeInOut** (t, b, c, d)
- **easeNone** (t, b, c, d)
- **easeIn** (t, b, c, d)
- **easeOut** (t, b, c, d)
- **easeInOut** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeOut ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeOut ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeOut ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn ** (t, b, c, d)
- **easeOut ** (t, b, c, d)
- **easeInOut ** (t, b, c, d)
- **easeIn** (t, b, c, d)
- **easeOut** (t, b, c, d)
- **easeInOut** (t, b, c, d)
- **__init__** (self)
- **update** (self)
- **setRotation** (self, rot)
- **getRotation** (self)
- **complete** (self)

pilas.utils
----------


- **cargar_autocompletado** ()
- **hacer_flotante_la_ventana** ()
- **es_interpolacion** (an_object)
- **obtener_ruta_al_recurso** (ruta)
- **esta_en_sesion_interactiva** ()
- **distancia** (a, b)
- **distancia_entre_dos_puntos((x1, y1), ** (x2, y2))
- **distancia_entre_dos_actores** (a, b)
- **colisionan** (a, b)
- **crear_juego** ()
- **interpolable** (f)
- **inner** (*args, **kwargs)
- **hacer_coordenada_mundo** (x, y)
- **hacer_coordenada_pantalla_absoluta** (x, y)
- **listar_actores_en_consola** ()
- **obtener_angulo_entre** (punto_a, punto_b)
- **convertir_de_posicion_relativa_a_fisica** (x, y)
- **convertir_de_posicion_fisica_relativa** (x, y)
- **interpolar** (valor_o_valores, duracion=1, demora=0, tipo='lineal')
- **obtener_area** ()
- **obtener_bordes** ()
- **obtener_area_de_texto** (texto)

pilas.imagenes
-------------


- **cargar** (ruta)
- **cargar_grilla** (ruta, columnas=1, filas=1)
- **cargar_lienzo** ()
- **cargar_superficie** (ancho, alto)

pilas.comportamientos
--------------------


- **iniciar** (self, receptor)
- **actualizar** (self)
- **terminar** (self)


class **Girar** (Comportamiento)

- **__init__** (self, delta, velocidad)
- **iniciar** (self, receptor)
- **actualizar** (self)


class **Avanzar** (Comportamiento)

- **__init__** (self, pasos, velocidad=5)
- **iniciar** (self, receptor)
- **actualizar** (self)

pilas.interpolaciones
--------------------




class **Lineal** (Interpolacion)

- **__init__** (self, values, duration, delay)
- **__neg__** (self)
- **apply** (self, target, function)

pilas.estudiante
---------------


- **__init__** (self)
- **aprender** (self, classname, *k, **w)
- **hacer_luego** (self, comportamiento, repetir_por_siempre=False)
- **hacer** (self, comportamiento)
- **eliminar_habilidades** (self)
- **eliminar_comportamientos** (self)
- **actualizar_habilidades** (self)
- **actualizar_comportamientos** (self)
- **_adoptar_el_siguiente_comportamiento** (self)

pilas.depurador
--------------


- **__init__** (self, lienzo, fps)
- **cuando_mueve_el_mouse** (self, evento)
- **comienza_dibujado** (self, motor)
- **dibuja_al_actor** (self, motor, actor)
- **termina_dibujado** (self, motor)
- **cuando_pulsa_tecla** (self, evento)
- **_alternar_modo** (self, clase_del_modo)
- **_activar_modo** (self, clase_del_modo)
- **_desactivar_modo** (self, clase_del_modo)
- **_mostrar_nombres_de_modos** (self, motor)
- **_mostrar_posicion_del_mouse** (self, motor)
- **_mostrar_cuadros_por_segundo** (self, motor)
- **__init__** (self, depurador)
- **comienza_dibujado** (self, motor, lienzo)
- **dibuja_al_actor** (self, motor, lienzo, actor)
- **termina_dibujado** (self, motor, lienzo)
- **orden_de_tecla** (self)


class **ModoPuntosDeControl** (ModoDepurador)

- **dibuja_al_actor** (self, motor, lienzo, actor)


class **ModoRadiosDeColision** (ModoDepurador)

- **dibuja_al_actor** (self, motor, lienzo, actor)


class **ModoArea** (ModoDepurador)

- **dibuja_al_actor** (self, motor, lienzo, actor)


class **ModoPosicion** (ModoDepurador)

- **__init__** (self, depurador)
- **dibuja_al_actor** (self, motor, lienzo, actor)


class **ModoFisica** (ModoDepurador)

- **termina_dibujado** (self, motor, lienzo)

pilas.grupo
----------




class **Grupo** (list)

- **__getattr__** (self, attr)
- **map_a_todos** (*k, **kw)
- **__setattr__** (self, atributo, valor)
- **desordenar** (self)
- **limpiar** (self)

pilas.sonidos
------------


- **cargar** (ruta)

pilas.colores
------------


- **__init__** (self, r, g, b, a=255)
- **obtener** (self)
- **__str__** (self)
- **obtener_componentes** (self)

pilas.colisiones
---------------


- **__init__** (self)
- **verificar_colisiones** (self)
- **_verificar_colisiones_en_tupla** (self, tupla)
- **agregar** (self, grupo_a, grupo_b, funcion_a_llamar)
- **obtener_colisiones** (self, actor, grupo_de_actores)

pilas.fondos
-----------




class **Fondo** (pilas.actores.Actor)

- **__init__** (self, imagen)


class **Volley** (Fondo)

- **__init__** (self)


class **Pasto** (Fondo)

- **__init__** (self)


class **Selva** (Fondo)

- **__init__** (self)


class **Tarde** (Fondo)

- **__init__** (self)


class **Espacio** (Fondo)

- **__init__** (self)


class **Noche** (Fondo)

- **__init__** (self)


class **Color** (Fondo)

- **__init__** (self, color)
- **dibujar** (self, motor)

pilas.simbolos
-------------



pilas.control
------------


- **__init__** (self)
- **cuando_pulsa_una_tecla** (self, evento)
- **cuando_suelta_una_tecla** (self, evento)
- **procesar_cambio_de_estado_en_la_tecla** (self, codigo, estado)
- **__str__** (self)

pilas.lienzo
-----------



pilas.tareas
-----------


- **__init__** (self)
- **actualizar** (self, dt)
- **_agregar** (self, proxima_ejecucion, periodo, function, params, invocar_una_vez=False)
- **una_vez** (self, time_out, function, params=[])
- **siempre** (self, time_out, function, params=[])
- **condicional** (self, time_out, function, params=[])

pilas.red
--------


- **iniciar_servidor** ()
- **setup** (self)
- **handle** (self)
- **finish** (self)

pilas.atajos
-----------


- **crear_grupo** (*k)
- **definir_gravedad** (x=0, y=-900)

pilas.ventana
------------


- **iniciar** (ancho, alto, titulo)

pilas.eventos
------------


- **imprimir_todos** ()

pilas.habilidades
----------------


- **__init__** (self, receptor)
- **actualizar** (self)
- **eliminar** (self)


class **RebotaComoPelota** (Habilidad)

- **__init__** (self, receptor)
- **eliminar** (self)


class **RebotaComoCaja** (Habilidad)

- **__init__** (self, receptor)
- **eliminar** (self)


class **ColisionableComoPelota** (RebotaComoPelota)

- **__init__** (self, receptor)
- **actualizar** (self)
- **eliminar** (self)


class **SeguirAlMouse** (Habilidad)

- **__init__** (self, receptor)
- **mover** (self, evento)


class **AumentarConRueda** (Habilidad)

- **__init__** (self, receptor)
- **cambiar_de_escala** (self, evento)


class **SeguirClicks** (Habilidad)

- **__init__** (self, receptor)
- **moverse_a_este_punto** (self, evento)


class **Arrastrable** (Habilidad)

- **__init__** (self, receptor)
- **try_to_drag** (self, evento)
- **drag** (self, evento)
- **drag_end** (self, evento)
- **comienza_a_arrastrar** (self)
- **termina_de_arrastrar** (self)


class **MoverseConElTeclado** (Habilidad)

- **__init__** (self, receptor)
- **on_key_press** (self, evento)


class **PuedeExplotar** (Habilidad)

- **__init__** (self, receptor)
- **eliminar_y_explotar** (self)


class **SeMantieneEnPantalla** (Habilidad)

- **actualizar** (self)


class **PisaPlataformas** (Habilidad)

- **__init__** (self, receptor)
- **actualizar** (self)
- **eliminar** (self)


class **Imitar** (Habilidad)

- **__init__** (self, receptor, objeto_a_imitar)
- **actualizar** (self)
- **eliminar** (self)

pilas.escenas
------------


- **__init__** (self)
- **iniciar** (self)
- **terminar** (self)


class **Normal** (Escena)

- **__init__** (self, color_de_fondo=None)

pilas.mundo
----------


- **actualizar_simuladores** (self, evento)
- **terminar** (self)
- **ejecutar_bucle_principal** (self, ignorar_errores=False)
- **definir_escena** (self, escena_nueva)
- **agregar_tarea_una_vez** (self, time_out, function, *params)
- **agregar_tarea_siempre** (self, time_out, function, *params)
- **agregar_tarea** (self, time_out, funcion, *parametros)
- **_realizar_actualizacion_logica** (self, ignorar_errores)
- **cerrar_ventana** (self)
- **definir_escena** (self, escena_nueva)
- **alternar_pausa** (self)
- **actualizar_actores** (self)
- **dibujar_actores** (self)
- **emitir_evento_actualizar** (self)
- **analizar_colisiones** (self)

pilas.xmlreader
--------------


- **__init__** (self, domElement)
- **getData** (self)
- **getAttributeValue** (self, name)
- **getChild** (self, tag)
- **getChildren** (self, tag)
- **makeRootNode** (xmlFileName)

pilas.camara
-----------




class **Camara** (object)

- **__init__** (self, app)
- **_set_x** (self, x)
- **_get_x** (self)
- **_set_y** (self, y)
- **_get_y** (self)

pilas.baseactor
--------------


- **__init__** (self)
- **aprender** (self, classname, *k, **w)
- **hacer_luego** (self, comportamiento, repetir_por_siempre=False)
- **hacer** (self, comportamiento)
- **eliminar_habilidades** (self)
- **eliminar_comportamientos** (self)
- **actualizar_habilidades** (self)
- **actualizar_comportamientos** (self)
- **_adoptar_el_siguiente_comportamiento** (self)
- **__init__** (self, x=0, y=0)
- **_definir_centro_del_actor** (self)
- **get_x** (self)
- **set_x** (self, x)
- **get_z** (self)
- **set_z** (self, z)
- **set_y** (self, y)
- **get_y** (self)
- **set_scale** (self, s)
- **get_scale** (self)
- **get_rotation** (self)
- **set_rotation** (self, x)
- **get_espejado** (self)
- **set_espejado** (self, nuevo_valor)
- **set_transparencia** (self, nuevo_valor)
- **get_transparencia** (self)
- **get_imagen** (self)
- **set_imagen** (self, imagen)
- **eliminar** (self)
- **actualizar** (self)
- **__cmp__** (self, otro_actor)
- **get_izquierda** (self)
- **set_izquierda** (self, x)
- **get_abajo** (self)
- **set_abajo** (self, y)
- **get_derecha** (self)
- **set_derecha** (self, x)
- **get_arriba** (self)
- **set_arriba** (self, y)
- **colisiona_con_un_punto** (self, x, y)

pilas.fps
--------


- **__init__** (self, fps, usar_modo_economico)
- **actualizar** (self)
- **obtener_cuadros_por_segundo** (self)
- **__init__** (self, fps, usar_modo_economico)
- **actualizar** (self)
- **obtener_cuadros_por_segundo** (self)

pilas.video.video
----------------




class **MissingOpencv** (Exception)

- **__init__** (self)
- **__str__** (self)
- **error** (biblioteca, web)
- **no_opencv** ()


class **DeCamara** (pilas.actores.Actor)

- **__init__** (self, ancho=640, alto=480)
- **actualizar_video** (self)


class **VideoDeArchivo** (object)

- **__init__** (self, ruta)
- **obtener_imagen** (self)


class **DePelicula** (pilas.actores.Actor)

- **__init__** (self, path, ancho=640, alto=480)
- **actualizar_video** (self)

pilas.video.webcam
-----------------




class **__camara_buffer** (object)

- **__init__** (self)
- **_obtener_imagen_de_camara** (self)
- **obtener_imagen** (self, numero_de_cuadro=0)

pilas.ejemplos.fisica
--------------------




class **ColisionesFisicas** (pilas.escenas.Normal)

- **__init__** (self)

pilas.ejemplos.piezas
--------------------




class **Piezas** (pilas.escenas.Normal)

- **__init__** (self, ruta_a_la_imagen="ejemplos/data/piezas.png", filas=4, columnas=4, al_terminar=None)
- **crear_piezas** (self, grilla, filas, columnas)
- **al_hacer_click** (self, evento)
- **al_soltar_el_click** (self, evento)
- **al_mover_el_mouse** (self, evento)
- **conectar** (self, pieza_a, pieza_b)


class **Pieza** (pilas.actores.Animado)

- **__init__** (self, escena_padre, grilla, cuadro, filas, columnas)
- **asignar_numero_de_piezas_laterales** (self, cuadro, columnas)
- **soltar_todas_las_piezas_del_grupo** (self)
- **soltar** (self)
- **se_pueden_conectar_los_bordes** (self, borde1, borde2)
- **intentar_conectarse_a** (self, otra)
- **conectar_con** (self, otra_pieza)
- **__repr__** (self)
- **set_x** (self, x)
- **set_y** (self, y)
- **get_x** (self)
- **get_y** (self)
- **mostrar_arriba_todas_las_piezas** (self)
- **mostrar_abajo_todas_las_piezas** (self)

pilas.ejemplos.colisiones
------------------------


- **comer** (mono, banana)


class **Colisiones** (pilas.escenas.Normal)

- **__init__** (self)
- **crear_personajes** (self)

pilas.ejemplos.listaseleccion
----------------------------


- **cuando_selecciona** (opcion)

pilas.cargador.syntax
--------------------


- **format** (color, style='')


class **PythonHighlighter ** (QSyntaxHighlighter)

- **__init__** (self, document)
- **highlightBlock** (self, text)
- **match_multiline** (self, text, delimiter, in_state, style)

pilas.cargador.ui
----------------




class **Ui_MainWindow** (object)

- **setupUi** (self, MainWindow)
- **retranslateUi** (self, MainWindow)

pilas.cargador.cargador
----------------------


- **__init__** (self)
- **centrar_ventana** (self)
- **_definir_estado_habilitado** (self, esta_habilitado)
- **_cargar_lista_de_ejemplos** (self)
- **_iniciar_interfaz** (self)
- **cuando_pulsa_boton_ejecutar** (self)
- **cuando_quiere_cerrar** (self)
- **cuando_pulsa_boton_fuente** (self)
- **cuando_pulsa_boton_guardar** (self)
- **cuando_cambia_seleccion** (self)
- **_mostrar_imagen_del_ejemplo** (self, nombre)
- **_mostrar_image_inicial** (self)
- **_mostrar_codigo_del_ejemplo** (self, nombre)
- **_mostrar_codigo_presentacion_inicial** (self)
- **_obtener_codigo_del_ejemplo** (self, nombre)
- **_obtener_item_actual** (self)
- **_ejecutar_ejemplo** (self, ejemplo)
- **_cuando_termina_la_ejecucion_del_ejemplo** (self, estado)
- **main** ()

pilas.cargador.ejemplos.seguir_clicks
------------------------------------



pilas.cargador.ejemplos.video
----------------------------


- **crear_otro_video** ()
- **hacer_que_rebote** ()

pilas.cargador.ejemplos.fondo
----------------------------



pilas.cargador.ejemplos.explosion
--------------------------------


- **crear_explosion** (evento)

pilas.cargador.ejemplos.actores_simples
--------------------------------------



pilas.cargador.ejemplos.punto_de_control
---------------------------------------



pilas.cargador.ejemplos.pizarra_avanzado_cairo
---------------------------------------------



pilas.cargador.ejemplos.pizarra
------------------------------


- **dibujar_en_la_pizarra** (evento)

pilas.cargador.ejemplos.habilidad_personalizada_con_argumentos
-------------------------------------------------------------




class **GirarPorSiempre** (pilas.habilidades.Habilidad)

- **__init__** (self, receptor, velocidad=1)
- **actualizar** (self)

pilas.cargador.ejemplos.grupos_y_colisiones
------------------------------------------



pilas.cargador.ejemplos.globo_simple
-----------------------------------


- **ejecutar** ()

pilas.cargador.ejemplos.mapas
----------------------------



pilas.cargador.ejemplos.sonidos
------------------------------


- **reproducir_sonido_cuando_hace_click** (evento)

pilas.cargador.ejemplos.colores
------------------------------



pilas.cargador.ejemplos.colisiones
---------------------------------


- **comer_banana** (mono, banana)
- **hacer_explotar_una_bomba** (mono, bomba)

pilas.cargador.ejemplos.pizarra_dibuja_triangulo
-----------------------------------------------



pilas.cargador.ejemplos.duplicar
-------------------------------



pilas.cargador.ejemplos.texto
----------------------------



pilas.cargador.ejemplos.grilla
-----------------------------


- **avanzar_cuadro** (*k, **kv)

pilas.cargador.ejemplos.deslizador
---------------------------------


- **cuando_cambia_escala** (valor)
- **cuando_cambia_rotacion** (valor)
- **cuando_cambia_posicion** (valor)

pilas.cargador.ejemplos.dialogo_con_preguntas
--------------------------------------------


- **cuando_responde_color_favorito** (respuesta)

pilas.cargador.ejemplos.dialogo_con_funciones
--------------------------------------------


- **hacer_que_el_mono_salte** ()

pilas.cargador.ejemplos.pingu_controlado_por_teclado
---------------------------------------------------



pilas.cargador.ejemplos.tareas
-----------------------------


- **girar** ()

pilas.cargador.ejemplos.boton
----------------------------


- **cuando_pulsan_el_boton** ()
- **cuando_pasa_sobre_el_boton** ()
- **cuando_deja_de_pulsar** ()

pilas.cargador.ejemplos.habilidad_personalizada
----------------------------------------------




class **GirarPorSiempre** (pilas.habilidades.Habilidad)

- **__init__** (self, receptor)
- **actualizar** (self)

pilas.cargador.ejemplos.usando_pygame
------------------------------------



pilas.cargador.ejemplos.dialogo
------------------------------



pilas.cargador.ejemplos.pizarra_dibujando_con_el_mouse
-----------------------------------------------------


- **cuando_pulsa_el_boton** (evento)
- **cuando_deja_de_pulsar_el_boton** (evento)
- **cuando_mueve_el_mouse** (evento)

pilas.cargador.ejemplos.texto_que_cambia
---------------------------------------


- **cuando_pulsa_el_boton** ()

pilas.cargador.ejemplos.entrada_de_texto
---------------------------------------



pilas.cargador.ejemplos.menu
---------------------------


- **selecciona_iniciar** ()
- **selecciona_terminar** ()

pilas.cargador.ejemplos.ejemplo_piezas
-------------------------------------



pilas.cargador.ejemplos.ejes
---------------------------



pilas.cargador.ejemplos.ingreso_de_texto_y_selector
--------------------------------------------------



pilas.cargador.ejemplos.selector
-------------------------------


- **cuando_el_selector_cambia** (estado)

pilas.cargador.ejemplos.arrastrable
----------------------------------



pilas.cargador.ejemplos.mapa_desde_archivo
-----------------------------------------



pilas.cargador.ejemplos.actor
----------------------------



pilas.cargador.ejemplos.video_pelicula
-------------------------------------



pilas.cargador.ejemplos.lista_seleccion
--------------------------------------


- **cuando_selecciona** (opcion_seleccionada)

pilas.cargador.ejemplos.pizarra_dibuja_grilla
--------------------------------------------



pilas.cargador.ejemplos.dialogo_con_botones
------------------------------------------


- **cuando_pulsa_el_boton** (texto)

pilas.cargador.ejemplos.arrastrable_varios_z
-------------------------------------------



pilas.cargador.ejemplos.interpolacion
------------------------------------



pilas.cargador.ejemplos.puntaje
------------------------------


- **sumar_5_al_clickear** (evento)

pilas.cargador.ejemplos.camara
-----------------------------


- **girar** ()

pilas.cargador.ejemplos.ejemplo_temporizador
-------------------------------------------


- **funcion_callback** ()

pilas.cargador.ejemplos.escenas_con_menu
---------------------------------------




class **EscenaDeMenu** (Normal)

- **__init__** (self)
- **comenzar** (self)
- **salir** (self)


class **EscenaDeJuego** (Normal)

- **__init__** (self)
- **cuando_pulsa_tecla** (self, evento)

pilas.cargador.ejemplos.pizarra_dibuja_imagen
--------------------------------------------



pilas.cargador.ejemplos.mover_actor_por_eventos
----------------------------------------------


- **mover_al_mono** (contexto)

pilas.cargador.ejemplos.comportamientos_movimiento_de_mono
---------------------------------------------------------



pilas.cargador.ejemplos.moverse_con_el_teclado
---------------------------------------------



pilas.actores.mapa
-----------------




class **Mapa** (Actor)

- **__init__** (self, grilla_o_mapa, x=0, y=0, restitucion=0.56)
- **_cargar_mapa** (self, archivo)
- **_crear_bloques** (self, capa, solidos)
- **pintar_bloque** (self, fila, columna, indice, es_bloque_solido=False)
- **reiniciar** (self)
- **eliminar** (self)
- **_eliminar_bloques** (self)

pilas.actores.utils
------------------


- **ordenar_actores_por_valor_z** ()
- **insertar_como_nuevo_actor** (actor)
- **eliminar_un_actor** (actor)
- **eliminar_a_todos** ()
- **destruir_a_todos** ()
- **obtener_actor_en** (x, y)
- **fabricar** (clase, cantidad=1, posiciones_al_azar=True, *k, **kv)

pilas.actores.opcion
-------------------




class **Opcion** (Texto)

- **__init__** (self, texto, x=0, y=0, funcion_a_invocar=None)
- **resaltar** (self, estado=True)
- **seleccionar** (self)

pilas.actores.explosion
----------------------




class **Explosion** (Animacion)

- **__init__** (self, x=0, y=0)

pilas.actores.pizarra
--------------------




class **Lapiz** (object)

- **__init__** (self)
- **set_x** (self, x)
- **get_x** (self)
- **set_y** (self, y)
- **get_y** (self)
- **__init__** (self, ancho=640, alto=480)
- **asignar** (self, actor)
- **levantar_lapiz** (self)
- **bajar_lapiz** (self)
- **pintar_punto** (self, x, y, radio, color)
- **mover_lapiz** (self, x, y)
- **definir_color** (self, color)
- **pintar_imagen** (self, imagen, x=0, y=0)
- **pintar_grilla** (self, grilla, x=0, y=0)
- **pintar_parte_de_imagen** (self, imagen_cairo, origen_x, origen_y, ancho, alto, x, y)
- **pintar** (self, color=None)
- **escribir** (self, texto, x=0, y=0, tamano=32, fuente="sans")
- **obtener_area_de_texto** (self, texto, tamano=32, fuente="sans")
- **obtener_area_para_lista_de_texto** (self, lista, tamano=32, fuente="sans")
- **dibujar_rectangulo** (self, x, y, ancho, alto, pintar=True)
- **dibujar_poligono** (self, puntos)
- **pintar_cruz** (self, x, y, ancho, color)
- **limpiar** (self)
- **dibujar_circulo** (self, x, y, radio, pintar=True)


class **Pizarra** (Actor)

- **__init__** (self, x=0, y=0, ancho=None, alto=None)
- **dibujar_punto** (self, x, y, color=colores.negro)
- **obtener_coordenada_fisica** (self, x, y)
- **pintar_imagen** (self, imagen, x, y)
- **pintar_parte_de_imagen** (self, imagen, origen_x, origen_y, ancho, alto, x, y)
- **pintar** (self, color)
- **linea** (self, x, y, x2, y2, color=colores.negro, grosor=1)

pilas.actores.globoelegir
------------------------




class **GloboElegir** (Globo)

- **__init__** (self, texto, opciones, funcion_a_invocar, x=0, y=0, dialogo=None)
- **colocar_origen_del_globo** (self, x, y)
- **_actualizar_posicion_de_la_lista_de_seleccion** (self)
- **_obtener_area_para_el_texto** (self, texto)
- **_escribir_texto** (self, texto)
- **cuando_quieren_avanzar** (self, *k)
- **_cuando_selecciona_opcion** (self, opcion)

pilas.actores.temporizador
-------------------------




class **Temporizador** (Texto)

- **__init__** (self, x=0, y=0, color=colores.negro)
- **funcion_vacia** (self)
- **definir_tiempo_texto** (self, variable)
- **ajustar** (self, tiempo = 1, funcion = None)
- **restar_a_contador** (self)
- **iniciar** (self)

pilas.actores.animacion
----------------------




class **Animacion** (Animado)

- **__init__** (self, grilla, ciclica=False, x=0, y=0)
- **actualizar** (self)

pilas.actores.bomba
------------------




class **Bomba** (Animacion)

- **__init__** (self, x=0, y=0)
- **explotar** (self)

pilas.actores.texto
------------------




class **Texto** (Actor)

- **__init__** (self, texto="None", x=0, y=0)
- **obtener_texto** (self)
- **definir_texto** (self, texto)
- **obtener_magnitud** (self)
- **definir_magnitud** (self, magnitud)
- **obtener_color** (self)
- **definir_color** (self, color)

pilas.actores.disparo
--------------------




class **Disparo** (Animacion)

- **__init__** (self, x=0, y=0, rotacion=0, velocidad=2)
- **actualizar** (self)
- **avanzar** (self)

pilas.actores.animado
--------------------




class **Animado** (Actor)

- **__init__** (self, grilla, x=0, y=0)
- **definir_cuadro** (self, indice)

pilas.actores.pingu
------------------




class **Pingu** (Actor)

- **__init__** (self, x=0, y=0)
- **definir_cuadro** (self, indice)


class **Esperando** (Comportamiento)

- **iniciar** (self, receptor)
- **actualizar** (self)


class **Caminando** (Comportamiento)

- **__init__** (self)
- **actualizar** (self)
- **avanzar_animacion** (self)


class **Saltando** (Comportamiento)

- **__init__** (self)
- **iniciar** (self, receptor)
- **actualizar** (self)

pilas.actores.cursordisparo
--------------------------




class **CursorDisparo** (Actor)

- **__init__** (self, x=0, y=0)

pilas.actores.boton
------------------




class **Boton** (Actor)

- **_cargar_imagenes** (self, ruta_normal, ruta_press, ruta_over)
- **conectar_normal** (self, funcion, arg = "null")
- **conectar_presionado** (self, funcion, arg = "null")
- **conectar_sobre** (self, funcion, arg = "null")
- **desconectar_normal_todo** (self)
- **desconectar_presionado_todo** (self)
- **desconectar_sobre_todo** (self)
- **desconectar_normal** (self, funcion, arg = "null")
- **desconectar_presionado** (self, funcion, arg = "null")
- **desconectar_sobre** (self, funcion, arg = "null")
- **ejecutar_funciones_normal** (self)
- **ejecutar_funciones_press** (self)
- **ejecutar_funciones_over** (self)
- **activar** (self)
- **desactivar** (self)
- **pintar_normal** (self)
- **pintar_presionado** (self, ruta_press = "null")
- **pintar_sobre** (self)
- **detection_move_mouse** (self, evento)
- **detection_click_mouse** (self, click)
- **detection_end_click_mouse** (self, end_click)

pilas.actores.dialogo
--------------------


- **__init__** (self, modo_automatico=True)
- **decir** (self, actor, texto)
- **decir_inmediatamente** (self, actor, texto)
- **elegir** (self, actor, texto, opciones, funcion_a_invocar)
- **ejecutar** (self, funcion)
- **iniciar** (self)
- **obtener_siguiente_dialogo_o_funcion** (self)
- **_eliminar_dialogo_actual** (self)
- **_mostrar_o_ejecutar_siguiente** (self, siguiente)
- **avanzar_al_siguiente_dialogo** (self, evento=None)

pilas.actores.piedra
-------------------




class **Piedra** (Actor)

- **__init__** (self, x=0, y=0, tamano="grande", dx=0, dy=0)
- **actualizar** (self)

pilas.actores.moneda
-------------------




class **Moneda** (Animacion)

- **__init__** (self, x=0, y=0)

pilas.actores.nave
-----------------




class **Nave** (Animacion)

- **__init__** (self, x=0, y=0, velocidad=2)
- **actualizar** (self)
- **eliminar_disparos_innecesarios** (self)
- **disparar** (self)
- **avanzar** (self)
- **definir_enemigos** (self, grupo, cuando_elimina_enemigo=None)
- **hacer_explotar_al_enemigo** (self, mi_disparo, el_enemigo)

pilas.actores.menu
-----------------




class **Menu** (Actor)

- **__init__** (self, opciones, x=0, y=0)
- **activar** (self)
- **desactivar** (self)
- **crear_texto_de_las_opciones** (self, opciones)
- **seleccionar_primer_opcion** (self)
- **_verificar_opciones** (self, opciones)
- **actualizar** (self)
- **seleccionar_opcion_actual** (self)
- **mover_cursor** (self, delta)
- **__setattr__** (self, atributo, valor)
- **cuando_mueve_el_mouse** (self, evento)
- **_deshabilitar_opcion_actual** (self)
- **cuando_hace_click_con_el_mouse** (self, evento)

pilas.actores.mono
-----------------




class **Mono** (Actor)

- **__init__** (self, x=0, y=0)
- **sonreir** (self)
- **gritar** (self)
- **normal** (self)
- **decir** (self, mensaje)

pilas.actores.ejes
-----------------




class **Ejes** (Actor)

- **__init__** (self, x=0, y=0)

pilas.actores.martian
--------------------




class **Martian** (Actor)

- **__init__** (self, x=0, y=0)
- **definir_cuadro** (self, indice)
- **mover** (self, x, y)
- **actualizar** (self)
- **crear_disparo** (self)


class **Esperando** (Comportamiento)

- **iniciar** (self, receptor)
- **actualizar** (self)


class **Caminando** (Comportamiento)

- **__init__** (self)
- **actualizar** (self)
- **avanzar_animacion** (self)


class **Saltando** (Comportamiento)

- **iniciar** (self, receptor)
- **actualizar** (self)


class **Disparar** (Comportamiento)

- **__init__** (self, receptor)
- **actualizar** (self)
- **avanzar_animacion** (self)

pilas.actores.tortuga
--------------------




class **Tortuga** (Actor)

- **__init__** (self, x=0, y=0, dibuja=True)
- **avanzar** (self, pasos)
- **giraderecha** (self, delta)
- **giraizquierda** (self, delta)
- **actualizar** (self)
- **dibujar_linea_desde_el_punto_anterior** (self)
- **bajalapiz** (self)
- **subelapiz** (self)
- **pon_color** (self, color)
- **crear_poligono** (self, lados = 4, escala = 100, sentido = -1)
- **crear_circulo** (self, radio = 30, sentido = -1)
- **get_color** (self)
- **set_color** (self, color)
- **pintar** (self, color=None)

pilas.actores.actor
------------------


- **__init__** (self, imagen="sin_imagen.png", x=0, y=0)
- **definir_centro(self, ** (x, y))
- **_interpretar_y_convertir_posicion** (self, posicion, maximo_valor)
- **obtener_centro** (self)
- **definir_posicion** (self, x, y)
- **obtener_posicion** (self)
- **dibujar** (self, aplicacion)
- **get_x** (self)
- **set_x** (self, x)
- **get_z** (self)
- **set_z** (self, z)
- **set_y** (self, y)
- **get_y** (self)
- **set_scale** (self, s)
- **get_scale** (self)
- **get_rotation** (self)
- **set_rotation** (self, x)
- **get_espejado** (self)
- **set_espejado** (self, nuevo_valor)
- **set_transparencia** (self, nuevo_valor)
- **get_transparencia** (self)
- **get_imagen** (self)
- **set_imagen** (self, imagen)
- **eliminar** (self)
- **destruir** (self)
- **actualizar** (self)
- **pre_actualizar** (self)
- **__cmp__** (self, otro_actor)
- **get_izquierda** (self)
- **set_izquierda** (self, x)
- **get_derecha** (self)
- **set_derecha** (self, x)
- **get_abajo** (self)
- **set_abajo** (self, y)
- **get_arriba** (self)
- **set_arriba** (self, y)
- **colisiona_con_un_punto** (self, x, y)
- **obtener_rotacion** (self)
- **definir_rotacion** (self, r)
- **definir_color** (self, c)
- **obtener_imagen** (self)
- **definir_imagen** (self, imagen)
- **duplicar** (self, **kv)
- **obtener_ancho** (self)
- **obtener_alto** (self)
- **__mul__** (self, cantidad)
- **__str__** (self)
- **obtener_escala** (self)
- **definir_escala** (self, escala)
- **definir_transparencia** (self, valor)
- **imitar** (self, otro_actor_o_figura)
- **esta_fuera_de_la_pantalla** (self)
- **decir** (self, mensaje, autoeliminar=True)
- **anexar** (self, otro_actor)
- **_eliminar_anexados** (self)

pilas.actores.banana
-------------------




class **Banana** (Actor)

- **__init__** (self, x=0, y=0)
- **definir_cuadro** (self, indice)
- **abrir** (self)
- **cerrar** (self)

pilas.actores.puntaje
--------------------




class **Puntaje** (Texto)

- **__init__** (self, texto='0', x=0, y=0, color=pilas.colores.negro)
- **definir** (self, puntaje_variable = '0')
- **aumentar** (self, cantidad=1)
- **obtener** (self)

pilas.actores.estrella
---------------------




class **Estrella** (Actor)

- **__init__** (self, x=0, y=0)

pilas.actores.aceituna
---------------------




class **Aceituna** (Actor)

- **__init__** (self, x=0, y=0)
- **normal** (self)
- **reir** (self)
- **burlarse** (self)
- **gritar** (self)

pilas.actores.pelota
-------------------




class **Pelota** (Actor)

- **__init__** (self, x=0, y=0)

pilas.actores.caja
-----------------




class **Caja** (Actor)

- **__init__** (self, x=0, y=0)

pilas.actores.globo
------------------




class **Globo** (Actor)

- **__init__** (self, texto, x=0, y=0, dialogo=None, avance_con_clicks=True, autoeliminar=False)
- **colocar_origen_del_globo** (self, x, y)
- **cuando_quieren_avanzar** (self, *k)
- **_pintar_globo** (self, ancho, alto)
- **eliminar** (self)

pilas.actores.entradadetexto
---------------------------




class **EntradaDeTexto** (Actor)

- **__init__** (self, x=0, y=0, imagen='invisible.png', color=pilas.colores.negro, limite=10, tamano=32, fuente='Arial', cursor_intermitente=True)
- **_actualizar_cursor** (self)
- **_asignar_atributos** (self, x, y, color, limite, tamano, fuente)
- **cuando_pulsa_una_tecla** (self, evento)
- **_actualizar_imagen** (self)
- **definir_escala** (self, s)
- **definir_rotacion** (self, r)
- **definir_posicion** (self, x, y)

pilas.interfaz.deslizador
------------------------




class **Deslizador** (Actor)

- **set_transparencia** (self, nuevo_valor)
- **set_x** (self, x)
- **set_y** (self, y)
- **conectar** (self, f)
- **desconectar** (self, f)
- **ejecutar_funciones** (self, valor)
- **click_del_mouse** (self, click)
- **movimiento_del_mouse** (self, movimiento)
- **termino_del_click** (self, noclick)

pilas.interfaz.selector
----------------------




class **Selector** (pilas.actores.Actor)

- **__init__** (self, texto, x=0, y=0, ancho=200)
- **_cargar_imagenes** (self, pilas)
- **_cargar_lienzo** (self, ancho)
- **pintar_texto** (self)
- **deseleccionar** (self)
- **seleccionar** (self)
- **detection_click_mouse** (self, click)
- **alternar_seleccion** (self)
- **definir_accion** (self, funcion)

pilas.interfaz.lista_seleccion
-----------------------------




class **ListaSeleccion** (Actor)

- **__init__** (self, opciones, funcion_a_ejecutar, x=0, y=0)
- **_pintar_opciones** (self, pinta_indice_opcion=None)
- **cuando_mueve_el_mouse** (self, evento)
- **cuando_hace_click_con_el_mouse** (self, evento)
- **_detectar_opcion_bajo_el_mouse** (self, evento)

pilas.interfaz.ingreso_de_texto
------------------------------




class **IngresoDeTexto** (pilas.actores.Actor)

- **__init__** (self, x=0, y=0)
- **_actualizar_cursor** (self)
- **_cargar_imagenes** (self, pilas)
- **cuando_pulsa_una_tecla** (self, evento)
- **_cargar_lienzo** (self)
- **_actualizar_imagen** (self)

pilas.data.juegobase.ejecutar
----------------------------



pilas.motores.motor_qt
---------------------


- **__init__** (self)
- **definir_centro** (self, x, y)
- **obtener_posicion** (self)
- **definir_posicion** (self, x, y)
- **obtener_escala** (self)
- **definir_escala** (self, s)
- **definir_transparencia** (self, nuevo_valor)
- **obtener_rotacion** (self)
- **definir_rotacion** (self, r)
- **set_espejado** (self, espejado)
- **__init__** (self, ruta)
- **ancho** (self)
- **alto** (self)
- **centro** (self)
- **dibujar** (self, motor, x, y, dx=0, dy=0, escala_x=1, escala_y=1, rotacion=0)
- **_dibujar_pixmap** (self, motor, x, y)


class **QtGrilla** (QtImagen)

- **__init__** (self, ruta, columnas=1, filas=1)
- **ancho** (self)
- **alto** (self)
- **_dibujar_pixmap** (self, motor, x, y)
- **definir_cuadro** (self, cuadro)
- **avanzar** (self)


class **QtTexto** (QtImagen)

- **_dibujar_pixmap** (self, motor, dx, dy)


class **QtLienzo** (QtImagen)

- **__init__** (self)
- **texto** (self, motor, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro)
- **texto_absoluto** (self, motor, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro)
- **pintar** (self, motor, color)
- **linea** (self, motor, x0, y0, x1, y1, color=colores.negro)
- **cruz** (self, motor, x, y, color=colores.negro)
- **circulo** (self, motor, x, y, radio, color=colores.negro)
- **rectangulo** (self, motor, x, y, ancho, alto, color=colores.negro)


class **QtSuperficie** (QtImagen)

- **__init__** (self, ancho, alto)
- **pintar** (self, color)
- **pintar_parte_de_imagen** (self, imagen, origen_x, origen_y, ancho, alto, x, y)
- **texto** (self, cadena, x=0, y=0, magnitud=10, fuente=None, color=colores.negro)
- **circulo** (self, x, y, radio, color=colores.negro, relleno=False, grosor=1)
- **rectangulo** (self, x, y, ancho, alto, color=colores.negro, relleno=False, grosor=1)
- **linea** (self, x, y, x2, y2, color=colores.negro, grosor=1)
- **dibujar_punto** (self, x, y, color=colores.negro)


class **QtActor** (BaseActor)

- **__init__** (self, imagen="sin_imagen.png", x=0, y=0)
- **definir_imagen** (self, imagen)
- **obtener_imagen** (self)
- **dibujar** (self, motor)
- **__init__** (self, ruta)
- **reproducir** (self)
- **__init__** (self, ancho, alto)
- **actualizar** (self)
- **limpiar** (self)
- **__init__** (self, ancho, alto, titulo)
- **do_update** (self)
- **hacer_flotante_la_ventana_en_i3** (self)
- **paintEvent** (self, event)
- **keyPressEvent** (self, event)
- **wheelEvent** (self, event)
- **render** (self, event, qp)


class **QtBase** (motor.Motor)

- **__init__** (self)
- **iniciar_ventana** (self, ancho, alto, titulo, pantalla_completa)
- **centro_fisico** (self)
- **obtener_area** (self)
- **centrar_ventana** (self)
- **obtener_actor** (self, imagen, x, y)
- **obtener_texto** (self, texto)
- **obtener_posicion_del_mouse** (self)
- **obtener_canvas** (self, ancho, alto)
- **obtener_grilla** (self, ruta, columnas, filas)
- **ocultar_puntero_del_mouse** (self)
- **mostrar_puntero_del_mouse** (self)
- **cerrar_ventana** (self)
- **procesar_y_emitir_eventos** (self)
- **procesar_evento_teclado** (self, event)
- **actualizar_pantalla** (self)
- **definir_centro_de_la_camara** (self, x, y)
- **obtener_centro_de_la_camara** (self)
- **pintar** (self, color)
- **cargar_sonido** (self, ruta)
- **cargar_imagen** (self, ruta)
- **obtener_lienzo** (self)
- **obtener_superficie** (self, ancho, alto)
- **guardar_captura** (self)
- **_obtener_numeracion_siguiente_imagen** (self)
- **ejecutar_bucle_principal** (self, mundo, ignorar_errores)
- **paintEvent** (self, event)
- **timerEvent** (self, event)
- **realizar_actualizacion_logica** (self)
- **resizeEvent** (self, event)
- **mousePressEvent** (self, e)
- **mouseReleaseEvent** (self, e)
- **mouseMoveEvent** (self, e)
- **keyPressEvent** (self, event)
- **keyReleaseEvent** (self, event)
- **obtener_codigo_de_tecla_normalizado** (self, tecla_qt)
- **escala** (self)
- **obtener_area_de_texto** (self, texto)
- **__init__** (self)
- **__init__** (self)

pilas.motores.motor_pygame
-------------------------


- **__init__** (self)
- **obtener_escala** (self)
- **__init__** (self, image="sin_imagen.png", x=0, y=0)
- **obtener_ancho** (self)
- **obtener_alto** (self)
- **obtener_area** (self)
- **definir_imagen** (self, imagen)
- **obtener_imagen** (self)
- **dibujar** (self, aplicacion)
- **duplicar** (self, **kv)
- **__str__** (self)
- **definir_centro** (self, x, y)
- **obtener_posicion** (self)
- **definir_posicion** (self, x, y)
- **definir_escala** (self, s)
- **obtener_rotacion** (self)
- **definir_rotacion** (self, r)
- **__init__** (self, texto="None", x=0, y=0)
- **obtener_texto** (self)
- **definir_texto** (self, texto)
- **obtener_magnitud** (self)
- **definir_magnitud** (self, size)
- **_set_central_axis** (self)
- **obtener_posicion** (self)
- **definir_posicion** (self, x, y)
- **obtener_color** (self)
- **definir_color** (self, k)
- **dibujar** (self, aplicacion)
- **colisiona_con_un_punto** (self, x, y)
- **obtener_ancho** (self)
- **obtener_alto** (self)
- **obtener_area** (self)
- **definir_centro** (self, x, y)
- **__init__** (self, ancho, alto)
- **actualizar** (self)
- **limpiar** (self)
- **__init__** (self, ruta, columnas=1, filas=1)
- **crear_grilla_de_imagenes** (self)
- **definir_cuadro** (self, cuadro)
- **asignar** (self, sprite)
- **avanzar** (self)
- **obtener_cuadro** (self)
- **obtener_componentes** (self)
- **__init__** (self, ruta)
- **reproducir** (self)
- **Play** (self)
- **__init__** (self)
- **crear_ventana** (self, ancho, alto, titulo)
- **cerrar_ventana** (self)
- **dibujar_circulo** (self, x, y, radio, color, color_borde)
- **cargar_sonido** (self, ruta)
- **centrar_ventana** (self)
- **pulsa_tecla** (self, tecla)
- **procesar_y_emitir_eventos** (self)
- **procesar_evento_teclado** (self, event)
- **actualizar_pantalla** (self)
- **obtener_canvas** (self, ancho, alto)
- **obtener_texto** (self, texto, x, y)
- **obtener_grilla** (self, ruta, columnas, filas)
- **ocultar_puntero_del_mouse** (self)
- **mostrar_puntero_del_mouse** (self)
- **obtener_posicion_del_mouse** (self)
- **pintar** (self, color)
- **cargar_imagen** (self, ruta)
- **obtener_centro_de_la_camara** (self)
- **definir_centro_de_la_camara** (self, x, y)
- **generar_imagen_cairo** (self, imagen)
- **obtener_actor** (self, imagen, x, y)
- **ejecutar_bucle_principal** (self, mundo, ignorar_errores)

pilas.motores.motor
------------------


- **abstract** ()


class **Motor** (object)

- **__init__** (self)
- **obtener_actor** (self, imagen, x, y)
- **obtener_texto** (self, texto, x, y)
- **obtener_canvas** (self, ancho, alto)
- **obtener_grilla** (self, ruta, columnas, filas)
- **crear_ventana** (self, ancho, alto, titulo)
- **ocultar_puntero_del_mouse** (self)
- **mostrar_puntero_del_mouse** (self)
- **cerrar_ventana** (self)
- **dibujar_circulo** (self, x, y, radio, color, color_borde)
- **pulsa_tecla** (self, tecla)
- **centrar_ventana** (self)
- **procesar_y_emitir_eventos** (self)
- **procesar_evento_teclado** (self, event)
- **definir_centro_de_la_camara** (self, x, y)
- **obtener_centro_de_la_camara** (self)
- **pintar** (self, color)
- **cargar_sonido** (self, ruta)
- **cargar_imagen** (self, ruta)
- **obtener_imagen_cairo** (self, imagen)
- **ejecutar_bucle_principal** (self, mundo, ignorar_errores)

pilas.dispatch.saferef
---------------------


- **safeRef** (target, onDelete = None)


class **BoundMethodWeakref** (object)

- **__new__** ( cls, target, onDelete=None, *arguments,**named )
- **__init__** (self, target, onDelete=None)
- **remove** (weak, self=self)
- **calculateKey** ( cls, target )
- **__str__** (self)
- **__nonzero__** ( self )
- **__cmp__** ( self, other )
- **__call__** (self)


class **BoundNonDescriptorMethodWeakref** (BoundMethodWeakref)

- **foo** (self)
- **__init__** (self, target, onDelete=None)
- **__call__** (self)
- **get_bound_method_weakref** (target, onDelete)

pilas.dispatch.dispatcher
------------------------




class **DictObj** (object)

- **__init__** (self, d)
- **__getattr__** (self, m)
- **__str__** (self)
- **_make_id** (target)


class **Signal** (object)

- **__init__** (self, providing_args=None)
- **conectar** (self, receptor, emisor=None, weak=True, uid=None)
- **connect** (self, receiver, sender=None, weak=True, uid=None)
- **desconectar** (self, receptor=None, emisor=None, weak=True, uid=None)
- **disconnect** (self, receiver=None, sender=None, weak=True, uid=None)
- **send** (self, sender, **named)
- **send_robust** (self, sender, **named)
- **_live_receivers** (self, senderkey)
- **_remove_receiver** (self, receiver)
- **esta_conectado** (self)
- **imprimir_funciones_conectadas** (self)
