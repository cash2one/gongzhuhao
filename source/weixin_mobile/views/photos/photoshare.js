'use strict';

angular.module('zenmezApp')
  .controller('PhotosShareCtrl', function ($scope,$http ,$stateParams , $location , $window) {
    $scope.share = {};
    $scope.has_dsiabled = false;
    function fetchData(){
      var promise = $http.get("/mobile/user/create/share/" + $stateParams.id + '/');
      promise.success(function(data ,state ){
        $scope.list = data.list_music;
        $scope.list_music = data.list_music[0];
        $scope.share.title = data.title;
        $scope.share.description = data.description;
      });

      promise.error(function(data , state){
        console.log("error");
      });
    };

    $scope.$on('$ionicView.beforeEnter' , function(){
      fetchData();
    });

    $scope.$watch("list_music" , function(item){
      if(item){
        $scope.share.music_id = item.music_id;
        $scope.share.music_url = item.music_url;
        $scope.share.music_name = item.music_name;
      }
    });

    $scope.onSave = function(share){
      $scope.has_dsiabled = true;
      var promise = $http.post("/mobile/user/create/share/" + $stateParams.id + '/', share);
      promise.success(function(data, status, headers, config) {
        var state = data.stat;
        if (state == '1000') {
          $scope.has_dsiabled = false;
          $location.path("/share");
        } else {
          $scope.error = data.info;
        }
      });

      promise.error(function(data, status, headers, config) {
        $scope.has_dsiabled = false;
        $scope.error = "分享照片失败";
      });
    };

  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('photoshare', {
	    url: "/photoshare/:id",
      templateUrl: "views/photos/photoshare.tpl.html",
      controller : 'PhotosShareCtrl'
	  });
});
