angular.module('MyApp')
    .controller('NavbarCtrl', function ($scope, $rootScope, $auth, Shared, $location) {
        /*$scope.users = [
            {
                "description": "Sharing things I'm learning through my foundation work and other interests...",
                "name": "Bill Gates",
                "profile_image_url": "images/j1f9DiJi_normal.jpeg",
                "screen_name": "BillGates"
            }
        ];*/
        $scope.selectedUser = "";
        $scope.isAuthenticated = function () {
            return $auth.isAuthenticated();
        };

        $scope.go = function () {
            $location.path('/home');
            Shared.set($scope.selectedUser);
            $rootScope.selected = $scope.selectedUser;
            $location.path('/result');



        }


    });