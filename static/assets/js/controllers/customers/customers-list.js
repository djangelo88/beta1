/**
 * Created by Hector on 10/01/2017.
 */
app.controller('CustomersController',
    ['$scope', '$window', '$aside', 'PlaceholderTextService', '$alert', '$http',
        'NomenclatorService', 'CustomerService', '$timeout', 'NotificationService',
        '$location', 'AlertConfirmService','$rootScope',
        'Upload',
        function ($scope, $window, $aside, PlaceholderTextService, $alert, $http, NomenclatorService, CustomerService,
                  $timeout, NotificationService, $location, AlertConfirmService,$rootScope, Upload) {

    // settings
    $scope.settings = {
        singular: 'Cliente',
        plural: 'Clientes',
        cmd: 'New'
    };
    //page
    $scope.page = {
        title: 'Clientes',
        description: 'In most applications you need basic table listings and editing capabilities.' +
        ' With this app you can create simple admin functionality based on a json web service.',
        icon: 'md md-group'
    };

    // adding customers data
    var data = [];
    CustomerService.getAll()
        .success(function (data, status, headers, config) {

            angular.forEach(data, function (item) {
                item.icon = CustomerService.createIcon(item.new);
            });

            $scope.data = data;
        });

    //adding others stuffs

    // adding customers data


    // defining template
    var formTpl = $aside({
        scope: $scope,
        templateUrl: '/static/assets/tpl/customers/customers-form.html',
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
            company: '',
            phone_home: '',
            cellphone: ''
        };
        $scope.item = item;
        $scope.settings.cmd = 'New';

        showForm();
    };
    $scope.reloadStates = function () {
        if ($scope.item.address.country.id) {
            NomenclatorService.getById('country', $scope.item.address.country.id).success(function (data) {
                $scope.countryStates = data.states;
            })
        }
    };

    $scope.showNewForm = false;
    $scope.saveAndAdd = function (val) {

        $scope.showNewForm = val;


    }


    $scope.saveClientItem = function (item) {

        console.log(item);

        item.first_line = item.address.first_line;
        item.second_line = item.address.second_line;
        item.city = item.address.city;
        item.zip = item.address.zip;
        item.state = item.address.state.id;
        item.country = item.address.country.id;


        $scope.validation_errors = '';

        if ($scope.settings.cmd == 'New') {

            CustomerService.add($scope.item)
                .success(function (data) {

                    NotificationService.success('', 'Se ha creado el cliente satisfactoriamente');
                    data.icon = CustomerService.createIcon(data);

                    if ($scope.settings.cmd == 'New') {
                        $scope.data.push(data   );
                    }
                    hideForm();
                    if ($scope.showNewForm) {
                        $scope.createItem();
                    }
                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);
                    NotificationService.error('Error', 'Ha existido un error al adicionar el cliente');


                });
        } else {

            CustomerService.edit(item.id, item)
                .success(function (data) {

                    NotificationService.success('', 'Se ha actualizado el cliente');

                    hideForm();

                }).error(function (data) {

                    $scope.validation_errors = JSON.parse(data);

                    NotificationService.error('Error', 'Ha existido un error al actualizar el cliente');

                });
        }


    };


    $scope.remove = function (item) {



        if (item) {
            callbackFn = function () {
                CustomerService.delete(new Array(item))
                    .success(function () {
                        NotificationService.success('', 'Se ha eliminado el cliente seleccionado');
                        $scope.data.splice($scope.data.indexOf(item), 1);
                    }).error(function () {
                        NotificationService.error('Error', 'Ha existido un error al eliminar el cliente seleccionado');
                    });
            };

            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea eliminar el cliente seleccionado?", callbackFn);

        } else {

            callbackFn = function () {
                var seleccionados = $scope.data.filter(
                    function (item) {
                        return item.selected;
                    }
                );
                CustomerService.delete(seleccionados).success(function () {
                    NotificationService.success('', 'Se han eliminado los clientes seleccionados');

                    for (index in seleccionados) {
                        $scope.data.splice($scope.data.indexOf(seleccionados[index]), 1);
                    }
                }).error(function () {
                    NotificationService.error('Error', 'Ha existido un error al eliminar los clientes seleccionados');
                });
            }
            AlertConfirmService.basicConfirm("Eliminar", "Confirma que desea eliminar los clientes seleccionados?", callbackFn);
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

    //$scope.exportExcel = function () {
    //    return $location.url('http://app.caterfull.com:8000/customers/export');
    //}
  //File Upload
  $scope.fileReaderSupported = window.FileReader !== undefined && (window.FileAPI === undefined || FileAPI.html5 !== false);

  $scope.$watch('importfile', function (file) {
      console.log(file);
    $scope.upload(file);
  });

  //progressHandler = function(evt) {
  //  var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
  //  console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
  //};
  //
  successHandler = function(data, status, headers, config) {
      console.log(data);
       angular.forEach(data, function (item) {
                item.icon = CustomerService.createIcon(item.new);
           $scope.data.push(item);
            });
    //console.log('file ' + config.file.name + 'uploaded. Response: ' + JSON.stringify(data));
  };





  $scope.upload = function (file) {

    if (file !== null && file !== undefined) {


        Upload.upload({
          url: '/api/customers/import/',
          file: file
        })

        .success(successHandler);

    }
  };
$scope.test_func = function () {
 console.log($scope.importfile);
}


}]);


//app.controller('ImportController',
//    ['$scope', '$window', '$aside', 'PlaceholderTextService', '$alert', '$http',
//        'NomenclatorService', 'CustomerService', '$timeout', 'NotificationService',
//        '$location', 'AlertConfirmService','$rootScope',
//        'Upload',
//        function ($scope, $window, $aside, PlaceholderTextService, $alert, $http, NomenclatorService, CustomerService,
//                  $timeout, NotificationService, $location, AlertConfirmService,$rootScope, Upload)
//        {
//            // File Upload
//  $scope.fileReaderSupported = window.FileReader !== undefined && (window.FileAPI === undefined || FileAPI.html5 !== false);
//    console.log( $scope.fileReaderSupported );
//    //$scope.importfile = 'importar';
//  $scope.$watch('importfile', function (val) {
//      console.log($scope.importfile );
//    //$scope.upload($scope.importfile);
//  });
//
//  //progressHandler = function(evt) {
//  //  var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
//  //  console.log('progress: ' + progressPercentage + '% ' + evt.config.file.name);
//  //};
//  //
//  successHandler = function(data, status, headers, config) {
//      console.log(data);
//
//    //console.log('file ' + config.file.name + 'uploaded. Response: ' + JSON.stringify(data));
//  };
//
//
//
//
//
//  $scope.upload = function (file) {
//    if (file !== null && file !== undefined) {
//
//
//        //Upload.upload({
//        //  url: '/api/business/uploadlogo',
//        //  file: file
//        //})
//
//        //.success(successHandler);
//
//    }
//  };
////$scope.test_func = function () {
//// console.log($scope.importfile);
////}
//
//        }]);