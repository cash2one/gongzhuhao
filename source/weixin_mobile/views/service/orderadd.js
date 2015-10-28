'use strict';

angular.module('zenmezApp')
  .controller('OrderAddCtrl', function ($scope , $http , $state ,$stateParams, $location , Order , $window) {
  	$scope.model = {};
    $scope.model.hasClientType = false;
    var serviceBase = "/mobile/merchant/orders/add/1/"
  	var promise = $http.get(serviceBase);
  	promise.success(function(data, status, headers, config ){
      var order_type = data.list[0]
      $scope.model.results = data;
      $scope.model.order_type = order_type;
      $scope.model.order_type_id = order_type.order_type_id;
  	});

  	promise.error(function(data, status, headers, config ){
  		console.log("error");
  	});

    $scope.$watch("model.order_type" , function(item){
      if(item){
        $scope.model.order_type_id = item.order_type_id;
      }
      if(item && item.order_type_id == 1){
        $scope.model.hasClientType = true;
      }else{
        $scope.model.hasClientType = false;
      }
    });

    $scope.onSave = function(order){
      order.order_type = order.order_type.order_type_id;
      var p = $http.post(serviceBase ,order);
      p.then(function(data){
        $location.path("/service");
      });
    }
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.orderadd', {
	    url: "/orderadd",
	    views: {
	      'menuContent': {
	        templateUrl: "views/service/orderadd.tpl.html",
	        controller : 'OrderAddCtrl'
	      }
	    }
	  });
});
