'use strict';

angular.module('zenmezApp')
  .controller('PhotosCtrl', function ($scope,$http) {
  	$scope.model = {};
    var promise = $http.get("/weixin/user/photos/");
    promise.success(function(data ,state ){
      $scope.model.photos = data;
    });

    promise.error(function(data , state){
      console.log("error");
    });
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.photos', {
	    url: "/photos",
	    views: {
	      'menuContent': {
	        templateUrl: "views/photos/photos.tpl.html",
	        controller : 'PhotosCtrl'
	      }
	    }
	  });
});
