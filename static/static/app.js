angular.module('MyApp', ['ngResource', 'ngMessages', 'ui.router', 'ui.bootstrap', 'angucomplete', 'mgcrea.ngStrap','ngVis', 'satellizer'])
    .config(function ($stateProvider, $urlRouterProvider, $authProvider) {
        $stateProvider
            .state('home', {
                url: '/',
                templateUrl: 'partials/home.html'
            })
            .state('login', {
                url: '/login',
                templateUrl: 'partials/login.html',
                controller: 'LoginCtrl'
            })
            .state('signup', {
                url: '/signup',
                templateUrl: 'partials/signup.html',
                controller: 'SignupCtrl'
            })

            .state('result', {
                url: '/result',
                templateUrl: 'partials/result.html',
                controller: 'ResultCtrl'
            })
            .state('logout', {
                url: '/logout',
                template: null,
                controller: 'LogoutCtrl'
            })
            .state('profile', {
                url: '/profile',
                templateUrl: 'partials/profile.html',
                controller: 'ProfileCtrl',
                resolve: {
                    authenticated: function ($q, $location, $auth) {
                        var deferred = $q.defer();

                        if (!$auth.isAuthenticated()) {
                            $location.path('/login');
                        } else {
                            deferred.resolve();
                        }

                        return deferred.promise;
                    }
                }
            });

        $urlRouterProvider.otherwise('/');

        $authProvider.facebook({
            clientId: '453741414776491'
        });

        $authProvider.google({
            clientId: "814523380763-0g3d7vr9v8ib4fu6dp7n70n0g4vq2akp.apps.googleusercontent.com"
        });

        $authProvider.github({
            clientId: 'ae74dcda4418f13dfcae'
        });

        $authProvider.linkedin({
            clientId: '77k4yo74vjgfsy'
        });

        $authProvider.yahoo({
            clientId: 'dj0yJmk9SDVkM2RhNWJSc2ZBJmQ9WVdrOWIzVlFRMWxzTXpZbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD0yYw--'
        });

        $authProvider.twitter({
            url: '/auth/twitter'
        });


        $authProvider.live({
            clientId: '000000004C12E68D'
        });

        $authProvider.oauth2({
            name: 'foursquare',
            url: '/auth/foursquare',
            clientId: 'MTCEJ3NGW2PNNB31WOSBFDSAD4MTHYVAZ1UKIULXZ2CVFC2K',
            redirectUri: window.location.origin || window.location.protocol + '//' + window.location.host,
            authorizationEndpoint: 'https://foursquare.com/oauth2/authenticate'
        });
    });
