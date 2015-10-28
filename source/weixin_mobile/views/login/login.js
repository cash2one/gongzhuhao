'use strict';

angular.module('zenmezApp')
  .controller('LoginCtrl', function($scope ,$state ,$location) {
    $scope.loginData = {};
    $scope.doLogin = function() {
      $location.url('/home'); 
    };

  })
  .config(function($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('login', {
        url: '/login',
        templateUrl: "views/login/login.tpl.html",
        controller: 'LoginCtrl'                
      });
  });