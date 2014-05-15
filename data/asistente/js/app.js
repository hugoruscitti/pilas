var app = angular.module('app', ['ngRoute', 'ngAnimate', 'ui.bootstrap']);

app.config(['$routeProvider', function($routeProvider) {
    $routeProvider.
          when('/', {
            controller: 'PrincipalCtrl',
            templateUrl: 'partials/principal.html'
          }).
          when('/ejemplos', {
            controller: 'EjemplosCtrl',
            templateUrl: 'partials/ejemplos.html'
          }).
          otherwise({redirectTo:'/'});
}]);

var ModalCodigoCtrl = function($scope, $modalInstance, $http, juego) {
    $scope.data = {};
    $scope.data.juego = juego;
    $scope.data.codigo = window.interlocutor.obtener_codigo_del_ejemplo(juego.nick);

    $scope.cancelar = function () {
        $modalInstance.dismiss('cancel');
    };

    $scope.ejecutar = function(juego) {
        window.interlocutor.abrir_ejemplo(juego);
    };
};


app.controller("MainCtrl", function($scope, $location){
});

app.controller("PrincipalCtrl", function($scope, $location){
});

app.controller("EjemplosCtrl", function($scope, $location, $modal){
    $scope.data = {};

    $scope.abrir_ejemplo = function(nick) {
        window.interlocutor.abrir_ejemplo(nick);
    }

    $scope.mostrar_codigo = function(juego) {

        var modalInstance = $modal.open({
            templateUrl: 'partials/modal_codigo.html',
            controller: ModalCodigoCtrl,
            resolve: {
                juego: function () {
                    return juego;
                }
            }
        });

    }

    $scope.data.ejemplos = [
        {
            titulo: "Muchos actores",
            nick: 'muchos_actores',
            tags: ['camara', 'rotacion']
        },
        {
            titulo: "Actor personalizado",
            nick: 'actor_personalizado',
            tags: ['actor']
        },
        {
            titulo: "Grilla",
            nick: 'grilla',
            tags: ['animaciones']
        },
        {
            titulo: 'aceitunas_vs_bombas_paso_1',
            nick: 'aceitunas_vs_bombas_paso_1',
            tags: [],
        },
        {
            titulo: 'aceitunas_vs_bombas_paso_2',
            nick: 'aceitunas_vs_bombas_paso_2',
            tags: [],
        },
        {
            titulo: 'aceitunas_vs_bombas_paso_3',
            nick: 'aceitunas_vs_bombas_paso_3',
            tags: [],
        },
        {
            titulo: 'aceitunas_vs_bombas_paso_4',
            nick: 'aceitunas_vs_bombas_paso_4',
            tags: [],
        },
        {
            titulo: 'aceitunas_vs_bombas_paso_5',
            nick: 'aceitunas_vs_bombas_paso_5',
            tags: [],
        },
        {
            titulo: 'actor',
            nick: 'actor',
            tags: [],
        },
        {
            titulo: 'actor_personalizado',
            nick: 'actor_personalizado',
            tags: [],
        },
        {
            titulo: 'actor_personalizado_con_imagen_y_control',
            nick: 'actor_personalizado_con_imagen_y_control',
            tags: [],
        },
        {
            titulo: 'actores_arrastrables',
            nick: 'actores_arrastrables',
            tags: [],
        },
        {
            titulo: 'actores_simples',
            nick: 'actores_simples',
            tags: [],
        },
        {
            titulo: 'ancho_de_texto',
            nick: 'ancho_de_texto',
            tags: [],
        },
        {
            titulo: 'animacion_con_velocidad',
            nick: 'animacion_con_velocidad',
            tags: [],
        },
        {
            titulo: 'arrastrable',
            nick: 'arrastrable',
            tags: [],
        },
        {
            titulo: 'arrastrable_varios_z',
            nick: 'arrastrable_varios_z',
            tags: [],
        },
        {
            titulo: 'asteroides',
            nick: 'asteroides',
            tags: [],
        },
        {
            titulo: 'barra_de_energia',
            nick: 'barra_de_energia',
            tags: [],
        },
        {
            titulo: 'boton',
            nick: 'boton',
            tags: [],
        },
        {
            titulo: 'boton_con_texto',
            nick: 'boton_con_texto',
            tags: [],
        },
        {
            titulo: 'camara',
            nick: 'camara',
            tags: [],
        },
        {
            titulo: 'colisiones',
            nick: 'colisiones',
            tags: [],
        },
        {
            titulo: 'colisiones_fisicas',
            nick: 'colisiones_fisicas',
            tags: [],
        },
        {
            titulo: 'colores',
            nick: 'colores',
            tags: [],
        },
        {
            titulo: 'comportamientos_movimiento_de_mono',
            nick: 'comportamientos_movimiento_de_mono',
            tags: [],
        },
        {
            titulo: 'control_personalizado',
            nick: 'control_personalizado',
            tags: [],
        },
        {
            titulo: 'cuerda_fisicas',
            nick: 'cuerda_fisicas',
            tags: [],
        },
        {
            titulo: 'deslizador',
            nick: 'deslizador',
            tags: [],
        },
        {
            titulo: 'desplazamiento',
            nick: 'desplazamiento',
            tags: [],
        },
        {
            titulo: 'dialogo',
            nick: 'dialogo',
            tags: [],
        },
        {
            titulo: 'dialogo_con_botones',
            nick: 'dialogo_con_botones',
            tags: [],
        },
        {
            titulo: 'dialogo_con_funciones',
            nick: 'dialogo_con_funciones',
            tags: [],
        },
        {
            titulo: 'dialogo_con_preguntas',
            nick: 'dialogo_con_preguntas',
            tags: [],
        },
        {
            titulo: 'disparar_a_monos',
            nick: 'disparar_a_monos',
            tags: [],
        },
        {
            titulo: 'disparo',
            nick: 'disparo',
            tags: [],
        },
        {
            titulo: 'duplicar',
            nick: 'duplicar',
            tags: [],
        },
        {
            titulo: 'ejemplo_global',
            nick: 'ejemplo_global',
            tags: [],
        },
        {
            titulo: 'ejemplo_piezas',
            nick: 'ejemplo_piezas',
            tags: [],
        },
        {
            titulo: 'ejemplo_temporizador',
            nick: 'ejemplo_temporizador',
            tags: [],
        },
        {
            titulo: 'escenas_apiladas',
            nick: 'escenas_apiladas',
            tags: [],
        },
        {
            titulo: 'escenas_con_menu',
            nick: 'escenas_con_menu',
            tags: [],
        },
        {
            titulo: 'fondo',
            nick: 'fondo',
            tags: [],
        },
        {
            titulo: 'globo_simple',
            nick: 'globo_simple',
            tags: [],
        },
        {
            titulo: 'grilla',
            nick: 'grilla',
            tags: [],
        },
        {
            titulo: 'grupos_y_colisiones',
            nick: 'grupos_y_colisiones',
            tags: [],
        },
        {
            titulo: 'habilidad_personalizada',
            nick: 'habilidad_personalizada',
            tags: [],
        },
        {
            titulo: 'habilidad_personalizada_con_argumentos',
            nick: 'habilidad_personalizada_con_argumentos',
            tags: [],
        },
        {
            titulo: 'ingreso_de_texto_y_selector',
            nick: 'ingreso_de_texto_y_selector',
            tags: [],
        },
        {
            titulo: 'interpolacion',
            nick: 'interpolacion',
            tags: [],
        },
        {
            titulo: 'interpolaciones',
            nick: 'interpolaciones',
            tags: [],
        },
        {
            titulo: 'lista_seleccion',
            nick: 'lista_seleccion',
            tags: [],
        },
        {
            titulo: 'log',
            nick: 'log',
            tags: [],
        },
        {
            titulo: 'mapa_desde_archivo',
            nick: 'mapa_desde_archivo',
            tags: [],
        },
        {
            titulo: 'mapa_personaje_martian',
            nick: 'mapa_personaje_martian',
            tags: [],
        },
        {
            titulo: 'mapa_plataformas',
            nick: 'mapa_plataformas',
            tags: [],
        },
        {
            titulo: 'mapas',
            nick: 'mapas',
            tags: [],
        },
        {
            titulo: 'memorice',
            nick: 'memorice',
            tags: [],
        },
        {
            titulo: 'menu',
            nick: 'menu',
            tags: [],
        },
        {
            titulo: 'monitos_que_disparan',
            nick: 'monitos_que_disparan',
            tags: [],
        },
        {
            titulo: 'mover_actor_por_eventos',
            nick: 'mover_actor_por_eventos',
            tags: [],
        },
        {
            titulo: 'moverse_con_el_teclado',
            nick: 'moverse_con_el_teclado',
            tags: [],
        },
        {
            titulo: 'muchos_actores',
            nick: 'muchos_actores',
            tags: [],
        },
        {
            titulo: 'pacman_simple',
            nick: 'pacman_simple',
            tags: [],
        },
        {
            titulo: 'pingu_controlado_por_teclado',
            nick: 'pingu_controlado_por_teclado',
            tags: [],
        },
        {
            titulo: 'pizarra',
            nick: 'pizarra',
            tags: [],
        },
        {
            titulo: 'pizarra_actores_conectados_por_linea',
            nick: 'pizarra_actores_conectados_por_linea',
            tags: [],
        },
        {
            titulo: 'pizarra_dibuja_grilla',
            nick: 'pizarra_dibuja_grilla',
            tags: [],
        },
        {
            titulo: 'pizarra_dibuja_imagen',
            nick: 'pizarra_dibuja_imagen',
            tags: [],
        },
        {
            titulo: 'pizarra_dibuja_triangulo',
            nick: 'pizarra_dibuja_triangulo',
            tags: [],
        },
        {
            titulo: 'pizarra_dibujando_con_el_mouse',
            nick: 'pizarra_dibujando_con_el_mouse',
            tags: [],
        },
        {
            titulo: 'puntaje',
            nick: 'puntaje',
            tags: [],
        },
        {
            titulo: 'punto_de_control',
            nick: 'punto_de_control',
            tags: [],
        },
        {
            titulo: 'reloj',
            nick: 'reloj',
            tags: [],
        },
        {
            titulo: 'seguir_clicks',
            nick: 'seguir_clicks',
            tags: [],
        },
        {
            titulo: 'selector',
            nick: 'selector',
            tags: [],
        },
        {
            titulo: 'sonidos',
            nick: 'sonidos',
            tags: [],
        },
        {
            titulo: 'tareas',
            nick: 'tareas',
            tags: [],
        },
        {
            titulo: 'test_ejes',
            nick: 'test_ejes',
            tags: [],
        },
        {
            titulo: 'test_explosion',
            nick: 'test_explosion',
            tags: [],
        },
        {
            titulo: 'texto',
            nick: 'texto',
            tags: [],
        },
        {
            titulo: 'texto_personalizado',
            nick: 'texto_personalizado',
            tags: [],
        },
        {
            titulo: 'texto_que_cambia',
            nick: 'texto_que_cambia',
            tags: [],
        },
        {
            titulo: 'transparencia',
            nick: 'transparencia',
            tags: [],
        },
        {
            titulo: 'tres_en_raya',
            nick: 'tres_en_raya',
            tags: [],
        },
        {
            titulo: 'vaca_voladora',
            nick: 'vaca_voladora',
            tags: [],
        },
    ];
});