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

app.controller("MainCtrl", function($scope, $location){
});

app.controller("PrincipalCtrl", function($scope, $location){
});

app.controller("EjemplosCtrl", function($scope, $location){
    $scope.data = {};

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
    ];
});