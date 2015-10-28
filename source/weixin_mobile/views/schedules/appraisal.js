'use strict';

angular.module('zenmezApp')
  .controller('SchedulesAppraisalCtrl', function ($scope, $state, $location, $http, $stateParams , $window , FileUploader) {
    $scope.model = {};
    $scope.has_dsiabled = false;
    $scope.hasDoubelRating = ($stateParams.schedule_type_id == "1");
    var evaluation_category_id;
    var serviceBase = "/mobile/create/evaluation/category/"+$stateParams.order_id+"/"+$stateParams.schedule_type_id+"/";
    var promise = $http.get(serviceBase);

    var uploader = $scope.uploader = new FileUploader({
            url: serviceBase,
            alias : 'image'
        });

    uploader.onCompleteAll = function(data){
      uploader.clearQueue();
      $scope.has_dsiabled = false;
      $location.path('/schedules');
    };

    $scope.onTriggerClick = function(){
      $('#file_post').trigger('click');
    };


    promise.success(function(data){
      $scope.model.evaluation_category_name = data.evaluation_category_name;
      $scope.model.evaluation_category_name_2 = data.evaluation_category_name_2;
      evaluation_category_id = data.evaluation_category_id;
      if(data.code == 1){
        $scope.model.score = data.star;
        $scope.model.content = data.content;
        if(data.shot_star){
          $scope.model.score = data.shot_star;
          $scope.model.score_2 = data.dressing_star;
        }
      }
    });

    promise.error(function(data, state){
      console.log("error");
    });

    $scope.model.score = 5;
    $scope.model.score_2 = 5;

    $scope.onUpdateRating = function(index){
       $scope.model.score = index;
    };

    $scope.onUpdateRating_2 = function(index){
      $scope.model.score_2 = index;
    };

    $scope.onSave = function(info){
       var obj = {};
       $scope.has_dsiabled = true;
       obj.Fscore = info.score;
      if($scope.hasDoubelRating){
        obj.Fscore = info.score + "&" + info.score_2;
      }
      obj.Fcontent = info.content;
      var p = $http.post(serviceBase , obj) ;


      p.success(function(rs){
        if(rs.stat == "1000"){
          var url = "/mobile/create/evaluation/image/" + rs.data;
          if(uploader.queue.length == 0){
            $scope.has_dsiabled = false;
            $location.path('/schedules');
            return;
          }else{
            var path= "/mobile/delete/evaluation/image/" + rs.data;
            $http.get(path);
          }
        }

        angular.forEach(uploader.queue, function(item) {
            item.url = url;
        });
        setTimeout(function(){uploader.uploadAll()} , 500);
      });
    }

  })
  .config(function($stateProvider) {
  $stateProvider
    .state('appraisal', {
      url: "/appraisal/:order_id/:schedule_type_id",
      templateUrl: "views/schedules/appraisal.tpl.html",
      controller : 'SchedulesAppraisalCtrl'
    });
});
