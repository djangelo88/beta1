/**
 * Created by Hector on 12/01/2017.
 */
app.factory('StripeService', ['$rootScope', '$filter', '$http', 'BASE_URL', function ($rootScope, $filter, $http, BASE_URL) {

    //var _baseURL = 'http://app.caterfull.com:8000/api';

   
    //var _get = function (model) {
    //    return $http.get(BASE_URL + local_model);
    //};
    //
    //var _post = function (object) {
    //    return $http.post(BASE_URL + local_model,object);
    //};
    var _post_email = function(url, object){
        return $http.post(url, object);
    }
    var _post_cancel_subs = function(url){
        return $http.post(url);
    }

    var _get_publishablekey = function () {
        return $http.get(BASE_URL + 'stripe/publishablekey');
    }

    var _subscribe = function(data){
        return $http.post(BASE_URL + 'stripe/subscribe');
    }
    var _changecard = function(data){
        return $http.post(BASE_URL + 'stripe/changecard');
    }
    //
    //
    //
    return {
        //get: _get,

        updateBillingEmail: _post_email,
        cancelSubscription: _post_cancel_subs,
        baseUrl: BASE_URL,
        publishableKey:_get_publishablekey,
        subscribe: _subscribe,
        changeCard: _changecard
    };


}]);

