'use strict';

angular.module('zenmezApp')
  .controller('SchedulesItemCtrl', function($scope, $state ,$http , $stateParams) {
    $scope.model = {};
    $scope.model.order_id = $stateParams.id;
    //console.log(Order);
    //$scope.model.order = Order.query();

    var promise = $http.get("/mobile/schedule/list/"+$stateParams.id+"/");
    promise.success(function(data ,state ){
      $scope.model.schedule = data;
    });

    promise.error(function(data , state){
      console.log("error");
    });
  })
  .config(function($stateProvider) {
    $stateProvider
      .state('zenmez.items', {
        url: "/items/:id",
        views: {
          'menuContent': {
            templateUrl: "views/schedules/items.tpl.html",
            controller: 'SchedulesItemCtrl'
          }
        }
      });
  });
