/**
 * Created by Hector on 21/01/2017.
 */
app.directive('websiteStatus', function () {

    return {
        restrict: 'E',
        templateUrl: '/static/assets/tpl/directives/website-status.html',
        replace: true,
        scope: {
            status: '='
        },
        controller: ['$element', '$location', '$rootScope', '$scope', function ($element, $location, $rootScope, $scope) {
            //
            //console.log($scope);
            //console.log($scope.status.template);
            //console.log($element);
            //console.log($rootScope);

            switch ($scope.status) {
                case 0:
                    $scope.published = false;
                    $scope.cssclass = 'green light-green';
                    //$scope.cssClass = 'grey lighten-1';
                    break;
                case 1:
                    $scope.published = true;
                     $scope.cssclass = 'green light-green';
                    break;
                default :
                    $scope.published = true;
                     $scope.cssclass = 'green light-green';
            }


        }],
        link: function (scope, element, attrs, linkCtrl) {
            //console.log('website-status');
            //console.log(scope.status);
            //attrs.class().append(l)
        }
    }

})