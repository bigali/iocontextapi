'use strict';

var myapp = angular.module('myapp', ["highcharts-ng"]);

myapp.controller('myctrl', function ($scope, $http) {

    $http.get('api/v1/bar').success(function (data) {
        var personalitydata = data.data;
        personalitydata.sort(function (a, b) {
            if (a[1] > b[1])
                return -1;
            if (a[1] < b[1])
                return 1;
            // a doit être égale à b
            return 0;
        });
        $scope.chartConfig = {
            "options": {"chart": {"type": "bar"}},
            series: [
                {
                    name: 'Personality',
                    data: personalitydata,
                    dataLabels: {
                        enabled: true,
                        color: '#FFFFFF',
                        align: 'right',
                        format: '{point.y:.1f}', // one decimal
                        y: 10, // 10 pixels down from the top
                        style: {
                            fontSize: '13px',
                            fontFamily: 'Verdana, sans-serif'
                        }
                    }
                }

            ],
            xAxis: {
                type: 'category',
                labels: {
                    style: {
                        fontSize: '13px',
                        fontFamily: 'Verdana, sans-serif'
                    }
                }
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'personality note'
                }
            },
            "title": {"text": "personality insight"},
            "credits": {"enabled": false},
            "loading": false,
            "size": {"width": "800", "height": "600"},
            "subtitle": {"text": "by hallak sidali"}
        }
    })


});