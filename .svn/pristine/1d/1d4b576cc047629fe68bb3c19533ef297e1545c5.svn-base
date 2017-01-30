/**
 * Created by maykel on 16/01/17.
 */
app.factory('WorkersService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var _getAll = function (model) {
        return $http.get(BASE_URL + 'workers');
    };

    var _getAllPositions = function (model) {
        return $http.get(BASE_URL + 'positions');
    };

    var _getById = function (model, id) {
        return $http.get(BASE_URL + '?model=' + model + '&id=' + id);
    };

    var _post = function (object) {
        return $http.post(BASE_URL + 'workers/add', object);
    };
    var _postEdit = function (id, object) {
        //console.log(id);
        return $http.post(BASE_URL + 'workers/edit/' + id, object);
    };
    var _postDelete = function (objects) {
        return $http.post(BASE_URL + 'workers/remove', objects);
    };



    return {
        getAll: _getAll,
        getAllPositions:_getAllPositions,
        getById: _getById,
        add: _post,
        edit: _postEdit,
        delete: _postDelete,
        baseUrl: BASE_URL
    };


}]);