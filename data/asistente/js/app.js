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
            titulo: "Personaje Animado Pixelart",
            nick: 'pixel_player_animado',
            tags: ['animacion', 'personalizado', 'pixelart']
        },

        {
            titulo: "Particulas de humo",
            nick: 'particulas_humo',
            tags: ['efectos', 'particulas']
        },
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
            titulo: 'aceitunas vs bombas paso 1',
            nick: 'aceitunas_vs_bombas_paso_1',
            tags: [],
        },
        {
            titulo: 'aceitunas vs bombas paso 2',
            nick: 'aceitunas_vs_bombas_paso_2',
            tags: [],
        },
        {
            titulo: 'aceitunas vs bombas paso 3',
            nick: 'aceitunas_vs_bombas_paso_3',
            tags: [],
        },
        {
            titulo: 'aceitunas vs bombas paso 4',
            nick: 'aceitunas_vs_bombas_paso_4',
            tags: [],
        },
        {
            titulo: 'aceitunas vs bombas paso 5',
            nick: 'aceitunas_vs_bombas_paso_5',
            tags: [],
        },
        {
            titulo: 'actor',
            nick: 'actor',
            tags: [],
        },
        {
            titulo: 'actor personalizado',
            nick: 'actor_personalizado',
            tags: [],
        },
        {
            titulo: 'actor personalizado con imagen y control',
            nick: 'actor_personalizado_con_imagen_y_control',
            tags: [],
        },
        {
            titulo: 'actores arrastrables',
            nick: 'actores_arrastrables',
            tags: [],
        },
        {
            titulo: 'actores simples',
            nick: 'actores_simples',
            tags: [],
        },
        {
            titulo: 'ancho de texto',
            nick: 'ancho_de_texto',
            tags: [],
        },
        {
            titulo: 'animacion con velocidad',
            nick: 'animacion_con_velocidad',
            tags: [],
        },
        {
            titulo: 'arrastrable',
            nick: 'arrastrable',
            tags: [],
        },
        {
            titulo: 'arrastrable varios z',
            nick: 'arrastrable_varios_z',
            tags: [],
        },
        {
            titulo: 'asteroides',
            nick: 'asteroides',
            tags: [],
        },
        {
            titulo: 'barra de energia',
            nick: 'barra_de_energia',
            tags: [],
        },
        {
            titulo: 'boton',
            nick: 'boton',
            tags: [],
        },
        {
            titulo: 'boton con texto',
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
            titulo: 'colisiones fisicas',
            nick: 'colisiones_fisicas',
            tags: [],
        },
        {
            titulo: 'colores',
            nick: 'colores',
            tags: [],
        },
        {
            titulo: 'comportamientos movimiento de mono',
            nick: 'comportamientos_movimiento_de_mono',
            tags: [],
        },
        {
            titulo: 'control personalizado',
            nick: 'control_personalizado',
            tags: [],
        },
        {
            titulo: 'cuerda fisicas',
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
            titulo: 'dialogo con botones',
            nick: 'dialogo_con_botones',
            tags: [],
        },
        {
            titulo: 'dialogo con funciones',
            nick: 'dialogo_con_funciones',
            tags: [],
        },
        {
            titulo: 'dialogo con preguntas',
            nick: 'dialogo_con_preguntas',
            tags: [],
        },
        {
            titulo: 'disparar a monos',
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
            titulo: 'ejemplo global',
            nick: 'ejemplo_global',
            tags: [],
        },
        {
            titulo: 'ejemplo piezas',
            nick: 'ejemplo_piezas',
            tags: [],
        },
        {
            titulo: 'ejemplo temporizador',
            nick: 'ejemplo_temporizador',
            tags: [],
        },
        {
            titulo: 'escenas apiladas',
            nick: 'escenas_apiladas',
            tags: [],
        },
        {
            titulo: 'escenas con menu',
            nick: 'escenas_con_menu',
            tags: [],
        },
        {
            titulo: 'fondo',
            nick: 'fondo',
            tags: [],
        },
        {
            titulo: 'globo simple',
            nick: 'globo_simple',
            tags: [],
        },
        {
            titulo: 'grilla',
            nick: 'grilla',
            tags: [],
        },
        {
            titulo: 'grupos y colisiones',
            nick: 'grupos_y_colisiones',
            tags: [],
        },
        {
            titulo: 'habilidad personalizada',
            nick: 'habilidad_personalizada',
            tags: [],
        },
        {
            titulo: 'habilidad personalizada con argumentos',
            nick: 'habilidad_personalizada_con_argumentos',
            tags: [],
        },
        {
            titulo: 'ingreso de texto y selector',
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
            titulo: 'lista seleccion',
            nick: 'lista_seleccion',
            tags: [],
        },
        {
            titulo: 'log',
            nick: 'log',
            tags: [],
        },
        {
            titulo: 'mapa desde archivo',
            nick: 'mapa_desde_archivo',
            tags: [],
        },
        {
            titulo: 'mapa personaje martian',
            nick: 'mapa_personaje_martian',
            tags: [],
        },
        {
            titulo: 'mapa plataformas',
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
            titulo: 'monitos que disparan',
            nick: 'monitos_que_disparan',
            tags: [],
        },
        {
            titulo: 'mover actor por eventos',
            nick: 'mover_actor_por_eventos',
            tags: [],
        },
        {
            titulo: 'moverse con el teclado',
            nick: 'moverse_con_el_teclado',
            tags: [],
        },
        {
            titulo: 'muchos actores',
            nick: 'muchos_actores',
            tags: [],
        },
        {
            titulo: 'pacman simple',
            nick: 'pacman_simple',
            tags: [],
        },
        {
            titulo: 'pingu controlado por teclado',
            nick: 'pingu_controlado_por_teclado',
            tags: [],
        },
        {
            titulo: 'pizarra',
            nick: 'pizarra',
            tags: [],
        },
        {
            titulo: 'pizarra actores conectados por linea',
            nick: 'pizarra_actores_conectados_por_linea',
            tags: [],
        },
        {
            titulo: 'pizarra dibuja grilla',
            nick: 'pizarra_dibuja_grilla',
            tags: [],
        },
        {
            titulo: 'pizarra dibuja imagen',
            nick: 'pizarra_dibuja_imagen',
            tags: [],
        },
        {
            titulo: 'pizarra dibuja triangulo',
            nick: 'pizarra_dibuja_triangulo',
            tags: [],
        },
        {
            titulo: 'pizarra dibujando con el mouse',
            nick: 'pizarra_dibujando_con_el_mouse',
            tags: [],
        },
        {
            titulo: 'puntaje',
            nick: 'puntaje',
            tags: [],
        },
        {
            titulo: 'punto de control',
            nick: 'punto_de_control',
            tags: [],
        },
        {
            titulo: 'reloj',
            nick: 'reloj',
            tags: [],
        },
        {
            titulo: 'seguir clicks',
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
            titulo: 'test ejes',
            nick: 'test_ejes',
            tags: [],
        },
        {
            titulo: 'test explosion',
            nick: 'test_explosion',
            tags: [],
        },
        {
            titulo: 'texto',
            nick: 'texto',
            tags: [],
        },
        {
            titulo: 'texto personalizado',
            nick: 'texto_personalizado',
            tags: [],
        },
        {
            titulo: 'texto que cambia',
            nick: 'texto_que_cambia',
            tags: [],
        },
        {
            titulo: 'transparencia',
            nick: 'transparencia',
            tags: [],
        },
        {
            titulo: 'tres en raya',
            nick: 'tres_en_raya',
            tags: [],
        },
        {
            titulo: 'vaca voladora',
            nick: 'vaca_voladora',
            tags: [],
        },
    ];
});
