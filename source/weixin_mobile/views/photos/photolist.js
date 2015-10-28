'use strict';

angular.module('zenmezApp')
  .controller('PhotoListCtrl', function ($scope, $http , $location, $stateParams , $window) {
  	$scope.model = {};
    var promise = $http.get("/mobile/user/album/list/"+$stateParams.id+"/");
    promise.success(function(data ,state ){
      $scope.model.photolist = data;
    });

    promise.error(function(data , state){
      console.log("error");
    });

    $scope.onShare = function(e){
      $location.url('/photoshare/'+$stateParams.id); 
      };
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.photolist', {
	    url: "/photolist/:id",
      // templateUrl: "/static/views/photos/photolist.tpl.html",
      // controller : 'PhotoListCtrl'
	    views: {
	      'menuContent': {
	        templateUrl: "views/photos/photolist.tpl.html",
	        controller : 'PhotoListCtrl'
	      }
	    }
	  });
});
