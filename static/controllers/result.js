angular.module('MyApp')
    .controller('ResultCtrl', function ($scope, Shared, $rootScope, $http, $q) {


        if ($rootScope.selected) {
            $scope.user = $rootScope.selected.originalObject;
            console.log($scope.user);
            $scope.height
            $scope.options =
            {
                stabilize: false,
                navigation: true,
                keyboard: true,
                width: "1024px",
                height: "700px",
                groups: {
                    values: {
                        color: 'red',
                        fontColor: 'black'
                    },
                    needs: {
                        color: {
                            border: 'black',
                            background: 'green',
                            highlight: {
                                border: 'black',
                                background: 'lightgray'
                            }
                        }
                    },
                    personality: {
                        color: {
                            border: 'black',
                            background: 'yellow'
                        },
                        fontColor: 'red'
                    }
                }

            };

            //var promise1 = $http({method: 'GET', url: "api/v1/personality/" + $scope.user.screen_name, cache: 'true'});
            var promise2 = $http({method: 'GET', url: "api/v1/interests/" + $scope.user.screen_name, cache: 'true'});
            var promise1 = $http({method: 'GET', url:"data/personality.json"  });
            // var promise2 = $http({method: 'GET', url: "data/interests.json" });

            $q.all([promise1, promise2]).then(function (data) {
                console.log(data[0], data[1]);
                $scope.profile = data[0].data;
                $scope.interests = data[1].data;
                $scope.draw()
            });
            $scope.draw = function () {

                var nodes = [
                    {
                        id: "person",
                        value: 400,
                        label: $scope.user.name,
                        shape: 'circularImage',
                        image: $scope.user.profile_image_url
                    },
                    {id: "interests", value: 300, label: 'interests', shape: 'circle'},
                    {id: 'people', value: 300, label: 'people', shape: 'circle'}


                ];
                // create an array with edges
                var edges = [
                    {from: "person", to: "interests"},
                    {from: "person", to: 'people'},
                    {from: "person", to: 'r'},
                ];


                nodes = nodes.concat($scope.profile.nodes);
                edges = edges.concat($scope.profile.edges);

                nodes = nodes.concat($scope.interests.nodes);
                edges = edges.concat($scope.interests.edges);


                // create a network
                $scope.data = {nodes: new vis.DataSet(nodes), edges: new vis.DataSet(edges)};

                console.log($scope.data)

            }
        }

    });