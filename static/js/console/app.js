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
app.directive('backButton', function() {
    return {
        restrict: 'A',
        link: function(scope, element, attrs) {
            element.bind('click', goBack);

            function goBack() {
                history.back();
                scope.$apply();
            }
        }
    }
});

app.config(function($stateProvider, $urlRouterProvider, RestangularProvider) {
    // For any unmatched url, send to /route1
    RestangularProvider.setDefaultHeaders({
        Authorization: "JWT " + $.cookie("token")
    });
    RestangularProvider.setRequestSuffix('/')
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
        .state('neworder', {
            url: "/neworder/:coachname",
            templateUrl: "/static/console/neworder.html",
        })
        .state('orderdetail', {
            url: "/order/:coachname/:orderid",
            templateUrl: "/static/console/order.html",
        })
})
app.controller("OrderDetailCtrl", ['$scope', "Restangular", "NgTableParams", '$stateParams',
    function($scope, Restangular, NgTableParams, $stateParams) {
        console.log($stateParams)
        var that = this
        var coachname = $stateParams.coachname
        var orderid = $stateParams.orderid
        that.booked = []
        that.done = []
        that.sum = 0
        that.product = null
        that.day = new Date()
        that.availiable = []


        that.newadd = []
        that.newremove = []

        that.open = function() {
            that.dayopened = true
        };
        that.dayopened = false

        that.cancelbook = function(date, hour) {
            var t = _.findWhere(that.tableParams.data, {
                date: date,
                hour: hour
            })
            that.tableParams.data = that.tableParams.data.splice(that.tableParams.data.indexOf(t), 1)
            that.newadd.data = _.without(that.tableParams.data, t)
            if (t != undefined && t.date == that.day.Format("yyyy-MM-dd")) {
                that.availiable.push(hour)
                that.availiable.push(hour + 1)
                that.refreshtimetable(true)

                that.tableParams.total(that.tableParams.data.length)
                that.tableParams.reload()
            }
        }

        that.book = function(i) {
            console.log(i)
            if (that.availiable.indexOf(i) >= 0 && that.availiable.indexOf(i + 1) >= 0) {
                //update availiable
                that.availiable.splice(that.availiable.indexOf(i), 1)
                that.availiable.splice(that.availiable.indexOf(i + 1), 1)

                that.refreshtimetable(true)
                    //update newadd and booked
                that.tableParams.data.push({
                    date: that.day.Format("yyyy-MM-dd"),
                    hour: i
                })
                that.newadd.push({
                    date: that.day.Format("yyyy-MM-dd"),
                    hour: i
                })

                that.tableParams.total(that.tableParams.data.length)
                console.log(that.tableParams.data)
            }
        }
        that.refreshtimetable = function(norefresh) {
            function t(ava) {
                that.timemapgroup = []
                for (var i = 0; i < TimeMap.length; i++) {
                    if (i % 5 == 0) {
                        that.timemapgroup.push([])
                    }
                    // if in ava or in newadd

                    if (ava.indexOf(i) >= 0 || i == 26) {
                        that.timemapgroup[Math.floor(i / 5)].push({
                            id: i,
                            status: false
                        })
                    } else {
                        that.timemapgroup[Math.floor(i / 5)].push({
                            id: i,
                            status: true
                        })
                    }
                }
                console.log(that.timemapgroup)
            }
            if (norefresh) {
                t(that.availiable)
            } else {
                Restangular.one("api/", coachname)
                    .one("d/", that.day.Format("yyyyMMdd"))
                    .get()
                    .then(function(data) {
                        that.availiable = data.availiable
                        t(that.availiable)
                    })
            }
        }

        that.refreshtimetable()

        Restangular.one("api/", coachname)
            .one("o/", orderid)
            .get()
            .then(function(data) {
                that.coach = data.coachdetail
                    //get product
                Restangular.one("api/p", data.product)
                    .get()
                    .then(function(product) {
                        that.product = product
                        that.sum = product.amount
                            //get booked

                        console.log(data.booked)
                        that.booked = _.where(data.booked, {
                            done: false
                        })
                        that.done = _.where(data.booked, {
                            done: true
                        })

                        $scope.timemap = TimeMap
                        that.tableParams = new NgTableParams({

                            sorting: {
                                name: "asc"
                            }
                        }, {
                            dataset: data.booked
                        });
                    })
            })

    }
])

app.controller("NewOrderCtrl", ['$scope', "Restangular", "NgTableParams", '$stateParams','$state',
    function($scope, Restangular, NgTableParams, $stateParams,$state) {
        console.log($stateParams)
        var that = this
        var coachname = $stateParams.coachname
        that.mo = {}
        that.mo.customer_displayname = ""
        that.mo.customer_phone = ""
        that.mo.product_introduction = ""
        that.mo.product_price = ""
        that.mo.product_promotion = 0
        that.mo.product_amount = ""
        Restangular.one("api/", coachname)
            .get()
            .then(function(data) {
                that.coach = data
            })
        that.submitorder = function() {
            Restangular.one("api/", coachname)
                .post("manualorder",that.mo)
                .then(function(data) {
                    console.log(data)
					$state.transitionTo('orderdetail',{coachname:coachname,orderid:data.id})
                })
        }
    }
])

app.controller("SalarySummaryCtrl", ['$scope', "Restangular", "NgTableParams",
    function($scope, Restangular, NgTableParams) {
        var gymid = $.cookie("gym")
        var that = this
        that.startday = new Date().addMonths(-1)
        that.endday = new Date();

        function calSum(data) {
            console.log(data)
            return (data.base_salary * (100 - data.yanglao - data.yiliao - data.shiye - data.gongjijin) + data.sale.sold * data.xiaoshou + data.sale.sold_xu * data.xuke) / 100

        }

        function refresh() {
            Restangular.one('api/g/', gymid)
                .one("salary/")
                .get({
                    start: that.startday.Format("yyyyMMdd"),
                    end: that.endday.Format("yyyyMMdd")
                })
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
        }

        refresh()
        that.refresh = refresh

        that.open = function($event) {
            if ($event == "start") {
                that.startopened = true
            } else {
                that.endopened = true
            }
        };
        that.startopened = false
        that.endopened = false
    }

])

app.controller("CoachSaleCtrl", ['$scope', "Restangular", "NgTableParams",
    function($scope, Restangular, NgTableParams, ngTableSimpleList) {
        var gymid = $.cookie("gym")
        var that = this
        that.startday = new Date().addMonths(-1)
        that.endday = new Date();

        function calSum(data) {
            console.log(data)
            return (data.base_salary * (100 - data.yanglao - data.yiliao - data.shiye - data.gongjijin) + data.sale.sold * data.xiaoshou + data.sale.sold_xu * data.xuke) / 100

        }

        function refresh() {
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

        refresh()
        that.refresh = refresh

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
