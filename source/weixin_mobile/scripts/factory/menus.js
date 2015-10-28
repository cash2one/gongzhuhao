'use strict';

angular.module('zenmezApp')
  .factory('Menus', function() {
    var chats = [{
      action: 'schedules',
      name: '我的排期',
      icon: 'ion-ios-calendar-outline'
    }, {
      action: 'photos',
      name: '我的照片',
      icon: 'ion-ios-camera-outline'
    }, {
      action: 'share',
      name: '我的分享',
      icon: 'ion-ios-upload-outline'
    }, {
      action: 'service',
      name: '服务列表',
      icon: 'ion-ios-list-outline'
    }, {
      action: 'setting',
      name: '设置',
      icon: 'ion-ios-gear-outline'
    }];

    return {
      all: function() {
        return chats;
      },
      remove: function(chat) {
        chats.splice(chats.indexOf(chat), 1);
      },
      get: function(chatId) {
        for (var i = 0; i < chats.length; i++) {
          if (chats[i].id === parseInt(chatId)) {
            return chats[i];
          }
        }
        return null;
      }
    };
  });