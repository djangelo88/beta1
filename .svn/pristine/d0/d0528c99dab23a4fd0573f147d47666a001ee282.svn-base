/**
 * Created by Hector on 12/01/2017.
 */
app.factory('ProductService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var local_model = 'products';

    var _getAll = function () {
        return $http.get(BASE_URL+ local_model);
    };

    var _getById = function (model, id) {
        return $http.get(BASE_URL+'?model='+model+'&id='+id);
    };

    var _post = function (object) {
        return $http.post(BASE_URL + local_model,object);
    };
    var _postEdit = function (id,object) {
        return $http.post(BASE_URL + local_model+'/'+id,object);
    };
    var _postDelete = function (objects) {
        return $http.post(BASE_URL + local_model + '/delete',objects);
    };


    return {
        getAll:_getAll,
        getById: _getById,
        add: _post,
        edit: _postEdit,
        delete: _postDelete,
        baseUrl: BASE_URL
    };


}]);