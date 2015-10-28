'use strict';

angular.module('zenmezApp')
  .controller('ServiceCtrl', function ($scope , $http , $state , $location) {
  	$scope.model = {};
    function fetchData(){
      var promise = $http.get("/mobile/merchant/service/");
      promise.success(function(data ,state ){
        $scope.model.service = data;
      });

      promise.error(function(data ,state ){
        console.log("error");
      });
    };

    $scope.$on('$ionicView.beforeEnter' , function(){
      fetchData();
    });

  	$scope.onAddOrder = function(e){
  		$location.url("/query");
  	};
    $scope.onSkipOrder = function(e){
      $location.path("/orderadd");
    };
    
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.service', {
	    url: "/service",
	    views: {
	      'menuContent': {
	        templateUrl: "views/service/service.tpl.html",
	        controller : 'ServiceCtrl'
	      }
	    }
	  });
});
