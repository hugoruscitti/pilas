pilas.comportamientos
---------------------




class **Comportamiento** (object)

- **actualizar** ()
- **terminar** ()


class **Girar** (Comportamiento)

- **actualizar** ()


class **Saltar** (Comportamiento)

- **actualizar** ()


class **Avanzar** (Comportamiento)

- **actualizar** ()

pilas.tareas
------------




class **Tarea** (object)

- **ejecutar** ()
- **eliminar** ()


class **TareaCondicional** (Tarea)

- **ejecutar** ()


class **Tareas** (object)

- **__init__** ()

pilas.imagenes
--------------


- **cargar** (ruta)

pilas.grupo
-----------




class **Grupo** (list)

- **desordenar** ()
- **limpiar** ()

pilas.lienzo
------------



pilas.xmlreader
---------------


- **getData** ()
- **makeRootNode** (xmlFileName)

pilas.interpolaciones
---------------------




class **Interpolacion** (object)



class **Lineal** (Interpolacion)

- **__neg__** ()

pilas.red
---------


- **setup** ()
- **handle** ()
- **finish** ()

pilas.escenas
-------------




class **Escena** (object)

- **__init__** ()
- **iniciar** ()
- **terminar** ()


class **Normal** (Escena)


pilas.atajos
------------


- **crear_grupo** (xk)

pilas.fondos
------------




class **Fondo** (pilas.actores.Actor)



class **Volley** (Fondo)

- **__init__** ()


class **Pasto** (Fondo)

- **__init__** ()


class **Selva** (Fondo)

- **__init__** ()


class **Tarde** (Fondo)

- **__init__** ()


class **Espacio** (Fondo)

- **__init__** ()


class **Noche** (Fondo)

- **__init__** ()


class **Color** (Fondo)


pilas.control
-------------




class **Control** (object)

- **__init__** ()
- **actualizar** ()
- **__init__** ()
- **__str__** ()

pilas.simbolos
--------------



pilas.fisica
------------




class **Fisica** (object)

- **crear_bordes_del_escenario** ()
- **reiniciar** ()
- **cuando_suelta_el_mouse** ()
- **actualizar** ()
- **_procesar_figuras_a_eliminar** ()
- **eliminar_suelo** ()
- **eliminar_techo** ()
- **eliminar_paredes** ()


class **Figura** (object)

- **obtener_x** ()
- **obtener_y** ()
- **obtener_rotacion** ()
- **obtener_velocidad_lineal** ()
- **detener** ()
- **eliminar** ()


class **Circulo** (Figura)



class **Rectangulo** (Figura)



class **ConstanteDeMovimiento** ()

- **eliminar** ()


class **ConstanteDeDistancia** ()

- **eliminar** ()

pilas.evento
------------



pilas.utils
-----------


- **es_interpolacion** (an_object)
- **obtener_ruta_al_recurso** (ruta)
- **interpolable** (f)
- **obtener_area_de_texto** (texto)

pilas.colisiones
----------------


- **__init__** ()
- **verificar_colisiones** ()

pilas.fps
---------


- **actualizar** ()
- **obtener_cuadros_por_segundo** ()


class **FPS** (object)

- **actualizar** ()
- **obtener_cuadros_por_segundo** ()

pilas.sonidos
-------------


- **cargar** (ruta)

pilas.colores
-------------




class **Color** (object)

- **obtener** ()
- **__str__** ()
- **obtener_componentes** ()

pilas.mundo
-----------




class **Mundo** (object)

- **reiniciar** ()
- **terminar** ()

pilas.pytweener
---------------




class **Tweener** (object)

- **hasTweens** ()
- **finish** ()


class **Tween** (object)

- **decodeArguments** ()
- **Remove** ()
- **__init__** ()
- **update** ()
- **getRotation** ()
- **complete** ()

pilas.habilidades
-----------------




class **Habilidad** (object)

- **actualizar** ()
- **eliminar** ()


class **RebotarComoPelota** (Habilidad)

- **eliminar** ()


class **RebotarComoCaja** (Habilidad)

- **eliminar** ()


class **ColisionableComoPelota** (RebotarComoPelota)

- **actualizar** ()
- **eliminar** ()


class **SeguirAlMouse** (Habilidad)



class **AumentarConRueda** (Habilidad)



class **SeguirClicks** (Habilidad)



class **Arrastrable** (Habilidad)

- **comienza_a_arrastrar** ()
- **termina_de_arrastrar** ()
- **_el_receptor_tiene_fisica** ()


class **MoverseConElTeclado** (Habilidad)



class **PuedeExplotar** (Habilidad)

- **eliminar_y_explotar** ()


class **SeMantieneEnPantalla** (Habilidad)

- **actualizar** ()


class **PisaPlataformas** (Habilidad)

- **actualizar** ()
- **eliminar** ()


class **Imitar** (Habilidad)

- **actualizar** ()
- **eliminar** ()

pilas.estudiante
----------------


- **__init__** ()
- **eliminar_habilidades** ()
- **eliminar_comportamientos** ()
- **actualizar_habilidades** ()
- **actualizar_comportamientos** ()
- **_adoptar_el_siguiente_comportamiento** ()

pilas.pilasversion
------------------



pilas.ventana
-------------



pilas.camara
------------




class **Camara** (object)

- **_get_x** ()
- **_get_y** ()

pilas.depurador
---------------




class **Depurador** (object)



class **ModoDepurador** (object)

- **orden_de_tecla** ()


class **ModoPuntosDeControl** (ModoDepurador)



class **ModoRadiosDeColision** (ModoDepurador)



class **ModoArea** (ModoDepurador)



class **ModoPosicion** (ModoDepurador)



class **ModoFisica** (ModoDepurador)



class **ModoInformacionDeSistema** (ModoDepurador)


pilas.dispatch.saferef
----------------------




class **BoundMethodWeakref** (object)

- **__str__** ()
- **__call__** ()


class **BoundNonDescriptorMethodWeakref** (BoundMethodWeakref)

- **foo** ()
- **__call__** ()

pilas.dispatch.dispatcher
-------------------------




class **DictObj** (object)

- **__str__** ()
- **_make_id** (target)


class **Signal** (object)

- **esta_conectado** ()
- **imprimir_funciones_conectadas** ()

pilas.actores.pelota
--------------------




class **Pelota** (Actor)


pilas.actores.animado
---------------------




class **Animado** (Actor)


pilas.actores.nave
------------------




class **Nave** (Animacion)

- **actualizar** ()
- **eliminar_disparos_innecesarios** ()
- **disparar** ()
- **avanzar** ()

pilas.actores.pausa
-------------------




class **Pausa** (Actor)


pilas.actores.opcion
--------------------




class **Opcion** (Texto)

- **seleccionar** ()

pilas.actores.estrella
----------------------




class **Estrella** (Actor)


pilas.actores.piedra
--------------------




class **Piedra** (Actor)

- **actualizar** ()

pilas.actores.aceituna
----------------------




class **Aceituna** (Actor)

- **normal** ()
- **reir** ()
- **burlarse** ()
- **gritar** ()
- **saltar** ()

pilas.actores.texto
-------------------




class **Texto** (Actor)

- **obtener_texto** ()
- **obtener_magnitud** ()
- **obtener_color** ()

pilas.actores.banana
--------------------




class **Banana** (Actor)

- **abrir** ()
- **cerrar** ()

pilas.actores.globoelegir
-------------------------




class **GloboElegir** (Globo)


pilas.actores.ejes
------------------




class **Ejes** (Actor)


pilas.actores.cooperativista
----------------------------




class **Cooperativista** (Actor)



class **Esperando** (Comportamiento)

- **actualizar** ()


class **Caminando** (Comportamiento)

- **__init__** ()
- **actualizar** ()
- **avanzar_animacion** ()


class **Saltando** (Comportamiento)

- **__init__** ()
- **actualizar** ()

pilas.actores.dialogo
---------------------


- **iniciar** ()
- **obtener_siguiente_dialogo_o_funcion** ()
- **_eliminar_dialogo_actual** ()

pilas.actores.disparo
---------------------




class **Disparo** (Animacion)

- **actualizar** ()
- **avanzar** ()

pilas.actores.bomba
-------------------




class **Bomba** (Animacion)

- **explotar** ()

pilas.actores.pizarra
---------------------




class **Pizarra** (Actor)


pilas.actores.tortuga
---------------------




class **Tortuga** (Actor)

- **actualizar** ()
- **dibujar_linea_desde_el_punto_anterior** ()
- **bajalapiz** ()
- **subelapiz** ()
- **get_color** ()

pilas.actores.mono
------------------




class **Mono** (Actor)

- **sonreir** ()
- **gritar** ()
- **normal** ()

pilas.actores.puntaje
---------------------




class **Puntaje** (Texto)

- **obtener** ()

pilas.actores.utils
-------------------


- **insertar_como_nuevo_actor** (actor)
- **eliminar_un_actor** (actor)

pilas.actores.mano
------------------




class **CursorMano** (Actor)

- **_cargar_imagenes** ()

pilas.actores.cursordisparo
---------------------------




class **CursorDisparo** (Actor)


pilas.actores.actor
-------------------


- **obtener_centro** ()
- **obtener_posicion** ()
- **get_x** ()
- **get_z** ()
- **get_y** ()
- **get_scale** ()
- **get_rotation** ()
- **get_espejado** ()
- **get_transparencia** ()
- **get_imagen** ()
- **get_fijo** ()
- **eliminar** ()
- **destruir** ()
- **actualizar** ()
- **pre_actualizar** ()
- **get_izquierda** ()
- **get_derecha** ()
- **get_abajo** ()
- **get_arriba** ()
- **obtener_rotacion** ()
- **obtener_imagen** ()
- **obtener_ancho** ()
- **obtener_alto** ()
- **__str__** ()
- **obtener_escala** ()
- **esta_fuera_de_la_pantalla** ()
- **_eliminar_anexados** ()

pilas.actores.explosion
-----------------------




class **Explosion** (Animacion)


pilas.actores.animacion
-----------------------




class **Animacion** (Animado)

- **obtener_velocidad_de_animacion** ()
- **actualizar** ()

pilas.actores.globo
-------------------




class **Globo** (Actor)

- **eliminar** ()

pilas.actores.temporizador
--------------------------




class **Temporizador** (Texto)

- **funcion_vacia** ()
- **_restar_a_contador** ()
- **iniciar** ()

pilas.actores.pingu
-------------------




class **Pingu** (Actor)



class **Esperando** (Comportamiento)

- **actualizar** ()


class **Caminando** (Comportamiento)

- **__init__** ()
- **actualizar** ()
- **avanzar_animacion** ()


class **Saltando** (Comportamiento)

- **__init__** ()
- **actualizar** ()

pilas.actores.menu
------------------




class **Menu** (Actor)

- **activar** ()
- **desactivar** ()
- **seleccionar_primer_opcion** ()
- **actualizar** ()
- **seleccionar_opcion_actual** ()
- **_deshabilitar_opcion_actual** ()

pilas.actores.moneda
--------------------




class **Moneda** (Animacion)


pilas.actores.martian
---------------------




class **Martian** (Actor)

- **actualizar** ()
- **crear_disparo** ()
- **puede_saltar** ()


class **Esperando** (Comportamiento)

- **actualizar** ()


class **Caminando** (Comportamiento)

- **__init__** ()
- **actualizar** ()
- **avanzar_animacion** ()


class **Saltando** (Comportamiento)

- **actualizar** ()


class **Disparar** (Comportamiento)

- **actualizar** ()
- **avanzar_animacion** ()

pilas.actores.caja
------------------




class **Caja** (Actor)


pilas.actores.boton
-------------------




class **Boton** (Actor)

- **desconectar_normal_todo** ()
- **desconectar_presionado_todo** ()
- **desconectar_sobre_todo** ()
- **ejecutar_funciones_normal** ()
- **ejecutar_funciones_press** ()
- **ejecutar_funciones_over** ()
- **activar** ()
- **desactivar** ()
- **pintar_normal** ()
- **pintar_sobre** ()

pilas.actores.mapa
------------------




class **Mapa** (Actor)

- **reiniciar** ()
- **eliminar** ()
- **_eliminar_bloques** ()

pilas.actores.entradadetexto
----------------------------




class **EntradaDeTexto** (Actor)

- **_actualizar_cursor** ()
- **_actualizar_imagen** ()

pilas.motores.motor_qt
----------------------




class **BaseActor** (object)

- **__init__** ()
- **obtener_posicion** ()
- **obtener_escala** ()
- **obtener_transparencia** ()
- **obtener_rotacion** ()


class **QtImagen** (object)

- **ancho** ()
- **alto** ()
- **centro** ()
- **avanzar** ()
- **__str__** ()


class **QtGrilla** (QtImagen)

- **ancho** ()
- **alto** ()
- **avanzar** ()
- **obtener_cuadro** ()


class **QtTexto** (QtImagen)

- **ancho** ()
- **alto** ()


class **QtLienzo** (QtImagen)

- **__init__** ()


class **QtSuperficie** (QtImagen)

- **limpiar** ()


class **QtActor** (BaseActor)

- **obtener_imagen** ()
- **reproducir** ()


class **QtBase** (motor.Motor)

- **__init__** ()
- **pantalla_completa** ()
- **pantalla_modo_ventana** ()
- **esta_en_pantalla_completa** ()
- **alternar_pantalla_completa** ()
- **centro_fisico** ()
- **obtener_area** ()
- **centrar_ventana** ()
- **actualizar_pantalla** ()
- **obtener_centro_de_la_camara** ()
- **obtener_lienzo** ()
- **realizar_actualizacion_logica** ()
- **escala** ()
- **alternar_pausa** ()
- **ocultar_puntero_del_mouse** ()
- **__init__** ()
- **__init__** ()
- **_pintar_fondo_negro** ()

pilas.motores.motor
-------------------




class **Motor** (object)

- **__init__** ()
- **ocultar_puntero_del_mouse** ()
- **mostrar_puntero_del_mouse** ()
- **cerrar_ventana** ()
- **centrar_ventana** ()
- **procesar_y_emitir_eventos** ()
- **obtener_centro_de_la_camara** ()

pilas.video.video
-----------------




class **MissingOpencv** (Exception)

- **__init__** ()
- **__str__** ()


class **DeCamara** (pilas.actores.Actor)

- **actualizar_video** ()


class **VideoDeArchivo** (object)

- **obtener_imagen** ()


class **DePelicula** (pilas.actores.Actor)

- **actualizar_video** ()

pilas.video.webcam
------------------




class **__camara_buffer** (object)

- **__init__** ()
- **_obtener_imagen_de_camara** ()

pilas.ejemplos.piezas
---------------------




class **Piezas** (pilas.escenas.Normal)



class **Pieza** (pilas.actores.Animado)

- **soltar_todas_las_piezas_del_grupo** ()
- **soltar** ()
- **__repr__** ()
- **get_x** ()
- **get_y** ()
- **mostrar_arriba_todas_las_piezas** ()
- **mostrar_abajo_todas_las_piezas** ()

pilas.ejemplos.listaseleccion
-----------------------------


- **cuando_selecciona** (opcion)

pilas.ejemplos.fisica
---------------------




class **ColisionesFisicas** (pilas.escenas.Normal)

- **__init__** ()

pilas.ejemplos.colisiones
-------------------------




class **Colisiones** (pilas.escenas.Normal)

- **__init__** ()
- **crear_personajes** ()

pilas.interfaz.lista_seleccion
------------------------------




class **ListaSeleccion** (Actor)


pilas.interfaz.selector
-----------------------




class **Selector** (pilas.actores.Actor)

- **_cargar_imagenes** ()
- **pintar_texto** ()
- **deseleccionar** ()
- **seleccionar** ()
- **alternar_seleccion** ()

pilas.interfaz.deslizador
-------------------------




class **Deslizador** (Actor)


pilas.interfaz.boton
--------------------




class **Boton** (pilas.actores.Actor)

- **_crear_imagenes_de_botones** ()

pilas.interfaz.ingreso_de_texto
-------------------------------




class **IngresoDeTexto** (pilas.actores.Actor)

- **_actualizar_cursor** ()
- **cualquier_caracter** ()
- **solo_numeros** ()
- **solo_letras** ()
- **_actualizar_imagen** ()

pilas.data.juegobase.ejecutar
-----------------------------


