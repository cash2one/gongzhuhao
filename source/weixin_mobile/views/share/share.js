'use strict';

angular.module('zenmezApp')
  .controller('ShareCtrl', function ($scope, $state, $http , $stateParams) {
  	$scope.model = {};
  	function fetchData(){
      var promise = $http.get("/weixin/user/share/");

      promise.success(function(data ,state ){
        $scope.model.share = data;
      });

      promise.error(function(data ,state ){
        console.log("error");
      });
    };

    $scope.$on('$ionicView.beforeEnter' , function(e){
      fetchData();
    });

  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.share', {
	    url: "/share",
	    views: {
	      'menuContent': {
	        templateUrl: "views/share/share.tpl.html",
	        controller : 'ShareCtrl'
	      }
	    }
	  });
});
  