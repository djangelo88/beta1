/**
 * Created by Hector on 12/01/2017.
 */
app.factory('ProfileService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';
    var local_model = 'business';
    var _get = function (model) {
        return $http.get(BASE_URL + local_model);
    };

    var _post = function (object) {
        return $http.post(BASE_URL + local_model,object);
    };

    var _getTax = function(){
        //_get(local_model).success(function (data) {
        //    console.log(data);
        //    return 5;
        //});
        return 7;
    }
    _getTax();




    return {
        get: _get,
        updateProfile: _post,
        baseUrl: BASE_URL,
        getTax:_getTax
    };


}]);

