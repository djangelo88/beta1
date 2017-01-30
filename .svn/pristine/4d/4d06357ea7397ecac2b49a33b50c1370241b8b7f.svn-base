/**
 * Created by maykel on 23/01/17.
 */
app.factory('RecipesService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    var local_model = 'recipes';

    var _getAll = function () {
        return $http.get(BASE_URL+ local_model);
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
        getById: _getById,
        add: _post,
        edit: _postEdit,
        delete: _postDelete,
        baseUrl: BASE_URL
    };


}]);
