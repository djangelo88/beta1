/**
 * Created by maykel on 23/01/17.
 */
app.factory('IngredientsService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    var local_model = 'ingredients';

    var _getAll = function () {
        return $http.get(BASE_URL+ local_model);
    };
    var _getAllMeasures = function (model) {
        return $http.get(BASE_URL + 'measures');
    };

    var _getById = function (model, id) {
        return $http.get(BASE_URL+'?model='+model+'&id='+id);
    };

    var _post = function (object) {
        return $http.post(BASE_URL + local_model+'/add',object);
    };
    var _postEdit = function (id,object) {
        return $http.post(BASE_URL + local_model+'/edit/'+id,object);
    };
    var _postDelete = function (objects) {
        return $http.post(BASE_URL + local_model + '/remove',objects);
    };


    return {
        getAll:_getAll,
        getAllMeasures:_getAllMeasures,
        getById: _getById,
        add: _post,
        edit: _postEdit,
        delete: _postDelete,
        baseUrl: BASE_URL
    };


}]);