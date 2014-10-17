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


app.directive('errSrc', function() {
  return {
    link: function(scope, element, attrs) {
      element.bind('error', function() {
        attrs.$set('src', "imagenes/ejemplos/inexistente.png");
      });
    }
  }
});


app.controller("MainCtrl", function($scope, $location, PanelVersionFactory) {
  $scope.data = {};
  $scope.data.version = DESCRIPCION_VERSION; // todo: se incluye de version.js

  $scope.data.consultar_panel_visible = PanelVersionFactory.consultar_panel_visible;
  $scope.alternar_panel_version = PanelVersionFactory.alternar_panel_version;
});

app.controller("PrincipalCtrl", function($scope, $location){
});

app.controller("EjemplosCtrl", function($scope, $location){
    $scope.data = {};


    $scope.abrir_ejemplo = function(nick) {
        window.interlocutor.abrir_ejemplo(nick);
    };


    var listado_plano = JSON.parse(window.interlocutor.obtener_ejemplos());
    $scope.data.ejemplos = [];

    for (var i in listado_plano.ejemplos) {
        var nombre = listado_plano.ejemplos[i];

        $scope.data.ejemplos.push({
            titulo: nombre.replace(/_/g, ' '),
            nick:  nombre,
            tags: []
        });
    }
});
