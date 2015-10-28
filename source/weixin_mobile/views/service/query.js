'use strict';

angular.module('zenmezApp')
  .controller('ServiceQueryCtrl', function ($scope, $http , $state , $location , $filter) {
  	$scope.model = {};
  	var promise = $http.get("/mobile/order/query_schedule/");
  	promise.success(function(data ,state ){
  	  $scope.model.selected = data.list[0];
      $scope.model.query = data;
      $scope.model.start_date = new Date(data.data.start_date);
      $scope.model.end_date = new Date(data.data.end_date);
  	});

  	promise.error(function(data ,state ){
  		console.log("error");
  	});

    $scope.$watch("model.selected" , function(item){
      if(item){
        $scope.model.selected = item;
      }
    });

    $scope.goList = function() {
       var path = [];
       path.push("/list/");
       path.push($scope.model.selected.id + "/");
       path.push($filter('date')($scope.model.start_date , 'yyyy-MM-dd') + "/");
       path.push($filter('date')($scope.model.end_date , 'yyyy-MM-dd'));
      $location.url(path.join("")); 
    };
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.query', {
	    url: "/query",
	    views: {
	      'menuContent': {
	        templateUrl: "views/service/query.tpl.html",
	        controller : 'ServiceQueryCtrl'
	      }
	    }
	  });
});
