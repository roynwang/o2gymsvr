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
Date.isLeapYear = function(year) {
    return (((year % 4 === 0) && (year % 100 !== 0)) || (year % 400 === 0));
};

Date.getDaysInMonth = function(year, month) {
    return [31, (Date.isLeapYear(year) ? 29 : 28), 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month];
};

Date.prototype.isLeapYear = function() {
    return Date.isLeapYear(this.getFullYear());
};

Date.prototype.getDaysInMonth = function() {
    return Date.getDaysInMonth(this.getFullYear(), this.getMonth());
};

Date.prototype.addMonths = function(value) {
    var n = this.getDate();
    this.setDate(1);
    this.setMonth(this.getMonth() + value);
    this.setDate(Math.min(n, this.getDaysInMonth()));
    return this;
};

var TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]

var app = angular.module('JobApp', [
    'ui.router',
    'restangular',
    'jkuri.slimscroll',
    "ngTable",
    'ui.bootstrap',
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
        .state('salarysetting', {
            url: "/salarysetting",
            templateUrl: "/static/console/salarysetting.html",
        })
        .state('salarysummary', {
            url: "/salarysummary",
            templateUrl: "/static/console/salarysummary.html",
        })
})
app.controller("SalarySummaryCtrl", ['$scope', "Restangular", "NgTableParams",
    function($scope, Restangular, NgTableParams, ngTableSimpleList) {
        var gymid = $.cookie("gym")
        var that = this

        function calSum(data) {
            console.log(data)
            return (data.base_salary * (100 - data.yanglao - data.yiliao - data.shiye - data.gongjijin) + data.sale.sold * data.xiaoshou + data.sale.sold_xu * data.xuke) / 100

        }
        Restangular.one('api/g/', gymid)
            .one("salary/")
            .get()
            .then(function(data) {
                $.each(data, function(i) {
                    data[i].sum = calSum(data[i])
                })
                that.tableParams = new NgTableParams({
                    sorting: {
                        name: "asc"
                    }
                }, {
                    dataset: data
                });
            })

        that.startday = new Date().addMonths(-1)
        that.endday = new Date();
        that.open = function($event) {
            if ($event == "start") {
                that.startopened = true
            } else {
                that.endopened = true
            }
        };
        that.startopend = false
        that.endopend = false
    }

])

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
    }
])
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
    function($scope, Restangular, NgTableParams) {
        var gymid = $.cookie("gym")
        var self = this
        var originalData = []
        Restangular.one('api/g/', gymid)
            .one("salarysetting/")
            .get()
            .then(function(data) {
                originalData = data
                self.tableParams = new NgTableParams({
                    sorting: {}
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

        function resetRow(row, rowForm) {
            row.isEditing = false;
            rowForm.$setPristine();
            //self.tableTracker.untrack(row);
            for (var i in originalData) {
                if (originalData[i].id === row.id) {
                    return originalData[i]
                }
            }
            /*
            return _.findWhere(originalData, function(r) {
                return r.id === row.id;
            });
			*/
        }

        function del(row) {
            _.remove(self.tableParams.settings().dataset, function(item) {
                return row === item;
            });
            self.tableParams.reload().then(function(data) {
                if (data.length === 0 && self.tableParams.total() > 0) {
                    self.tableParams.page(self.tableParams.page() - 1);
                    self.tableParams.reload();
                }
            });
        }

        function save(row, rowForm) {
            var originalRow = resetRow(row, rowForm);
            angular.extend(originalRow, row);

            //save the row
            console.log(row)

            Restangular.one('api/g/', gymid)
                .all("salarysetting")
                .getList()
                .then(function(data) {
                    var cs = _.find(data, function(obj) {
                        return obj.id === row.id
                    })
                    cs.base_salary = row.base_salary
                    cs.yanglao = row.yanglao
                    cs.yiliao = row.yiliao
                    cs.shiye = row.shiye
                    cs.gongjijin = row.gongjijin
                    cs.xiaoshou = row.xiaoshou
                    cs.xuke = row.xuke
                    cs.patch()
                })

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
