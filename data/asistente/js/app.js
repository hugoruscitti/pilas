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
            titulo: "Animacion con velocidad",
            nick: 'animacion_con_velocidad',
            tags: ['animaciones', 'velocidad']
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
    ];
});