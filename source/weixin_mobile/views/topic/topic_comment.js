'use strict';

angular.module('zenmezApp')
  .controller('TopicCommentCtrl', function ($scope, $state, $http, $stateParams , $location) {
  	var pid = 1,
  		follow_id;

  	$scope.model = {};

  	$scope.initialize = function(item){
  		$scope.comment = item;
  		follow_id = item.Fid;
      if(item.has_count){
        fetchData();
      }
  	};

  	function fetchData(){
      var path = "/mobile/topics/reply/"+follow_id+"/"+pid;
      var promise = $http.get(path);
      promise.success(function(rs ){
      	if(pid == 1){
	      	$scope.model.count = rs.data.count;
	      	$scope.model.total_page = rs.data.total_page;
      	}
        $scope.model.comment = rs.data.replies;
      });

      promise.error(function(error){
        console.log("服务器请求数据出错！");
      });
    };

    $scope.onLoadMore = function(){

    };

});