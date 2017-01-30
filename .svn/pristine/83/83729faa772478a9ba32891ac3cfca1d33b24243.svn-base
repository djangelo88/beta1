/**
 * Created by maykel on 16/01/17.
 */

app.controller('PositionController', ['$scope', '$window', '$aside', 'PlaceholderTextService', '$alert', '$http', 'PositionService', '$timeout','$location','AlertConfirmService','NotificationService', function ($scope, $window, $aside, PlaceholderTextService, $alert, $http, PositionService, $timeout,$location,AlertConfirmService,NotificationService) {

    // settings
    $scope.settings = {
        singular: 'Puesto',
        plural: 'Puestos',
        cmd: 'Nuevo'
    };
    //page
    $scope.page = {
        title: 'Puestos de Trabajo',
        description: 'In most applications you need basic table listings and editing capabilities.' +
        ' With this app you can create simple admin functionality based on a json web service.',
        icon: 'md md-work'
    };


    //console.debug($hh);

    // adding customers data
    var data = [];
    PositionService.getAll()
        .success(function (data, status, headers, config) {
            console.log(data);
            $scope.data = data;
        });

    //adding others stuffs

    // defining template
    var formTpl = $aside({
        scope: $scope,
        templateUrl: '/static/assets/tpl/positions/positions-form.html',
        show: false,
        placement: 'left',
        backdrop: false,
        animation: 'am-slide-left'
    });

    // methods
    $scope.checkAll = function () {
        angular.forEach($scope.data, function (item) {
            item.selected = !item.selected;
        });
    };


    $scope.editItem = function (item) {

        if (item) {
            item.editing = true;
            $scope.item = item;
            $scope.settings.cmd = 'Edit';



            console.log($scope.item);

            showForm();
        }
    };

    $scope.viewItem = function (item) {
        if (item) {
            item.editing = false;
            $scope.item = item;
            $scope.settings.cmd = 'View';
            showForm();
        }
    };

    $scope.createItem = function () {

        var item = {
            //icon: PlaceholderTextService.createIcon(true),
            editing: true,
            creating: true,
            name: '',
            description: '',
        };
        $scope.item = item;
        $scope.settings.cmd = 'New';

        showForm();
    };

    $scope.saveItem = function (item, saveAndAdd) {

        $scope.item.positions = $scope.item.positions;

        $scope.validation_errors = '';

        if ($scope.settings.cmd == 'New') {

            PositionService.add($scope.item)
                .success(function (data) {

                    var refererNotThemeforest = $alert({
                        title: '',
                        content: 'Se ha creado el Puesto de Trabajo satisfactoriamente',
                        placement: 'top-right',
                        type: 'success',
                        //types:info,theme,danger,success,warning
                        //container: '.alert-container-top-right',
                        show: true,
                        animation: 'mat-grow-top-right'
                    });

                    $timeout(function () {
                        refererNotThemeforest.show();
                    }, 1750);


                    if ($scope.settings.cmd == 'New') {
                        $scope.data.push($scope.item);
                    }

                    hideForm();

                    if (saveAndAdd) {
                        $scope.selectedPreffix = '';
                        $scope.selectedSuffix = '';

                        $scope.createItem();
                    }
                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);

                    var refererNotThemeforest = $alert({
                        title: 'Error',
                        content: 'Ha exixtido un error al adicionar el puesto de trabajo',
                        placement: 'top-right',
                        type: 'danger',
                        //types:info,theme,danger,success,warning
                        //container: '.alert-container-top-right',
                        show: true,
                        animation: 'mat-grow-top-right'
                    });
                    $timeout(function () {
                        refererNotThemeforest.show();
                    }, 1750);

                });
        } else {

            PositionService.edit($scope.item.id, $scope.item)
                .success(function (data) {

                    NotificationService.success('', 'Se ha actualizado el puesto de trabajo');

                    hideForm();

                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    NotificationService.error('Error', 'Ha existido un error al adicionar el puesto de trabajo');

                });
        }


    };

   $scope.remove = function (item) {

        if (item) {
            callbackFn = function () {
                PositionService.delete(new Array(item))
                    .success(function () {
                        NotificationService.success('', 'Se ha eliminado el puesto de trabajo seleccionado');
                        $scope.data.splice($scope.data.indexOf(item), 1);
                    }).error(function () {
                        NotificationService.error('Error', 'Ha existido un error al eliminar el puesto de trabajo seleccionado');
                    });
            };

            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea eliminar el puesto de trabajo seleccionado?", callbackFn);

        } else {

            callbackFn = function () {
                var seleccionados = $scope.data.filter(
                    function (item) {
                        return item.selected;
                    }
                );
                PositionService.delete(seleccionados).success(function () {
                    NotificationService.success('', 'Se han eliminado los puestos de trabajo seleccionados');

                    for (index in seleccionados) {
                        $scope.data.splice($scope.data.indexOf(seleccionados[index]), 1);
                    }
                }).error(function () {
                    NotificationService.error('Error', 'Ha existido un error al eliminar los puestos de trabajo seleccionados');
                });
            }
            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea los clientes seleccionados?", callbackFn);
        }


    };

    showForm = function () {
        angular.element('.tooltip').remove();
        formTpl.show();
    };

    hideForm = function () {
        formTpl.hide();
    };

    $scope.$on('$destroy', function () {
        hideForm();
    });

    $scope.print = function () {
        return $window.print();
    }


}]);

