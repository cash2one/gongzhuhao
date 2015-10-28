'use strict';

angular.module('zenmezApp')
  .controller('ServiceAddCtrl', function ($scope , $http , $state ,$stateParams, $location , Order , $window) {
  	$scope.model = {};
    $scope.model.schedule_category_name = $stateParams.schedule_category_name;
    $scope.model.date = $stateParams.date;
    $scope.model.hasClientType = false;
    $scope.model.schedule_category_id = $stateParams.id;
  	var promise = Order.getOrder($stateParams.id);
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
      Order.insertOrder(order).then(function(){
        $location.path("/service");
      });
    }
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.add', {
	    url: "/add/:id/:date/:schedule_category_name",
	    views: {
	      'menuContent': {
	        templateUrl: "views/service/add.tpl.html",
	        controller : 'ServiceAddCtrl'
	      }
	    }
	  });
});
