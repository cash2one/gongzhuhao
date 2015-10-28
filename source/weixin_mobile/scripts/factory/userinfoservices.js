'use strict';

angular.module('zenmezApp')
  .factory("UserInfo", function($http, $q, Menus) {
    var serviceBase = '/mobile/user/show/services/check/'
    var userInfo = {};
    userInfo.getUserInfo = function() {
      if (!userInfo.instance) {
        var promise = $http.get(serviceBase);
        return $q(function(resolve, reject) {
          promise.then(function(data) {
            if (data && data.data.stat == '0') {
              Menus.remove(3);
            }
            userInfo.instance = data;
            resolve(userInfo.instance);
          })
        });
      } else {
        return $q(function(resolve, reject) {
          resolve(userInfo.instance);
        });
      }
    };
    return userInfo;
  });