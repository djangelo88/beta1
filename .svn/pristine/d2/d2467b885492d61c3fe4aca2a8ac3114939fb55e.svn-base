/**
 * Created by Hector on 12/01/2017.
 */
app.factory('NomenclatorService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var _getAll = function (model) {
        return $http.get(BASE_URL+'nomenclator?model='+model);
    };

    var _getById = function (model, id) {
        return $http.get(BASE_URL+'nomenclator?model='+model+'&id='+id);
    };

    var _post = function (model, object) {

        $http.get(BASE_URL + model, object)
            .success(function (data, status, headers, config) {
                return data;
            })
            .error(function (data, status, headers, config) {
                return status;
            });
    };

    return {
        getAll:_getAll,
        getById: _getById,
        post: _post,
        baseUrl: BASE_URL
    };


}]);