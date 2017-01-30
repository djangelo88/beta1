/**
 * Created by Hector on 14/01/2017.
 */
    //types:info,theme,danger,success,warning
    //types:info,theme,danger,success,warning
app.factory('NotificationService', ['$rootScope', '$alert','$timeout', function ($rootScope, $alert,$timeout) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var _baseAlert = function (type, title, message) {

        var refererNotThemeforest = $alert({
            title: title,
            content: message,
            placement: 'top-right',
            type: type,
            //container: '.alert-container-top-right',
            show: true,
            animation: 'mat-grow-top-right'
            //autoclose: true

        });

        $timeout(function () {
            refererNotThemeforest.show();
        }, 1750);

    };

    var _success = function (title, message) {
        return _baseAlert('success', title, message);
    };

    var _error = function (title, message) {
        return _baseAlert('danger', title, message);
    };
    var _warning = function (title, message) {
        return _baseAlert('warning', title, message);
    };
    var _info = function (title, message) {
        return _baseAlert('info', title, message);
    };


    var _theme = function (title, message) {
        return _baseAlert('theme', title, message);
    };


    return {
        success: _success,
        error: _error,
        info: _info,
        theme: _theme,
        warning: _warning
    };


}]);