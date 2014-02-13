app = angular.module('app', ['ngRoute', 'ngAnimate', 'ui.bootstrap']);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider.
          when('/index', {
            templateUrl: 'partials/tutoriales.html'
          }).
            when('/tutoriales/caminos', {
              templateUrl: 'partials/tutoriales/caminos.html'
            }).
            when('/tutoriales/nave', {
              templateUrl: 'partials/tutoriales/nave.html'
            }).
            when('/tutoriales/fisica', {
              templateUrl: 'partials/tutoriales/fisica.html'
            }).
					otherwise({redirectTo:'/index'});
}]);

$(function(){
    var rx = /INPUT|SPAN|SELECT|TEXTAREA/i;

    $(document).bind("keydown keypress", function(e) {
        if (e.which == 8) {
            if (!rx.test(e.target.tagName) || e.target.disabled || e.target.readOnly) {
                e.preventDefault();
            }
        }
    });
});


app.controller("MainCtrl", function($scope) {
});