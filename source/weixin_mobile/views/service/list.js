'use strict';

angular.module('zenmezApp')
  .controller('ServiceListCtrl', function ($scope , $http , $state ,$stateParams, $location ) {
    $scope.model = {};
  	var promise = $http.post("/mobile/order/query_schedule/" , {
  		"start_date" : $stateParams.start_date,//$stateParams.start_date,
  		"end_date" :$stateParams.end_date, //$stateParams.end_date,
  		"category" : $stateParams.schedule_id
  	});

  	promise.success(function(data, status, headers, config ){
      $scope.model.list = data;
  	});

  	promise.error(function(data, status, headers, config ){
  		console.log("error");
  	});

  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.list', {
	    url: "/list/:schedule_id/:start_date/:end_date",
	    views: {
	      'menuContent': {
	        templateUrl: "views/service/list.tpl.html",
	        controller : 'ServiceListCtrl'
	      }
	    }
	  });
});
