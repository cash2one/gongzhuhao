angular.module('gzh.filter.qqface',[]).filter('qqface', function(){
  'use strict';
    return function(value){
      if(!!value){
        // value = value.replace(/\</g, '&lt;');
        // value = value.replace(/\>/g, '&gt;');
        // value = value.replace(/\n/g, '<br/>');
        value = value.replace(/\[em_([0-9]*)\]/g, '<img src="/static/images/faces/$1.gif" border="0" />');
      }
      return value;
    }
});