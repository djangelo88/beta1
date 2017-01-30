/**
 * Created by Hector on 22/01/2017.
 */

app.controller('WebsiteController', ['$scope', 'NotificationService', 'AlertConfirmService', 'WizardHandler', '$aside', 'WebsiteService', '$stateParams', 'Upload', '$q', function ($scope, NotificationService, AlertConfirmService, WizardHandler, $aside, WebsiteService, $stateParams, Upload, $q) {


    $scope.page = {
        title: 'Website',
        description: 'In most applications you need basic table listings and editing capabilities.' +
        ' With this app you can create simple admin functionality based on a json web service.',
        icon: 'md md-cloud'
    };

    // settings
    $scope.gallery = {
        singular: 'Image',
        plural: 'Images',
        cmd: 'New'
    };
    $scope.settings = {
        wizardEditMode: false,
        editing: true
    };


    /*Get Website by Business*/
    WebsiteService.getAll().success(function (data) {
        $scope.website = data;
        console.debug(data);
    }).error(function (data) {

    }).then(function () {
        /*Route params & Wizard Step set*/
        //NotificationService.error("","ahora");

        if ($stateParams.step) {
            switch ($stateParams.step) {
                case "template":
                    WizardHandler.wizard().goTo(0);
                    break;
                case "basic-info":
                    WizardHandler.wizard().goTo(1);
                    break;
                case "image-gallery":
                    WizardHandler.wizard().goTo(2);
                    break;

                case "menu":
                    WizardHandler.wizard().goTo(3);
                    break;

                case "social-network":
                    WizardHandler.wizard().goTo(4);
                    break;

                case "contact-us":
                    WizardHandler.wizard().goTo(5);
                    break;

                case "staff-service":
                    WizardHandler.wizard().goTo(6);
                    break;

                case "website":
                    WizardHandler.wizard().goTo(7);
                    break;
                default :
                    WizardHandler.wizard().goTo(0);

            }
            if ($scope.website.edit === undefined) {
                $scope.settings.wizardEditMode = true;
            }
        }

    });


    //var defer = $q.defer();


    //$scope.website = WebsiteService.getWebsite();
    //console.log($scope.website);

    /*Basic info*/
    $scope.currentStepOnlyAddAction = false;
    $scope.saveBasicInfo = function (basicinfo) {

        if (!$scope.settings.editing) {
            NotificationService.theme("", "pendiente crear");
        } else {
            WebsiteService.edit("basic_info", $scope.website.id, basicinfo)
                .success(function (data) {
                    if ($scope.currentStepOnlyAddAction) {
                        console.log("save");
                        NotificationService.success("", "Se ha actualizado");
                    } else {
                        console.log("save & add");
                        WizardHandler.wizard().next();
                    }
                }).error(function (data) {
                    NotificationService.error("", "Error al actualizar");
                });

        }

        console.log(basicinfo);


    }

    $scope.onlySave = function () {
        $scope.currentStepOnlyAddAction = true;
    }

    $scope.saveAndContinue = function () {
        $scope.currentStepOnlyAddAction = false;
    }

    // File Upload
    $scope.fileReaderSupported = window.FileReader !== undefined && (window.FileAPI === undefined || FileAPI.html5 !== false);
    $scope.upload = function (file) {
        //alert("dddd")

        if (file !== null && file !== undefined) {
            Upload.upload({
                url: '/api/logosave',
                file: file
            })
                //.progress(progressHandler)
                .success(successHandler);

        }
    };
    $scope.$watch('logofile', function () {
        console.log($scope.logofile);
        $scope.upload($scope.logofile);

    });

    successHandler = function (data, status, headers, config) {
        console.log(data);
        $scope.website.basicinfo.logo = data.logo;
        //console.log('file ' + config.file.name + 'uploaded. Response: ' + JSON.stringify(data));
    };


    /*Website Gallery*/
    var formTplGallery = $aside({
        scope: $scope,
        templateUrl: '/static/assets/tpl/website/form-gallery.html',
        show: false,
        placement: 'left',
        backdrop: false,
        animation: 'am-slide-left'

    });

    showGalleryForm = function () {
        angular.element('.tooltip').remove();
        formTplGallery.show();
    };

    hideGalleryForm = function () {
        formTplGallery.hide();
    };

    $scope.$on('$destroy', function () {
        hideGalleryForm();
    });

    $scope.createItem = function () {
        var item = {editing: true}
        $scope.item = item;
        showGalleryForm();
    };

    /*Contact Us*/
    $scope.saveContactUs = function (contactUs) {

        console.log(contactUs);

        NotificationService.theme("Pendiente", "Actualizacion de contactUs")

        if (!$scope.settings.editing) {

        } else {

            WebsiteService.edit("contact_us", $scope.website.id, contactUs)
                .success(function (data) {
                    if ($scope.currentStepOnlyAddAction) {
                        console.log("save");
                        NotificationService.success("", "Se ha actualizado");
                    } else {
                        console.log("save & add");
                        WizardHandler.wizard().next();
                    }
                }).error(function (data) {
                    NotificationService.error("", "Error al actualizar");
                });
        }
    }


}]);