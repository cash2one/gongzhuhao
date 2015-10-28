'use strict';

angular.module('zenmezApp')
  .controller('HomeCtrl', function($scope, Menus, UserInfo) {
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
      .state('home', {
        url: '/home',
        templateUrl: "views/home/home.tpl.html",
        controller: 'HomeCtrl'
      });


  });