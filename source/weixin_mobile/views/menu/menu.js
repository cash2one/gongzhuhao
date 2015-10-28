'use strict';

angular.module('zenmezApp')
  .controller('MenuCtrl', function($scope, $state, Menus, UserInfo) {
    $scope.$state = $state;
    $scope.model = {};
    UserInfo.getUserInfo().then(function(userInfo) {
      $scope.chats = Menus.all();
      $scope.model.user_name = userInfo.data.nick_name;
      $scope.model.user_mobi = userInfo.data.user_mobi;
      $scope.model.user_avatar = userInfo.data.head_photo_url;
    });
  })
  .config(function($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('zenmez', {
        abstract: true,
        templateUrl: 'views/menu/menu.tpl.html',
        controller: 'MenuCtrl',
        resolve: {
          // 'login': function(loginService, $q, $http) {
          //     var roleDefined = $q.defer();
          //     if (loginService.pendingStateChange) {
          //         return loginService.resolvePendingState($http.get('/user'));
          //     } else {
          //         roleDefined.resolve();
          //     }
          //     return roleDefined.promise;
          // }
        }
      });
  });