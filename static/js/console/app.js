'use strict';

var app = angular.module('JobApp', [
     'ui.router'
 ])
 
 app.config(function ($stateProvider, $urlRouterProvider) {
     // For any unmatched url, send to /route1
     $urlRouterProvider.otherwise("/");
     $stateProvider
         .state('index', {
             url: "/",
             templateUrl: "/static/console/mainpage.html",
             controller: "MainPageCtrl"
         })
 
 })
 
 app.controller("MainPageCtrl", ['$scope',
 function ($scope) {
 
 }])// end controller
