var app = angular.module('app', ['ngRoute', 'ngAnimate']);

app.config(['$routeProvider', function($routeProvider) {
  $routeProvider.
  	when('/',  {templateUrl: 'partials/paso1.html', controller: 'Paso1Ctrl'}).
  	when('/2', {templateUrl: 'partials/paso2.html', controller: 'Paso2Ctrl'}).
  	when('/3', {templateUrl: 'partials/paso3.html', controller: 'Paso3Ctrl'}).
  	when('/4', {templateUrl: 'partials/paso4.html', controller: 'Paso4Ctrl'}).
  	when('/5', {templateUrl: 'partials/paso5.html', controller: 'Paso5Ctrl'}).
  	when('/6', {templateUrl: 'partials/paso6.html', controller: 'Paso6Ctrl'}).
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
  
  $scope.$parent.cuando_ejecuta = function(dato) {
    if (dato == 4) {
      $location.path('/2');
      //$scope.$parent.mensaje = "Ejercicio 1 completado!";
      //$scope.$parent.mostrar_mensaje = true;
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
  
  $scope.consignas = [
    {completa: false, texto: "Escribí zack.saludar() para que nos diga algo."},
  ];
    
  
  $scope.$parent.cuando_ejecuta = function(data) {
      console.log(data);
    
    if (numero==0 && data == "saludando ...") {
    	sumar_consigna($scope, "¡Bien!, ahora zack.caminar_derecha(2)");
      numero=1;
    }
                             
    if (numero==1 && data == "caminando 2 pasos") {
      $location.path('/4');
      $scope.$parent.ejercicios[2]['completado'] = true;
    }
  }
  
}]);

app.controller('Paso4Ctrl', ['$scope', '$location', function($scope, $location) {
    var numero=0;
    var capturadas=0;

    var m1 = new pilas.actores.Manzana(40*3);
    var m2 = new pilas.actores.Manzana(-40*3, -60);
    var m3 = new pilas.actores.Manzana(20*3, 40);
    var m4 = new pilas.actores.Manzana(0, 100);

    var _scope = $scope;
    var _location = $location;

    window.setTimeout(function() {
      console.log("head");

      pilas.colisiones.agregar(window['zack'], [m1, m2, m3, m4], function(m, manzana) {
        manzana.eliminar();
        capturadas += 1;

        if (capturadas >= 4) {
          _location.path('/5');
          _scope.$parent.ejercicios[3]['completado'] = true;
          _scope.$apply();
          window['zack'].decir("genial!");
        }

      });
    }, 2000);
  
}]);
  
app.controller('Paso5Ctrl', ['$scope', '$location', function($scope, $location) {
  $scope.consignas = [
    {completa: false, texto: "Escribí zack.inspeccionar()"},
  ];

  $scope.$parent.cuando_ejecuta = function(dato) {

    if (/del actor/.test(dato)) {
    	sumar_consigna($scope, "¡Bien!, ahora zack.habilitar_teclado()");
    }

    if (dato == "Habilitando el teclado" || dato == "El teclado ya estaba habilitado.") {
      $scope.consignas[1].completa = true;
      $scope.$parent.ejercicios[4]['completado'] = true;
      $scope.$apply();
      $location.path('/6');
    }
  }

}]);

app.controller('Paso6Ctrl', ['$scope', '$location', function($scope, $location) {
  var globo_activo = false;
  var cofres_abiertos = 0;
  $scope.mostrar_final = false;

  /*
   * Hace que el actor diga algo pero evitando tener multiples
   * dialogos al mismo tiempo.
   */
  function decir(mensaje) {
    if (globo_activo === false) {
      zack.decir(mensaje);
      globo_activo = true;

      setTimeout(function() {
        globo_activo = false;
      }, 4000);
    }
  }

  setTimeout(function() {
    var cofre1 = new pilas.actores.Cofre(100, 0);
    var cofre2 = new pilas.actores.Cofre(-20*5, 40);

    var llave1 = new pilas.actores.Llave(40, 100);
    var llave2 = new pilas.actores.Llave(-60, -100);

    zack.tiene_llave = false;
    zack.habilitar_teclado();

    pilas.colisiones.agregar(window['zack'], [llave1, llave2], function(m, llave) {
      if (zack.tiene_llave != true) {
        zack.tiene_llave = true;
        llave.eliminar();
      } else {
        decir("ya tengo una llave");
      }
    });

    pilas.colisiones.agregar(window['zack'], [cofre1, cofre2], function(m, cofre) {

      if (cofre.esta_abierto == false) {
        if (m.tiene_llave) {
          cofre.abrir();
          m.tiene_llave = false;
          decir("¡bien!");
          cofres_abiertos += 1;

          if (cofres_abiertos >= 2) {
            $scope.mostrar_final = true;
            $scope.$apply();
          }

        } else {
          decir("no tengo llave ...");
        }
      }
      
    });

  }, 500);

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
        var fondo = new pilas.fondos.PastoCuadriculado();
        window.zack = new pilas.actores.Maton();
        window.zack.aprender(pilas.habilidades.SeMantieneEnPantalla)
	    }

	    pilas.ejecutar();
    },
    template: '<div class="centrado">' + 
    		  '<canvas id="canvas"></canvas>' +
    		  '</div>'
  }
});
