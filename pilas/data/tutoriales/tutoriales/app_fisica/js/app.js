var app = angular.module('app', ['ngRoute', 'ngAnimate']);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
  	when('/',  {templateUrl: 'partials/paso1.html', controller: 'Paso1Ctrl'}).
  	when('/2', {templateUrl: 'partials/paso2.html', controller: 'Paso2Ctrl'}).
  	when('/3', {templateUrl: 'partials/paso3.html', controller: 'Paso3Ctrl'}).
  	when('/4', {templateUrl: 'partials/paso4.html', controller: 'Paso4Ctrl'}).
  	when('/5', {templateUrl: 'partials/paso5.html', controller: 'Paso5Ctrl'}).
  	when('/6', {templateUrl: 'partials/paso6.html', controller: 'Paso6Ctrl'}).
  	when('/7', {templateUrl: 'partials/paso7.html', controller: 'Paso7Ctrl'}).
    when('/8', {templateUrl: 'partials/paso8.html', controller: 'Paso8Ctrl'}).
    when('/9', {templateUrl: 'partials/paso9.html', controller: 'Paso9Ctrl'}).
  	otherwise({redirectTo: '/'});
}]);


function sumar_consigna($scope, texto) {
  for (var i=0; i<$scope.consignas.length; i++)
    $scope.consignas[i].completa = true;
  $scope.consignas.push({completa: false, texto: texto});
}


app.controller('TutorialCtrl', ['$scope', '$location', function($scope, $location) {
  $scope.mostrar_mensaje = false;
  $scope.mensaje = "";
  
  $scope.ocultar_mensajes = function() {
  	$scope.mostrar_mensaje = false;
  }
  
  function es_actual() {
    var path_del_ejercicio = "/" + this.path;
    var path_actual = $location.path();
    return (path_actual == path_del_ejercicio);
  }
  
  $scope.ejercicios = [
    {numero: 1, completado: false, path:  '', es_actual: es_actual},
    {numero: 2, completado: false, path: '2', es_actual: es_actual},
    {numero: 3, completado: false, path: '3', es_actual: es_actual},
    {numero: 4, completado: false, path: '4', es_actual: es_actual},
    {numero: 5, completado: false, path: '5', es_actual: es_actual},
    {numero: 6, completado: false, path: '6', es_actual: es_actual},
    {numero: 7, completado: false, path: '7', es_actual: es_actual},
    {numero: 8, completado: false, path: '8', es_actual: es_actual},
    {numero: 9, completado: false, path: '9', es_actual: es_actual},
  ];
    
   /* La funcion "cuando_ejecuta" contiene el callback que se va
      a llamar cada vez que el usuario escriba dentro de la consola.
      
      El argumento que recibe es la salida por pantalla (en formato string).
      
      Este callback va a ser sobre-escrito por cada controller. Así cada
      consigna del tutorial hacer sus propias validaciones y flujo de
      programa.
    */
   $scope.cuando_ejecuta = function(datos) {
   };
    
}]);

app.controller('Paso1Ctrl', ['$scope', '$location', function($scope, $location) {

  window.crear_pelota = function() {
    window.pelota = new pilas.actores.Pelota();
    return "creando pelota ...";
  }
  
  $scope.$parent.cuando_ejecuta = function(dato) {

    if (dato == "creando pelota ...") {
      $location.path('/2');
      $scope.$parent.ejercicios[0]['completado'] = true;
    } 
  }
  
}]);
    
app.controller('Paso2Ctrl', ['$scope', '$location', function($scope, $location) {
  
  $scope.comenzar_tutorial = function() {
  	$location.path('/3');
    $scope.$parent.ejercicios[1]['completado'] = true;
  }
  
  $scope.$parent.cuando_ejecuta = function(dato) {
  }
  
}]);





app.controller('Paso3Ctrl', ['$scope', '$location', function($scope, $location) {
  var numero=0;

  pelota.saltar = function() {
    pelota.empujar(0, 15);
    return "saltando ...";
  }

  pelota.saludar = function() {
    pelota.decir("hola !!!");
    return "saludando ...";
  }
  
  $scope.consignas = [
    {completa: false, texto: "Escribí pelota.saltar()"},
  ];
    
  
  $scope.$parent.cuando_ejecuta = function(data) {

    if (numero==0 && data == "saltando ...") {
    	sumar_consigna($scope, "Escribí pelota.saludar()");
      numero=1;
    }
                             
    if (numero==1 && data == "saludando ...") {
    	sumar_consigna($scope, "Escribí pelota.empujar(10, 5)");
      numero=2;
    }
                             
    if (numero==2 && data == "empujando hacia (10, 5) ...") {
      $location.path('/4');
      $scope.$parent.ejercicios[2]['completado'] = true;
    }
  }
  
}]);

app.controller('Paso4Ctrl', ['$scope', '$location', function($scope, $location) {


  $scope.$parent.cuando_ejecuta = function(dato) {

    if (/empujando/.test(dato)) {
      $location.path('/5');
      $scope.$parent.ejercicios[3]['completado'] = true;
    }

  }
  
}]);
  
app.controller('Paso5Ctrl', ['$scope', '$location', function($scope, $location) {
  window.crear_cesto = function() {
    window.cesto =  new pilas.actores.Cesto();
    return "creando cesto ...";
  }

  $scope.$parent.cuando_ejecuta = function(dato) {

    if (dato == 0.75) {
      $location.path('/6');
      $scope.$parent.ejercicios[4]['completado'] = true;
    }
  }

}]);

app.controller('Paso6Ctrl', ['$scope', '$location', function($scope, $location) {
  $scope.consignas = [
  {completa: false, texto: "Escribí pilas.mostrar_fisica() para ver las colisiones."},
  ];

  $scope.$parent.cuando_ejecuta = function(dato) {

    if (dato == "Mostrando fisica") {
      $scope.mostrar_extras = true;
      $scope.consignas[0].completa = true;

    }

    $scope.avanzar = function() {
  	  $location.path('/7');
      $scope.$parent.ejercicios[5]['completado'] = true;
    }

  }
    
}]);
    
app.controller('Paso7Ctrl', ['$scope', '$location', function($scope, $location) {
  var numero=0;

  $scope.consignas = [
    {completa: false, texto: "Escribí la siguiente línea de código: pelota.aprender(pilas.habilidades.Arrastrable)"},
  ];

  $scope.$parent.cuando_ejecuta = function(dato) {

    if (dato == "Enseñando una habilidad ...") {
      $scope.mostrar_extras = true;
      $scope.consignas[0].completa = true;
    }

    $scope.avanzar = function() {
  	  $location.path('/8');
      $scope.$parent.ejercicios[6]['completado'] = true;
    }

  }


}]);

app.controller('Paso8Ctrl', ['$scope', '$location', function($scope, $location) {
  window.avanzar = function() {return "ok"};

  window.caja = new pilas.actores.Caja();
  window.caja.y = 100;
  window.caja.aprender(pilas.habilidades.RebotarComoCaja);
  window.aceituna = new pilas.actores.Aceituna();
  window.aceituna.x = -1;
  window.aceituna.aprender(pilas.habilidades.RebotarComoPelota);

  pilas.definir_gravedad = function(x, y) {
    var escena = pilas.escena_actual();
    escena.fisica.definir_gravedad(x + 0.1, -y + 0.1);
    return "Cambiando gravedad del escenario ...";
  }

  $scope.$parent.cuando_ejecuta = function(dato) {

    if (dato == "ok") {
      $location.path('/9');
      $scope.$parent.ejercicios[7]['completado'] = true;
    }

  }

}]);


app.controller('Paso9Ctrl', ['$scope', '$location', function($scope, $location) {
  /* Link a pilas */
}]);

app.directive('pilasInterprete', function() {
  return {
    restrict: 'E',
    replace: true,
    transclude: true,
    link: function (scope, elem, attrs) {
    
      var exec = document.getElementById('exec');
      /* Se conecta al evento de impresion de pantalla que emite la consola.
         Cuando llega esta senal intenta conectarla con el callback de la
         directiva.
         
         Todo esto se evalua en el contexto del scope. */
      elem[0].addEventListener('salida', function (e) {
        var funcion = attrs.evaluador.replace("()", "('" + e.texto + "')");
      	scope.$eval(funcion);
        scope.$apply();
      }, false);
      
			iniciar_jsconsole();
    },
    template: '<div id="consola" class="stretch console">' + 
       	'<div id="console" class="stretch">' +
        ' <ul id="output"></ul>' +
        '  <form>' + 
        '   <textarea autofocus id="exec" spellcheck="false" autocapitalize="off" rows="1" autocorrect="off"></textarea>' +
        '  </form>' +
      	' </div>' +
        '</div>',
  }
});
  
app.directive('pilasCanvas', function() {
  return {
    restrict: 'E',
    replace: true,
    transclude: true,
    link: function (scope, elem, attrs) {
    pilas = new Pilas();
	  pilas.iniciar({ancho: 320, alto: 240, data_path: '../../data'});
      
    pilas.onready = function() {
  		var fondo = new pilas.fondos.Tarde();
	  }

	  pilas.ejecutar();
    },
    template: '<div class="centrado">' + 
    		  '<canvas id="canvas"></canvas>' +
    		  '</div>'
  }
});
