/**
 * Created by Hector on 17/01/2017.
 */
app.factory('AlertConfirmService', ['$rootScope', '$ngConfirm', function ($rootScope, $ngConfirm) {

    var _basicConfirm = function (title, content, callbackFn) {
        $ngConfirm({
            title: title,
            content: content,
            //scope: $scope,
            escapeKey: 'no',
            buttons: {
                yes: {
                    //show: false, // hides the button using display: none
                    text:'si',
                    btnClass: 'btn-red',
                    keys: ['y'],
                    action: function ($scope, button) {
                        return callbackFn();
                    }
                },
                no: {
                    btnClass: 'btn-default',
                    keys: ['N'],
                    action: function ($scope, button) {
                        //$ngConfirm('You clicked No.');
                    }
                }
            }
        });
    }



    return {
        basicConfirm: _basicConfirm
    };


}]);