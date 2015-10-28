+(function(window, angular, undefined) {

  'use strict';

  var mfb = angular.module('ng-mfb', []);

  mfb.run(['$templateCache',
    function($templateCache) {
      $templateCache.put('ng-mfb-menu-default.tpl.html',
        '<ul class="mfb-component--{{position}} mfb-{{effect}}"' +
        '    data-mfb-toggle="{{togglingMethod}}">' +
        '  <li class="mfb-component__wrap">' +
        '    <a ng-href="{{ngHref}}" ng-click="clicked()" ng-mouseenter="hovered()" ng-mouseleave="hovered()"' +
        '     class="mfb-component__button--main">' +
        '     <i class="mfb-component__main-icon--resting {{resting}}"></i>' +
        '     <i class="mfb-component__main-icon--active {{active}}"></i>' +
        '    </a>' +
        '</li>' +
        '</ul>'
      );
    }
  ]);

  mfb.directive('mfbMenu', ['$timeout',
    function($timeout) {
      return {
        restrict: 'EA',
        transclude: true,
        replace: true,
        scope: {
          position: '@',
          effect: '@',
          resting: '@restingIcon',
          active: '@activeIcon',
          ngHref: '@',
          togglingMethod: '@',
        },
        templateUrl: function(elem, attrs) {
          return attrs.templateUrl || 'ng-mfb-menu-default.tpl.html';
        },
        link: function(scope, elem, attrs) {

          function _isTouchDevice() {
            return window.Modernizr && Modernizr.touch;
          }

          function _isHoverActive() {
            return scope.togglingMethod === 'hover';
          }

          function useClick() {
            scope.$apply(function() {
              scope.togglingMethod = 'click';
            });
          }

          scope.$watch('$parent.isMoving' , function(value){
            if(value){
              elem.removeClass('mfb-component--br').addClass("mfb-component--lr")
            }else{
              elem.removeClass('mfb-component--lr').addClass("mfb-component--br")
            }
          });

          scope.clicked = function() {
            if (!_isHoverActive()) {
              scope.$parent.toggle(scope.menuState);
            }
          };
          scope.hovered = function() {
            if (_isHoverActive()) {}
          };

          if (_isTouchDevice() && _isHoverActive()) {
            $timeout(useClick);
          }
        }
      };
    }
  ]);
})(window, angular);