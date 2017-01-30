/**
 * Created by maykel on 16/01/17.
 */

app.controller('WorkersController', ['$scope', '$window', '$aside', 'PlaceholderTextService', '$alert', '$http', 'WorkersService', '$timeout','$location','AlertConfirmService','NotificationService', function ($scope, $window, $aside, PlaceholderTextService, $alert, $http, WorkersService, $timeout,$location,AlertConfirmService,NotificationService) {

    // settings
    $scope.settings = {
        singular: 'Trabajador',
        plural: 'Trabajadores',
        cmd: 'Nuevo'
    };
    //page
    $scope.page = {
        title: 'Trabajadores',
        description: 'In most applications you need basic table listings and editing capabilities.' +
        ' With this app you can create simple admin functionality based on a json web service.',
        icon: 'md md-group'
    };


    //console.debug($hh);

    // adding customers data
    var data = [];
    WorkersService.getAll()
        .success(function (data, status, headers, config) {
            $scope.data = data;
        });
    WorkersService.getAllPositions()
        .success(function (data, status, headers, config) {
            $scope.positions = data;
        });

    //adding others stuffs

    // defining template
    var formTpl = $aside({
        scope: $scope,
        templateUrl: '/static/assets/tpl/workers/workers-form.html',
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
            console.log(item);
            item.editing = true;
            $scope.item = item;
            $scope.settings.cmd = 'Edit';

            //console.log($scope.item);
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
            last_name: ''

        };
        $scope.item = item;
        $scope.settings.cmd = 'New';

        showForm();
    };

    $scope.saveItem = function (item, saveAndAdd) {

        $scope.validation_errors = '';

        if ($scope.settings.cmd == 'New') {

            WorkersService.add($scope.item)
                .success(function (data1) {
                    var refererNotThemeforest = $alert({
                        title: '',
                        content: 'Se ha creado el Trabajador satisfactoriamente',
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
                        $scope.data.push(data1);
                    }

                    hideForm();

                    if (saveAndAdd) {
                    $scope.createItem();
                    }
                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    var refererNotThemeforest = $alert({
                        title: 'Error',
                        content: 'Ha exixtido un error al adicionar el Trabajador',
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

            WorkersService.edit($scope.item.id, $scope.item)
                .success(function (data) {

                    NotificationService.success('', 'Se ha actualizado el trabajador');
                    hideForm();

                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    NotificationService.error('Error', 'Ha existido un error al adicionar el trabajador');

                });
        }


    };

   $scope.remove = function (item) {

        if (item) {
            callbackFn = function () {
                WorkersService.delete(new Array(item))
                    .success(function () {
                        NotificationService.success('', 'Se ha eliminado el trabajador seleccionado');
                        $scope.data.splice($scope.data.indexOf(item), 1);
                    }).error(function () {
                        NotificationService.error('Error', 'Ha existido un error al eliminar el trabajador seleccionado');
                    });
            };

            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea eliminar el trabajador seleccionado?", callbackFn);

        } else {

            callbackFn = function () {
                var seleccionados = $scope.data.filter(
                    function (item) {
                        return item.selected;
                    }
                );
                WorkersService.delete(seleccionados).success(function () {
                    NotificationService.success('', 'Se han eliminado los trabajador seleccionados');

                    for (index in seleccionados) {
                        $scope.data.splice($scope.data.indexOf(seleccionados[index]), 1);
                    }
                }).error(function () {
                    NotificationService.error('Error', 'Ha existido un error al eliminar los trabajadores seleccionados');
                });
            }
            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea los trabajadores seleccionados?", callbackFn);
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

