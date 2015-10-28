/*
 * SimplePubSub from https://github.com/mbenford/ngTagsInput/blob/master/src/util.js
 * */
'use strict';

function SimplePubSub() {
  var events = {};
  return {
    on: function(names, handler) {
      names.split(' ').forEach(function(name) {
        if (!events[name]) {
          events[name] = [];
        }
        events[name].push(handler);
      });
      return this;
    },
    trigger: function(name, args) {
      angular.forEach(events[name], function(handler) {
        handler.call(null, args);
      });
      return this;
    }
  };
};

angular.module('tabSlideBox', [])
  .directive('tabSlideBox', ['$timeout', '$window', '$ionicSlideBoxDelegate', '$ionicScrollDelegate',
    function($timeout, $window, $ionicSlideBoxDelegate, $ionicScrollDelegate) {
      'use strict';

      return {
        restrict: 'A, E, C',
        link: function(scope, element, attrs, ngModel) {

          var ta = element[0],
            $ta = element;
          $ta.addClass("tabbed-slidebox");
          if (attrs.tabsPosition === "bottom") {
            $ta.addClass("btm");
          }

          function renderScrollableTabs() {
            var iconsDiv = angular.element(ta.querySelector(".tsb-icons")),
              icons = iconsDiv.find("a"),
              wrap = iconsDiv[0].querySelector(".tsb-ic-wrp"),
              totalTabs = icons.length;
            var scrollDiv = wrap.querySelector(".scroll");

            angular.forEach(icons, function(value, key) {
              var a = angular.element(value);
              a.on('click', function() {
                $ionicSlideBoxDelegate.slide(key);
              });
            });

            var initialIndex = attrs.tab;
            //Initializing the middle tab
            if (typeof attrs.tab === 'undefined' || (totalTabs <= initialIndex) || initialIndex < 0) {
              initialIndex = Math.floor(icons.length / 2);
            }

            //If initial element is 0, set position of the tab to 0th tab 
            if (initialIndex == 0) {
              setPosition(0);
            }

            $timeout(function() {
              $ionicSlideBoxDelegate.slide(initialIndex);
            }, 0);
          }

          function setPosition(index) {
            var iconsDiv = angular.element(ta.querySelector(".tsb-icons")),
              icons = iconsDiv.find("a"),
              wrap = iconsDiv[0].querySelector(".tsb-ic-wrp"),
              totalTabs = icons.length;
            var scrollDiv = wrap.querySelector(".scroll");

            var middle = iconsDiv[0].offsetWidth / 2;
            var curEl = angular.element(icons[index]);
            if (curEl && curEl.length) {
              var curElWidth = curEl[0].offsetWidth,
                curElLeft = curEl[0].offsetLeft;

              angular.element(iconsDiv[0].querySelector(".active")).removeClass("active");
              curEl.addClass("active");
            }
          };

          function getX(matrix) {
            matrix = matrix.replace("translate3d(", "");
            matrix = matrix.replace("translate(", "");
            return (parseInt(matrix));
          }
          var events = scope.events;
          events.on('slideChange', function(data) {
            setPosition(data.index);
          });
          renderScrollableTabs();
        },
        controller: function($scope, $attrs, $element , $window) {
          $scope.events = new SimplePubSub();
          $scope.$watch('isLoading' , function(flag){
            if(!flag){
              var elm = $element.find('.slider-slides');
              $window.setTimeout(function(){
                var h = angular.element(elm.children()[$attrs.tab || 0]).find('.topic-tabs').height();
                $element.parent().css('height',h + 'px');
              } , 500);
            }
          });

          $scope.slideHasChanged = function(index) {
            var elm = $element.find('.slider-slides');
            var h = angular.element(elm.children()[index]).find('.topic-tabs').height();
            $element.parent().css('height',h + 'px');
            $scope.events.trigger("slideChange", {
              "index": index
            });
            $timeout(function() {
              $scope.onSlideMove({
                "index": eval(index)
              });
            }, 100);
          };
        }
      };

    }
  ]);