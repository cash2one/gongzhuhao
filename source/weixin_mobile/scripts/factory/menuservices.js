'use strict';

angular.module('zenmezApp')
  .factory('Menus', function() {
    var chats = [{
      id : 0 ,
      action: 'schedules',
      name: '我的排期',
      icon: 'ion-ios-calendar-outline'
    }, {
      id : 1 ,
      action: 'photos',
      name: '我的照片',
      icon: 'ion-ios-camera-outline'
    }, {
      id : 2 ,
      action: 'share',
      name: '我的分享',
      icon: 'ion-ios-upload-outline'
    }, {
      id : 3 ,
      action: 'service',
      name: '服务列表',
      icon: 'ion-ios-list-outline'
    }, /*{
      id : 4 ,
      action: 'topic',
      name: '话题',
      icon: 'ion-ios-chatboxes-outline'
    },*/{
      id : 5,
      action: 'setting',
      name: '设置',
      icon: 'ion-ios-gear-outline'
    }];

    return {
      all: function() {
        return chats;
      },
      remove: function(chat) {
        chats.splice(chat, 1);
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