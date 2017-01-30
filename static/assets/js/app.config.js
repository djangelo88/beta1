// routes$stateProvider, $urlRouterProvider
//app.config(['$routeProvider', function ($routeProvider) {
//    $routeProvider.when('/', {
//        templateUrl: '/static/assets/tpl/dashboard.html'
//    }).when('/:folder/:tpl', {
//        templateUrl: function (attr) {
//            return '/static/assets/tpl/' + attr.folder + '/' + attr.tpl + '.html';
//        }
//    }).when('/:tpl', {
//        templateUrl: function (attr) {
//            return '/static/assets/tpl/' + attr.tpl + '.html';
//        }
//    }).otherwise({redirectTo: '/'});
//}])
app.config(['$stateProvider','$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
   var route = 'static/assets/tpl/';
   $urlRouterProvider.otherwise("/dashboard");
        $stateProvider


        // Landing page
        .state('dashboard', {
            url: "/dashboard",
            templateUrl: route+"dashboard.html"

        })
        .state('customers', {
                url: "/customers",
                templateUrl: route+"customers/list.html",
                 controller:'CustomersController'

            })
        .state('proposals', {
                url: "/proposals",
                templateUrl: route+"proposals/list.html",
                 controller:'ProposalsController'

            })
      .state('invoices', {
                url: "/invoices",
                templateUrl: route+"invoices/list.html",
                 controller:'ProductController'

            })
       .state('positions', {
                url: "/positions",
                templateUrl: route+"positions/list.html",
                 controller:'PositionController'

            })
     .state('workers', {
                url: "/workers",
                templateUrl: route+"workers/list.html",
                 controller:'WorkersController'

            })
      .state('services', {
                url: "/services",
                templateUrl: route+"services/list.html"
                 //controller:'ServicesController'

            })
    .state('ingredients', {
                url: "/ingredients",
                templateUrl: route+"ingredients/list.html",
                 controller:'IngredientsController'

            })
    .state('recipes', {
                url: "/recipes",
                templateUrl: route+"recipes/list.html",
                 controller:'RecipesController'

            })
    .state('products', {
                url: "/products",
                templateUrl: route+"products/list.html",
                 controller:'ProductController'

            })
    .state('calendar', {
                url: "/calendar",
                templateUrl: route+"calendar/calendar.html",
                 controller:'CalendarController'

            })
    .state('website', {
                url: "/website/:step",
                templateUrl: route+"website/templates.html",
                controller: 'WebsiteController'

            })
    .state('profile', {
                url: "/profile",
                templateUrl: route+"business/profile.html",
                controller:'ProfileController'

            })
     .state('profile.subscribe', {
                url: "/subscribe",
                templateUrl: route+"stripe/payment.html",
                controller:'StripeController',
                data:{
                    action:'subscribe'
                }

            })
             .state('profile.card', {
                url: "/card",
                templateUrl: route+"stripe/payment.html",
                 controller:'StripeController',
                data:{
                    action:'changecard'
                }

            })
    //$routeProvider.when('/', {
    //    templateUrl: '/static/assets/tpl/dashboard.html'
    //}).when('/:folder/:tpl', {
    //    templateUrl: function (attr) {
    //        return '/static/assets/tpl/' + attr.folder + '/' + attr.tpl + '.html';
    //    }
    //}).when('/:tpl', {
    //    templateUrl: function (attr) {
    //        return '/static/assets/tpl/' + attr.tpl + '.html';
    //    }
    //}).otherwise({redirectTo: '/'});
}])
// google maps
    .config(['uiGmapGoogleMapApiProvider', function (uiGmapGoogleMapApiProvider) {
        uiGmapGoogleMapApiProvider.configure({
            //    key: 'your api key',
            v: '3.17',
            libraries: 'weather,geometry,visualization'
        });
    }])

// loading bar settings
    .config(['cfpLoadingBarProvider', function (cfpLoadingBarProvider) {
        cfpLoadingBarProvider.includeSpinner = false;
        cfpLoadingBarProvider.latencyThreshold = 300;
    }])

// defaults for date picker
    .config(['$datepickerProvider', function ($datepickerProvider) {
        angular.extend($datepickerProvider.defaults, {
            dateFormat: 'dd/MM/yyyy',
            iconLeft: 'md md-chevron-left',
            iconRight: 'md md-chevron-right',
            autoclose: true
        });
    }])

// defaults for date picker
    .config(['$timepickerProvider', function ($timepickerProvider) {
        angular.extend($timepickerProvider.defaults, {
            timeFormat: 'HH:mm',
            iconUp: 'md md-expand-less',
            iconDown: 'md md-expand-more',
            hourStep: 1,
            minuteStep: 1,
            arrowBehavior: 'picker',
            modelTimeFormat: 'HH:mm'
        });
    }])

// disable nganimate with adding class
    .config(['$animateProvider', function ($animateProvider) {
        $animateProvider.classNameFilter(/^(?:(?!ng-animate-disabled).)*$/);
    }])


// set constants
    .
    run(['$rootScope', 'APP','NomenclatorService', function ($rootScope, APP,NomenclatorService) {
        $rootScope.APP = APP;

        NomenclatorService.getAll('prefix')
            .success(function (data, status, headers, config) {
                $rootScope.preffixs = data;
            });

        NomenclatorService.getAll('suffix')
            .success(function (data, status, headers, config) {
                $rootScope.suffixs = data;
            });



    }]);
