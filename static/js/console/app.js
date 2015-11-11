'use strict';

var app = angular.module('JobApp', [
     'ui.router',
     'restangular'
 ])
app.config(function ($stateProvider, $urlRouterProvider, RestangularProvider) {
     // For any unmatched url, send to /route1
	 RestangularProvider.setDefaultHeaders({Authorization: "JWT " + $.cookie("token") });
     $urlRouterProvider.otherwise("/");
     $stateProvider
         .state('index', {
             url: "/",
             templateUrl: "/static/console/mainpage.html",
             controller: "MainPageCtrl"
         })
 
 })
 
 app.controller("MainPageCtrl", ['$scope',"Restangular",
 function ($scope, Restangular) {

	 function renderCoaches(){
		var gymid = $.cookie("gym")
        Restangular.one('api/g/', gymid).get().then(function(gym){
			$scope.coaches = gym.coaches_set
			
			$.each($scope.coaches, function(i,item){
				console.log(i)
				Restangular.one("api/",item.name).one("income/").get().then(function(data){
					$scope.coaches[i].income = data
				})
			})
			console.log($scope.coaches)
		})
		
     }
	 function recur(){
		 if(!$.cookie("user")){
			setTimeout(recur, 1000)
		 }else {
	 		renderCoaches()
		}
	 }
	 recur()
 }])// end controller
