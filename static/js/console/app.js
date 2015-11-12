'use strict';
// 对Date的扩展，将 Date 转化为指定格式的String 
// 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符， 
// 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字) 
// 例子： 
// (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423 
// (new Date()).Format("yyyy-M-d h:m:s.S")      ==> 2006-7-2 8:9:4.18 
Date.prototype.Format = function(fmt) { //author: meizz 
    var o = {
        "M+": this.getMonth() + 1, //月份 
        "d+": this.getDate(), //日 
        "h+": this.getHours(), //小时 
        "m+": this.getMinutes(), //分 
        "s+": this.getSeconds(), //秒 
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度 
        "S": this.getMilliseconds() //毫秒 
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}

var TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]

var app = angular.module('JobApp', [
    'ui.router',
    'restangular',
    'jkuri.slimscroll',
    "ngTable"
])
app.config(function($stateProvider, $urlRouterProvider, RestangularProvider) {
    // For any unmatched url, send to /route1
    RestangularProvider.setDefaultHeaders({
        Authorization: "JWT " + $.cookie("token")
    });
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/console/mainpage.html",
            controller: "MainPageCtrl"
        })
        .state('customers', {
            url: "/customers",
            templateUrl: "/static/console/customers.html",
        })
        .state('sale', {
            url: "/sale",
            templateUrl: "/static/console/sale.html",
        })
        .state('salary', {
            url: "/salary",
            templateUrl: "/static/console/salarysetting.html",
        })
})

app.controller("CoachSaleCtrl", ['$scope', "Restangular", "NgTableParams",
    function($scope, Restangular, NgTableParams, ngTableSimpleList) {
        var gymid = $.cookie("gym")
        Restangular.one('api/g/', gymid).get().then(function(gym) {
                    $scope.coaches = gym.coaches_set
                    $.each($scope.coaches, function(i, item) {
                        //render income
                        Restangular.one("api/", item.name).one("income/").get().then(function(data) {
                            $scope.coaches[i].income = data
                        })
					})
		})
	}])
app.controller("CustomerCtrl", ['$scope', "Restangular", "NgTableParams",
    function($scope, Restangular, NgTableParams, ngTableSimpleList) {
        var gymid = $.cookie("gym")
		var that = this
        Restangular.one('api/g/', gymid)
            .one("customers/")
            .get()
            .then(function(data) {
                that.tableParams = new NgTableParams({
                    sorting: {
                        name: "asc"
                    }
                }, {
                    dataset: data
                });
            })
    }
])
app.controller("SalarySettingCtrl", ['$scope', "Restangular", "NgTableParams",
    function($scope, Restangular, NgTableParams, ngTableSimpleList) {
        var gymid = $.cookie("gym")
		var that = this
	    var originalData = []
        Restangular.one('api/g/', gymid)
            .one("salarysetting/")
			.get()
            .then(function(data) {
				originalData = data
                that.tableParams = new NgTableParams({
                    sorting: {
                    }
                }, {
                    dataset: angular.copy(originalData)
                });
            })
    self.cancel = cancel;
    self.save = save;

    //////////

    function cancel(row, rowForm) {
      var originalRow = resetRow(row, rowForm);
      angular.extend(row, originalRow);
    }
    
    function resetRow(row, rowForm){
      row.isEditing = false;
      rowForm.$setPristine();
      self.tableTracker.untrack(row);
      return _.findWhere(originalData, function(r){
        return r.id === row.id;
      });
    }

    function save(row, rowForm) {
      var originalRow = resetRow(row, rowForm);
      angular.extend(originalRow, row);
    }
    }
])

app.controller("MainPageCtrl", ['$scope', "Restangular",
        function($scope, Restangular) {
            //var date = new Date().format("yyyy-MM-dd");
            var date = "20151029"
            $scope.calendarRowGroup = []
            var g = -1

            $scope.coursecount = 0

            function renderSale() {
                var gymid = $.cookie("gym")
                Restangular.one('api/g/', gymid)
                    .one("sold/", date)
                    .get()
                    .then(function(data) {
                        $scope.sale = data
                    })
            }

            function renderCoaches() {
                var gymid = $.cookie("gym")
                Restangular.one('api/g/', gymid).get().then(function(gym) {
                    $scope.coaches = gym.coaches_set
                    $.each($scope.coaches, function(i, item) {
                        //render income
                        Restangular.one("api/", item.name).one("income/").get().then(function(data) {
                            $scope.coaches[i].income = data
                        })

                        //render booked schedule
                        Restangular.one("api/", item.name).one("b/", date).get().then(function(data) {
                            $scope.coaches[i].books = data
                            $scope.coursecount += data.length
                            if (i % 2 == 0) {
                                $scope.calendarRowGroup.push([])
                                g += 1
                            }
                            $scope.calendarRowGroup[g].push($scope.coaches[i])
                            $scope.timemap = TimeMap
                        })

                        //render the today income
                    })
                    console.log($scope.coaches)
                })
            }

            function recur() {
                if (!$.cookie("user")) {
                    setTimeout(recur, 1000)
                } else {
                    renderCoaches()
                    renderSale()
                }
            }
            recur()
        }
    ]) // end controller
