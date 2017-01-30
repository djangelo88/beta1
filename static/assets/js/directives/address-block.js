/**
 * Created by Hector on 15/01/2017.
 */
app.directive('addressBlock', ['NomenclatorService', function (NomenclatorService) {
    return {
        restrict: 'E',
        templateUrl: '/static/assets/tpl/directives/address-block.html',
        replace: true,

        scope: {
            address: '=',
            validation_errors: '=',
            editing: '=',
            new:'='

        },
        controller: ['$element', '$location', '$rootScope', '$scope', function ($element, $location, $rootScope, $scope) {

            //console.log($scope.validation_errors);
            //console.log($element);

            //$element.countries = [];
            NomenclatorService.getAll('country')
                .success(function (data) {
                    $scope.countries = data;
                });


            //if ($scope.address !== undefined) {
            //    NomenclatorService.getById('country', $scope.address.country.id).success(function (data) {
            //        $scope.countryStates = data.states;
            //    });
            //}
            console.debug($scope);
            $scope.reloadStates = function () {

                if ($scope.address !== undefined && $scope.address.country.id) {
                    NomenclatorService.getById('country', $scope.address.country.id).success(function (data) {
                        $scope.countryStates = data.states;
                    })
                }

            };
            if(!$scope.new){
                $scope.reloadStates();
            }


        }],
        link: function ($scope, $element) {


  //          console.log( $element.validation_errors);
  //console.log($scope);
        }

        //    this.getName = function (name) {
        //        if (name !== undefined) {
        //            return name;
        //        } else {
        //            return $element.find('a').text().trim();
        //        }
        //    };
        //
        //    this.setBreadcrumb = function (name) {
        //        $rootScope.pageTitle = this.getName(name);
        //    };
        //
        //    this.isSelected = function (href) {
        //        return $location.path() == href.slice(1, href.length);
        //    };
        //}],
        //link: function ($scope, $element) {
        //    $scope.todoService = new todoService($scope);
        //}
    };
}]);

