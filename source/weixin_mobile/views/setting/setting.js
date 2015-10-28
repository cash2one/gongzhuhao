'use strict';

angular.module('zenmezApp')
  .controller('SettingCtrl', function ($scope) {
  })
  .config(function($stateProvider) {
  $stateProvider
	  .state('zenmez.setting', {
	    url: "/setting",
	    views: {
	      'menuContent': {
	        templateUrl: "views/setting/setting.tpl.html",
	        controller : 'SettingCtrl'
	      }
	    }
	  });
});
