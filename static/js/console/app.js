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
Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf());
    dat.setDate(dat.getDate() + days);
    return dat;
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
    'oitozero.ngSweetAlert',
    'angular-ladda'
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
app.factory("$login", function(Restangular) {
    function login(username, pwd, onsuccess, onfail) {
        Restangular.one("api")
            .post("lg", {
                username: username,
                password: pwd
            })
            .then(onsuccess, onfail)
    }
    return {
        login: login
    }
})

app.factory("$customersvc", function(Restangular) {
    var customers = []

    function getcustomers(onsuccess, force) {
        if (force == true || customers.length == 0) {
            var gymid = $.cookie("gym")
            var that = this
            Restangular.one('api/g/', gymid)
                .one("customers/")
                .get()
                .then(function(data) {
                    customers = data
                    onsuccess && onsuccess(customers)
                })
        } else {
            onsuccess && onsuccess(customers)
        }
    }

    function getcustomer(key) {}
    return {
        getcustomers: getcustomers,
        getcustomer: getcustomer
    }
})

app.config(function($stateProvider, $urlRouterProvider, RestangularProvider, $httpProvider) {
    // For any unmatched url, send to /route1
    RestangularProvider.setDefaultHeaders({
        Authorization: "JWT " + $.cookie("token")
    });
    //$httpProvider.defaults.headers.common.Authorization = "JWT " + $.cookie("token")
    RestangularProvider.setRequestSuffix('/')
	RestangularProvider.setDefaultHttpFields({timeout: 10000})
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/console/mainpage.html",
            controller: "MainPageCtrl"
        })
        .state('gym', {
            url: "/gym/:gymid",
            controller: "GymCtrl"
                //templateUrl: "/static/console/customers.html",
        })
        .state('customers', {
            url: "/customers",
            templateUrl: "/static/console/customers.html",
        })
        .state('customerorders', {
            url: "/customer/:customername/orders",
            templateUrl: "/static/console/customerorders.html",
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
        .state('feedback', {
            url: "/feedback",
            templateUrl: "/static/console/feedback.html",
        })
        .state('coaches', {
            url: "/coaches",
            templateUrl: "/static/console/coaches.html",
        })
        .state('coachecalendar', {
            url: "/coach/:coachid/calendar",
            templateUrl: "/static/console/coachcalendar.html",
        })
        .state('newgym', {
            url: "/newgym",
            templateUrl: "/static/console/newgym.html",
        })
})

app.controller("GymCtrl", ["$stateParams", "$state",
    function($stateParams, $state) {
        $.cookie("gym", $stateParams.gymid, {
            path: "/"
        })
        refreshcorner()
		getincomplete()
        $state.transitionTo("index")
            //window.location = "/console/dashboard/"
    }
])
app.controller("CustomerOrdersCtrl", ['$scope', "Restangular", "NgTableParams", "$stateParams", "SweetAlert",
    function($scope, Restangular, NgTableParams, $stateParams, SweetAlert) {
        var that = this
        that.coaches = []
        that.coach = {}

        Restangular.one('api/g/', $.cookie("gym")).get().then(function(gym) {
            that.coaches = gym.coaches_set
        })

        that.statusmap = {
            "inprogress": "进行中",
            "unpaid": "待支付",
            "paid": "待预约",
            "done": "已完成"
        }
        that.changecoach = function(c, coach) {
			if(c.coach == coach.name){
				return
			}
            swal({
                    title: "修改教练",
                    text: "确定修改订单至" + coach.displayname + "吗?",
                    type: "warning",
                    showLoaderOnConfirm: true,
                    showCancelButton: true,
                    confirmButtonText: "保存",
                    cancelButtonText: "取消",
                    closeOnConfirm: false,
                },
                function(yes) {
                    if (!yes) {
                        return
                    }
					var pdata = {
						coach: coach.id
					}
                    Restangular.one("api", $stateParams.customername)
                        .one("o", c.id)
                        .patch(pdata)
                        .then(function(data) {
                                swal({
                                    title: "成功",
                                    text: "修改已保存",
                                    type: "success",
                                    timer: 1500,
                                    showConfirmButton: false
                                });
                                that.refresh()
                            },
                            function(data) {
                                swal("", "保存失败了",
                                    "warning")
                            })
                })
        }
        that.refresh = function() {
            Restangular.one('api/', $stateParams.customername)
                .one("o/")
                .get()
                .then(function(data) {
                    _.map(data.results, function(item) {
                        if (eval(item.complete_status) == 1) {
                            item.status = "done"
                        }
                        item["removable"] = false
                        if (eval(item.complete_status) == 0) {
                            item["removable"] = true
                        }
                    })
                    that.tableParams = new NgTableParams({
                        sorting: {}
                    }, {
                        dataset: data.results
                    });
                })
        }
        that.modify = function(c, type) {
            var tx = ""
            var v = ""
            if (type == "duration") {
                tx = "有效时间(月)"
                v = c.duration
            } else {
                tx = "价格(元)"
                v = c.amount
            }
            swal({
                    title: "修改订单",
                    text: "请输入订单新" + tx,
                    type: "input",
                    showLoaderOnConfirm: true,
                    showCancelButton: true,
                    confirmButtonText: "保存",
                    cancelButtonText: "取消",
                    closeOnConfirm: false,
                    inputPlaceholder: v
                },
                function(inputValue) {
                    if (inputValue === false) return false;
                    inputValue = parseInt(inputValue)
                    if (inputValue == undefined && inputValue.isNaN()) {
                        swal.showInputError("请输入合法的数字");
                        return false
                    }
                    var pdata = {}
                    if (type == "duration") {
                        pdata["duration"] = inputValue
                    }
                    if (type == "price") {
                        pdata["amount"] = inputValue
                    }

                    Restangular.one("api", $stateParams.customername)
                        .one("o", c.id)
                        .patch(pdata)
                        .then(function(data) {
                                swal({
                                    title: "成功",
                                    text: "修改已保存",
                                    type: "success",
                                    timer: 1500,
                                    showConfirmButton: false
                                });
                                that.refresh()
                            },
                            function(data) {
                                swal("", "保存失败了",
                                    "warning")
                            })
                })
        }

        that.remove = function(orderid) {
            SweetAlert.swal({
                    //title: "确定移除该教练吗?",
                    title: "",
                    text: "确定移除该订单吗?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#1fb5ad",
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    showLoaderOnConfirm: true,
                    closeOnConfirm: false
                },
                function(yes) {
                    if (!yes) {
                        return
                    }
                    Restangular.one("api", $stateParams.customername)
                        .one("o", orderid)
                        .remove()
                        .then(function(data) {
                                swal({
                                    title: "成功",
                                    text: "订单已经移除",
                                    type: "success",
                                    timer: 1500,
                                    showConfirmButton: false
                                });
                                that.refresh()
                            },
                            function(data) {
                                swal("", "删除失败了",
                                    "warning")
                            })
                })
        }
        that.refresh()
    }
])
app.controller("CoachesControl", ['$scope', "Restangular", "$uibModal", "SweetAlert",
    function($scope, Restangular, $uibModal, SweetAlert) {
        var that = this
        var gymid = $.cookie("gym")

        that.loadcoaches = function() {
            Restangular.one("api/g", gymid)
                .get()
                .then(function(data) {
                    that.rowcount = Math.ceil((data.coaches_set.length + 1) / 3)
                    that.coaches = data.coaches_set
                    that.rows = _.range(0, that.rowcount)
                })
        }
        that.remove = function(c) {
            SweetAlert.swal({
                    //title: "确定移除该教练吗?",
                    title: "",
                    text: "确定移除该教练吗?",
                    type: "warning",
                    showLoaderOnConfirm: true,
                    showCancelButton: true,
                    confirmButtonColor: "#1fb5ad",
                    confirmButtonText: "移除",
                    cancelButtonText: "取消",
                    closeOnConfirm: false
                },
                function(yes) {
                    if (!yes) {
                        return
                    }
                    Restangular.one("api/", c.name)
                        .post("gym", {})
                        .then(function(data) {
                            Restangular.one("api/g/", $.cookie("gym"))
                                .one("sync")
                                .get()
                                //$state.transitionTo('coaches')
                            that.loadcoaches()
                            SweetAlert.swal("", "移除完成", "success");
                        })
                });
        }

        that.loadcoaches()

        that.newcoach = function(size) {
            var modalInstance = $uibModal.open({
                animation: $scope.animationsEnabled,
                templateUrl: 'newcoach.html',
                controller: 'NewCoachCtrl',
                size: size,
                resolve: {
                    reload: function() {
                        return that.loadcoaches
                    },
                    test: function() {
                        return "hahah"
                    }
                }
            });
        }

    }
])
app.controller('NewCoachCtrl', function($scope, Restangular, $uibModalInstance, reload, test) {
    console.log(test)
    $scope.newcoach = {
        displayname: "",
        name: "",
        iscoach: true
    }

    function changeGym(coachphone, gymid) {
        Restangular.one("api/", $scope.newcoach.name)
            .post("gym", {
                gym: $.cookie("gym")
            })
            .then(function(data) {
                $uibModalInstance.close("");
                Restangular.one("api/g/", $.cookie("gym"))
                    .one("sync")
                    .get()
                    //$state.transitionTo('coaches')
                reload()
            })
    }
    $scope.ok = function() {
        Restangular.one("api/")
            .post("u", $scope.newcoach)
            .then(function(data) {
                    //set the gym
                    changeGym($scope.newcoach.name, $.cookie("gym"))
                },
                function(res) {
                    changeGym($scope.newcoach.name, $.cookie("gym"))
                }
            )
    };

    $scope.cancel = function() {
        $uibModalInstance.dismiss('cancel');
    };
})

app.controller("FeedbackControl", ['$scope', "Restangular",
    function($scope, Restangular) {
        this.feedback = {}
        this.feedback.feedback = ""
        this.feedback.name = $.cookie("user")
        this.submitFeedback = function() {
            Restangular.one("api/")
                .post("fb", this.feedback)
                .then(function(data) {
                    console.log("submit feedback success")
                })
        }
    }
])

app.controller("OrderDetailCtrl", ['$scope', "Restangular", "NgTableParams", '$stateParams', '$state', 'SweetAlert', "$http",
    function($scope, Restangular, NgTableParams, $stateParams, $state, SweetAlert, $http) {
        console.log($stateParams)
        var that = this
        var coachname = $stateParams.coachname
        var orderid = $stateParams.orderid

        that.showncoaches = false
        that.changecoach = function(c) {
            that.coach = c
            coachname = c.name
            that.refreshtimetable()
        }
        Restangular.all("api")
            .one("g", $.cookie("gym"))
            .get()
            .then(function(data) {
                    that.gym = data
                },
                function(data) {})
        Restangular.one("api", coachname)
            .get()
            .then(function(data) {
                that.coach = data
            })


        $scope.timemap = TimeMap

        that.booked = []
        that.done = []
        that.sum = 0
        that.product = null
        that.order = null
        that.day = new Date()
        that.availiable = []

        that.open = function() {
            that.dayopened = true
        };
        that.dayopened = false

        that.gohome = function() {
            $state.transitionTo('index')
        }
        that.pendingaction = 0

        that.completeditem = function() {
            that.pendingaction--
                if (that.pendingaction == 0) {
                    that.submitting = false
                    swal({
                        type: "success",
                        title: "提交成功",
                        text: "",
                        timer: 1500,
                        showConfirmButton: false
                    });
                    that.reload()
                }

        }

        that.submitBook = function() {
            swal({
                title: "提交",
                text: "确认提交预约请求吗?",
                type: "warning",
                showCancelButton: true,
                cancelButtonText: "取消",
                confirmButtonText: "确认",
                confirmButtonColor: "#1fb5ad",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function() {
                var removelist = _.where(that.tableParams.data, {
                    pendingaction: "remove"
                })
                var addlist = _.where(that.tableParams.data, {
                    pendingaction: "add"
                })
                that.pendingaction = removelist.length + addlist.length
                if (that.pendingaction == 0) {
                    return
                } else {
                    that.submitting = true
                }

                _.each(removelist, function(item, i) {
                    var datestr = item.date.replace(/-/g, "")
                    Restangular.one("api/", item.coachprofile.name)
                        .one("b/" + datestr, item.hour)
                        .remove()
                        .then(function(data) {
                            console.log("remove success")
                            that.completeditem()
                        })
                })
                _.each(addlist, function(item, i) {
                    var datestr = item.date.replace(/-/g, "")
                    item.coach = item.coachprofile.id
                    item.custom = that.order.customerdetail.id
                    item.order = that.order.id
                    Restangular.one("api/", item.coachprofile.name)
                        .post("b/" + datestr, item)
                        .then(function(data) {
                            that.completeditem()
                            console.log(data)
                        })
                })
            })

        }
        that.bookComplete = function(date, hour) {
            var time_obj = Date.parse(date + " " + TimeMap[hour] + ":00") + 60 * 60 * 8
            var now = Date.now()
            if (time_obj > now) {
                swal({
                    type: "warning",
                    title: "",
                    text: "未到课程开始时间，无法完成课程",
                });
                return
            }

            SweetAlert.swal({
                    //title: "确定移除该教练吗?",
                    title: "确认",
                    text: "这节课已经上完了吗?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#1fb5ad",
                    confirmButtonText: "完成",
                    cancelButtonText: "取消",
                    showLoaderOnConfirm: true,
                    closeOnConfirm: false
                },
                function(yes) {
                    if (!yes) {
                        return
                    }
                    var url = "/api/" + coachname + "/b/" + date.replace(/-/g, "") + "/" + hour + "/";
                    var bookdone = Restangular.one("api", coachname)
                        .one("b", date.replace(/-/g, ""))
                        .all(hour)
                    bookdone.patch({
                            order: orderid,
                            done: true
                        })
                        .then(function(data) {
                            swal({
                                type: "success",
                                title: "课程已完成",
                                text: "",
                                timer: 1500,
                                showConfirmButton: false
                            });
                            that.reload()
							//refresh notification !!!!
							getincomplete()
                        })
                        /*
                    $http.patch(url, {
                            order: orderid,
                            done: true
                        })
                        .then(function(data) {
                            swal({
                                type: "success",
                                title: "课程已完成",
                                text: "",
                                timer: 1500,
                                showConfirmButton: false
                            });
                            that.reload()
                        })
						*/

                });
        }
        that.cancelbook = function(date, hour) {
            var tar = {
                date: date,
                hour: hour
            }
            var b = _.findWhere(that.tableParams.data, tar)
                //set to 'remove' for existed item
            if (b.pendingaction == undefined) {
                b.pendingaction = "remove"
            } else if (b.pendingaction == "add") { //remove directly for new added item
                var i = that.tableParams.data.indexOf(b)
                that.tableParams.data.splice(i, 1)
            }
            that.refreshtimetable(true)
            that.tableParams.total(that.tableParams.data)
                //that.tableParams.reload()
            console.log(that.tableParams.data)
        }
        that.book = function(i) {
            if (!isAva(i, that.availiable) || !isAva(i + 1, that.availiable)) {
                return
            }
            //
            var r = _.filter(that.tableParams.data, function(item) {
                return item.pendingaction != "remove"
            })
            if (r.length == that.sum) {
                return
            }
            that.tableParams.data.push({
                date: that.day.Format("yyyy-MM-dd"),
                hour: i,
                coachprofile: that.coach,
                pendingaction: "add"
            })
            that.tableParams.total(that.tableParams.data)
            that.refreshtimetable(true)
        }
        that.bookvisiable = function(actual, expected) {
            return actual.pendingaction != "remove"
        }

        function isAva(h, ava) {
            if (h == undefined || (h + 1) > TimeMap.length) {
                return false
            }

            for (var i = 0; i < that.tableParams.data.length; i++) {
                var item = that.tableParams.data[i]
                if (that.day.Format("yyyy-MM-dd") == item.date && item.pendingaction == "remove" && (item.hour == h || item.hour + 1 == h)) {
                    return true
                }
                if (
                    item.coachprofile.name == that.coach.name &&
                    that.day.Format("yyyy-MM-dd") == item.date && item.pendingaction != "remove" && (item.hour == h || item.hour + 1 == h)) {
                    return false
                }
            }
            if (ava.indexOf(h) >= 0) {
                return true
            }
            if (h == TimeMap.length - 1) {
                return true
            }
            return false

        }
        that.refreshtimetable = function(norefresh) {
            function t(ava) {
                that.timemapgroup = []
                for (var i = 0; i < TimeMap.length; i++) {
                    if (i % 5 == 0) {
                        that.timemapgroup.push([])
                    }
                    var g = Math.floor(i / 5)
                    if (isAva(i, ava)) {
                        that.timemapgroup[g].push({
                            id: i,
                            status: false
                        })
                    } else {
                        that.timemapgroup[g].push({
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


        that.reload = function() {
            Restangular.one("api/", coachname)
                .one("o/", orderid)
                .get()
                .then(function(data) {
                    //that.coach = data.coachdetail
                    //get product
                    that.order = data
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
                            that.tableParams = new NgTableParams({
                                sorting: {
                                },
                            }, {
                                dataset: data.booked,
                            });
                            that.refreshtimetable()
                        })
                })
        }
        that.reload()
    }
])

app.controller("CoachCalendarCtrl", ['$scope', "Restangular", "NgTableParams", '$stateParams', '$state', '$http',
    function($scope, Restangular, NgTableParams, $stateParams, $state, $http) {
        var that = this

        $scope.timemap = TimeMap
        var date = new Date()
        var coachid = $stateParams.coachid
        that.load = function() {

            that.title = date.Format("yyyy-MM-dd")
            Restangular.one("api", coachid)
                .one("w", date.Format("yyyyMMdd"))
                .get()
                .then(function(data) {
                    that.tableParams = new NgTableParams({
                        sorting: {
                            name: "asc"
                        }
                    }, {
                        dataset: data.results
                    });
                }, function(data) {})
        }
        that.loadprev = function() {
            date = date.addDays(-7)
            that.load()
        }
        that.loadnext = function() {
            date = date.addDays(7)
            that.load()
        }
        that.load()
    }
])

app.controller("NewOrderCtrl", ['$scope', "Restangular", "NgTableParams", '$stateParams', '$state', "SweetAlert", "$customersvc",
    function($scope, Restangular, NgTableParams, $stateParams, $state, SweetAlert, $customersvc) {
        console.log($stateParams)
        var that = this
        var coachname = $stateParams.coachname
        that.mo = {}
        that.mo.customer_displayname = ""
        that.mo.customer_phone = ""
        that.mo.product_introduction = "dummy"
        that.mo.product_price = ""
        that.mo.product_promotion = -1
        that.mo.product_amount = ""
        that.mo.product_duration = ""
        that.mo.sex = '0'
        Restangular.one("api/", coachname)
            .get()
            .then(function(data) {
                that.coach = data
                that.coach.avatar += "?imageView2/1/w/150/h/150"
            })

        function validate() {
            var data = that.mo
            if (that.mo.customer_phone.toString().length != 11) {
                swal("", "请输入正确的11位电话号码", "warning")
                return false
            }
            for (var k in data) {
                if (data[k] == undefined || data[k].length == 0) {
                    swal("", "请填完所有选项", "warning")
                    return false
                }
            }
            return true
        }

        that.submitorder = function() {
            if (!validate()) {
                return
            }
            SweetAlert.swal({
                    //title: "确定移除该教练吗?",
                    title: "提交",
                    text: "确认提交订单吗？",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#1fb5ad",
                    confirmButtonText: "确认",
                    cancelButtonText: "取消",
                    showLoaderOnConfirm: true,
                    closeOnConfirm: false
                },
                function(yes) {
                    if (!yes) {
                        return
                    }
                    Restangular.one("api/", coachname)
                        .post("manualorder", that.mo)
                        .then(function(data) {
                            console.log(data)
                            $customersvc.getcustomers(false, true)
                            swal({
                                title: "成功",
                                text: "订单提交成功",
                                type: "success",
                                timer: 1500,
                                showConfirmButton: false
                            });
                            $state.transitionTo('orderdetail', {
                                coachname: coachname,
                                orderid: data.id
                            })
                        }, function(data) {
                            swal("", "订单保存失败，请检查输入后重试", "warning")
                        })
                })
        }
    }
])

app.controller("SalarySummaryCtrl", ['$scope', "Restangular", "NgTableParams", "$login",
    function($scope, Restangular, NgTableParams, $login) {
        var gymid = $.cookie("gym")
        var that = this
        that.startday = new Date().addMonths(-1)
        that.endday = new Date();

        that.is_admin = false
        that.errmsg = ""
        that.pwd = ""

        that.submit = function() {
            if (that.pwd == undefined || that.pwd.length == 0) {
                that.errmsg("请输入密码")
                return
            }
            $login.login($.cookie("user"), that.pwd,
                function(data) {
                    $.cookie("token", data.token, {
                        path: '/'
                    })
                    that.is_admin = true
                },
                function(data) {
                    that.is_admin = false
                    that.errmsg = "密码验证失败"
                })
        }


        function calSum(data) {
            console.log(data)
            return (data.base_salary * (100 - data.yanglao - data.yiliao - data.shiye - data.gongjijin) + data.sale.sold * data.xiaoshou + data.sale.sold_xu * data.xuke + data.sale.course * data.shangke) / 100

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

app.controller("CoachSaleCtrl", ['$scope', "Restangular", "NgTableParams", "$login",
    function($scope, Restangular, NgTableParams, $login) {
        var gymid = $.cookie("gym")
        var that = this
        that.startday = new Date().addMonths(-1)
        that.endday = new Date();

        that.is_admin = false
        that.errmsg = ""
        that.pwd = ""

        that.submit = function() {
            if (that.pwd == undefined || that.pwd.length == 0) {
                that.errmsg("请输入密码")
                return
            }
            $login.login($.cookie("user"), that.pwd,
                function(data) {
                    $.cookie("token", data.token, {
                        path: '/'
                    })
                    that.is_admin = true
                },
                function(data) {
                    that.is_admin = false
                    that.errmsg = "密码验证失败"
                })
        }

        function calSum(data) {
            console.log(data)
            return (data.base_salary * (100 - data.yanglao - data.yiliao - data.shiye - data.gongjijin) + data.sale.sold * data.xiaoshou + data.sale.sold_xu * data.xuke) / 100

        }

        function refresh() {
            Restangular.one('api/g/', gymid).get().then(function(gym) {
                $scope.coaches = gym.coaches_set
                $.each($scope.coaches, function(i, item) {
                    //render income
                    Restangular.one("api/", item.name).one("income/").get({
                        start: that.startday.Format("yyyyMMdd"),
                        end: that.endday.Format("yyyyMMdd")
                    }).then(function(data) {
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
app.controller("CustomerCtrl", ['$scope', "Restangular", "NgTableParams", "$customersvc",
    function($scope, Restangular, NgTableParams, $customersvc) {
        var gymid = $.cookie("gym")
        var that = this
        $customersvc.getcustomers(function(data) {
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
app.controller("SalarySettingCtrl", ['$scope', "Restangular", "NgTableParams", "$login",
    function($scope, Restangular, NgTableParams, $login) {
        var gymid = $.cookie("gym")
        var self = this
        var originalData = []
        var that = this

        that.is_admin = false
        that.errmsg = ""
        that.pwd = ""

        that.submit = function() {
            if (that.pwd == undefined || that.pwd.length == 0) {
                that.errmsg("请输入密码")
                return
            }
            $login.login($.cookie("user"), that.pwd,
                function(data) {
                    $.cookie("token", data.token, {
                        path: '/'
                    })
                    that.is_admin = true
                },
                function(data) {
                    that.is_admin = false
                    that.errmsg = "密码验证失败"
                })
        }

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
                if (data.length === 0 && self.tableParams.total > 0) {
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
                    cs.shangke = row.shangke
                    cs.patch()
                })

        }
    }
])

app.controller("MainPageCtrl", ['$scope', "Restangular",
        function($scope, Restangular) {
            var date = new Date().Format("yyyyMMdd");
            //var date = "20151029"
            $scope.calendarRowGroup = []
            $scope.timemap = TimeMap
            var g = 0

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
                        Restangular.one("api/", item.name).one("b/", date).get().then(function(data) {
                            var g = Math.floor(i / 4)
                            if ($scope.calendarRowGroup[g] == undefined) {
                                $scope.calendarRowGroup[g] = []
                            }
                            $scope.coaches[i].books = data
                                //$scope.coursecount += data.length
                            $scope.calendarRowGroup[g][i % 4] = $scope.coaches[i]
                        })

                        //render the today income
                    })
                    console.log($scope.coaches)
                })
            }

            function recur() {
                if (!$.cookie("user")) {
                    setTimeout(recur, 3000)
                } else {
                    renderCoaches()
                    renderSale()
                }
            }
            recur()
        }
    ]) // end controller

app.controller("NewGymCtrl", ['$scope', "Restangular", "SweetAlert",
    function($scope, Restangular, SweetAlert) {
        var that = this
        that.vcodetext = "发送验证码"
        that.data = {}
        that.data["phone"] = $.cookie("user")
        that.data["vcode"] = undefined
            //that.data["password"] = undefined
        that.data["gymname"] = undefined
        that.data["gymphone"] = undefined
        that.data["gymaddr"] = undefined
        that.errmsg = undefined

        function validate() {
            var data = that.data
            for (var k in data) {
                if (data[k] == undefined || data[k].length == 0) {
                    that.errmsg = "请填完所有选项"
                    return false
                }
            }
            return true
        }
        that.sendvcode = function() {
            if (that.vcodetext != "发送验证码")
                return
            Restangular.one("api")
                .post("sms", {
                    number: that.data["phone"]
                })
                .then(function() {
                    that.vcodetext = "30秒后重发"
                    setTimeout(function() {
                        that.vcodetext = "发送验证码"
                    }, 30000)
                }, function() {
                    swal("", "发送失败,稍后重试",
                        "warning")
                })

        }

        that.submit = function() {
            if (validate() == false) {
                return
            }
            SweetAlert.swal({
                    //title: "确定移除该教练吗?",
                    title: "",
                    text: "确定提交吗?",
                    type: "warning",
                    showCancelButton: true,
                    confirmButtonColor: "#1fb5ad",
                    confirmButtonText: "确定",
                    cancelButtonText: "取消",
                    showLoaderOnConfirm: true,
                    closeOnConfirm: false
                },
                function(yes) {
                    if (!yes) {
                        return
                    }
                    Restangular.one("api")
                        .post("gr", that.data)
                        .then(function(data) {
                                swal({
                                    title: "成功",
                                    text: "分店已经添加成功",
                                    type: "success",
                                    timer: 1500,
                                    showConfirmButton: false
                                });
                                refreshcorner(true)
                            },
                            function(data) {
                                if (data.status == 403) {
                                    swal("", "验证码错误,请检查后重试", "warning")
                                } else {
                                    swal("", "添加失败,请检查后重试", "warning")
                                }
                            })
                })
        }
    }
])
