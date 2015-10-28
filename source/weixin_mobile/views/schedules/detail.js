'use strict';

angular.module('zenmezApp')
  .controller('SchedulesDetailCtrl', function($scope, $state, $location, $http, $stateParams) {
    $scope.model = {};
    $scope.model.order_id = $stateParams.order_id;
    $scope.model.schedule_type_id = $stateParams.schedule_type_id;
    var promise = $http.get("/mobile/schedule/detail/"+$stateParams.order_id+"/"+$stateParams.schedule_type_id+"/");
    promise.success(function(data ,state ){
      $scope.model.detail = data;
    });

    promise.error(function(data , state){
      console.log("error");
    });

    $scope.addAppraisal = function(e){
      var _url = $location.url("/appraisal/" + $stateParams.order_id + '/' + $stateParams.schedule_type_id);
    }
  })

  .config(function($stateProvider, $urlRouterProvider) {
    $stateProvider
      .state('detail', {
        url: "/detail/:order_id/:schedule_type_id",
        templateUrl: "views/schedules/detail.tpl.html",
        controller: 'SchedulesDetailCtrl'
      });
  });
