angular.module('zenmezApp').directive('fancybox', function ($compile, $http) {
    return {
        restrict: 'A',
        
        controller: function($scope) {
            $scope.openFancybox = function (url) {
                $.fancybox( {href : url , closeClick:true, closeBtn : false ,padding : [0 ,0 ,0 ,0] , width: 'auto' , height: 'auto' , fitToView : true} )
                    // $http.get(url).then(function(response) {
                    //     if (response.status == 200) {

                    //         var template = angular.element(response.data);
                    //         var compiledTemplate = $compile(template);
                    //         compiledTemplate($scope);

                    //         $.fancybox.open({ content: template, type: 'html' });
                    //     }
                    // });
            };
        }
    };
});