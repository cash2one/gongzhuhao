'use strict';

 angular.module('zenmezApp', [
  'ionic',
  'tabSlideBox',
  'ng-mfb',
  'elif',
  'angularFileUpload',
  'templates',
  'gzh.filter.qqface'
]);

angular.module('zenmezApp')
  .run(function($ionicPlatform ,$rootScope , $http , $state , $resource) {
    $ionicPlatform.ready(function() {
      if (window.cordova && window.cordova.plugins.Keyboard) {
        cordova.plugins.Keyboard.hideKeyboardAccessoryBar(true);
      }
      if (window.StatusBar) {
        StatusBar.styleDefault();
      }
    });
  })
  .config(function($stateProvider, $urlRouterProvider , $provide , $compileProvider) {
    $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|ftp|weixin|file|mailto|chrome-extension):/)
    $urlRouterProvider.otherwise('/home');
  });
