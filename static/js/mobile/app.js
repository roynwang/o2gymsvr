


'use strict';

function setmenu(userobj){
	document.getElementById("avatar").setAttribute("src", userobj.avatar)
	$("#coachname").html(userobj.displayname)
}

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

var app = angular.module('o2m', [
    'ui.router',
    'restangular',
    'oitozero.ngSweetAlert',
    'ngMaterial'
])
app.config(function($stateProvider, $urlRouterProvider, RestangularProvider, $httpProvider, $mdDateLocaleProvider) {
    // For any unmatched url, send to /route1
    $mdDateLocaleProvider.formatDate = function(date) {
        return moment(date).format('');
    };
    RestangularProvider.setDefaultHeaders({
        Authorization: "JWT " + $.cookie("token")
    });
    $httpProvider.defaults.headers.common.Authorization = "JWT " + $.cookie("token")
    RestangularProvider.setRequestSuffix('/')
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('login', {
            url: "/login",
            templateUrl: "/static/mobile/login.html",
        })
        .state('index', {
            url: "/",
            templateUrl: "/static/mobile/coachtabs.html",
        })
        .state('coachhome', {
            url: "/coach",
            templateUrl: "/static/mobile/coach.html",
        })
        .state('order', {
            url: "/:coachname/:orderid",
            templateUrl: "/static/mobile/orderdetail.html",
        })
})

app.factory("$date", function() {
    var date = undefined
    return {
        seleteddate: function(pdate) {
            if (pdate != undefined) {
                date = pdate
            }
            if (date == undefined) {
                date = new Date().Format("yyyyMMdd")
            }
            return date
        }

    }
})
app.factory("$booksvc", function(Restangular) {
    function complete(book, onsuccess, onfail) {
        var bookdone = Restangular.one("api", book.coachprofile.name)
            .one("b", book.date.replace(/-/g, ""))
            .all(book.hour)
        bookdone.patch({
                order: book.order,
                done: true
            })
            .then(function(data) {
                swal({
                    title: "成功",
                    text: "课程已经完成",
                    type: "success",
                    timer: 1500,
                    showConfirmButton: false
                });
                onsuccess ? onsuccess() : true
            }, function(data) {
                swal("", "课程完成失败", "warning")
                onfail ? onfail() : true
            })
    }
    return {
        complete: complete
    }
})
app.factory("$ordersvc", function(Restangular) {
    var orderid = undefined

    function setorder(id) {
        orderid = id
    }

    function getorder(id, onsuccess, onfail) {
        var oid = (id ? id : orderid)
        Restangular.one("api", $.cookie("user"))
            .one("o", oid)
            .get()
            .then(onsuccess, onfail)
    }
    return {
        setorder: setorder,
        getorder: getorder
    }
})

app.factory("$usersvc", function(Restangular) {
    var userlist = {}
    var usr = false
    var customer = false

    function gettimetable(username, day, onsuccess, onfail) {
        if (username == undefined) {
            username = $.cookie("user")
        }
        if (username == undefined) {
            return
        }
        Restangular.one("api/", username)
            .one("d/", day.Format("yyyyMMdd"))
            .get()
            .then(onsuccess, onfail)
    }

    function setcustomer(customername) {
        customer = customername
    }

    function getuser(username, refresh, onsuccess, onfail) {
        if (username == undefined) {
            username = $.cookie("user")
        }
        if (username == undefined) {
            return
        }
        if (userlist[username] != undefined && !refresh) {
            onsuccess && onsuccess(userlist[username])
        } else {
            Restangular.one("api", username)
                .get()
                .then(function(data) {
                    userlist[username] = data
                    onsuccess && onsuccess(userlist[username])
                }, function(data) {
                    onfail && onfail()
                })
        }
        return
    }

    function getcustomer(customername, refresh, onsuccess, onfail) {
        getuser(customername ? customername : customer, refresh, onsuccess, onfail)
    }


    function login(username, pwd, onsuccess, onfail) {

        /*
        Restangular.one("api")
            .post("lg",{
                username: username,
                password: pwd
            })
            .then(
                onsuccess,
                onfail)
		*/

        $.post("/api/lg/", {
                    username: username,
                    password: pwd
                },
                onsuccess)
            .fail(onfail)
    }
    return {
        login: login,
        getuser: getuser,
        gettimetable: gettimetable,
        setcustomer: setcustomer,
        getcustomer: getcustomer
    }
})
app.controller("LoginCtrl", ["$state", "$usersvc",
    function($state, $usersvc) {
        var that = this
        that.user = {}
        that.loading = true

        function onfail() {
            that.loading = false
        }

        function trans(user) {
            that.loading = false
            $state.transitionTo(user.iscoach ? "coachhome" : "userhome")
        }
        if ($.cookie("token") == undefined) {
            var user = $usersvc.getuser(undefined, false, trans)
        } else {
            that.loading = false
        }
        that.login = function() {
            that.loading = true
                //$.removeCookie("user")
                //$.removeCookie("gym")
            $usersvc.login(that.user.name, that.user.pwd,
                function(data) {
                    that.loading = false
                    $.cookie("token", data.token, {
                        path: '/'
                    })
                    $.cookie("user", that.user.name, {
                        path: '/'
                    })
                    $usersvc.getuser(that.user.name, false, trans)
                },
                function(data) {
                    that.loading = false
                    that.errmsg = "登录失败"
                })

        }
    }
])
app.controller("TodayCourseCtrl", ["$state", "$usersvc", "$date", "Restangular", "$booksvc", "$mdDialog", "$ordersvc",
    function($state, $usersvc, $date, Restangular, $booksvc, $mdDialog, $ordersvc) {
        var user = $.cookie("user")
        var that = this
        that.timemap = TimeMap
        that.courselist = []
        that.tabs = [true, false]

        that.currentdate = new Date()
        that.dates = []
        that.customerlist = []
		$usersvc.getuser(undefined, false, function(data){
			setmenu(data)
		},
		function(data){})
        Restangular.one("api", user)
            .all("customers")
            .getList()
            .then(function(data) {
                    that.customerlist = data
                },
                function(data) {})

        that.refresh = function() {
            Restangular.one("api", user)
                .one("b", that.selected.Format("yyyyMMdd"))
                .getList()
                .then(function(data) {
                        that.courselist = data
                    },
                    function(data) {
                        //console.log(data.data)
                        if (data.status == 403) {
                            window.location.href = "/mobile/login/"
                        } else {
                            swal("", "获取信息失败，请稍后重试。", "warning")
                        }
                    })
        }
        that.toggle = function(i) {
            that.tabs = [false, false]
            that.tabs[i] = true
        }
        that.select = function(td) {
            that.selected = td
            that.refresh()
        }
        that.complete = function(book) {
            if (book.done) {
                return
            }
            swal({
                title: "完成",
                text: "确认完成课程吗？",
                type: "info",
                showCancelButton: true,
                closeOnConfirm: false,
                confirmButtonText: "确认",
                cancelButtonText: "取消",
                showLoaderOnConfirm: true,
            }, function(yes) {
                if (!yes) {
                    return
                }
                $booksvc.complete(book, that.refresh)
            });
        }
        that.refreshdates = function() {
            that.selected = that.currentdate
            that.dates[0] = that.currentdate
            that.dates[1] = that.currentdate.addDays(1)
            that.dates[2] = that.currentdate.addDays(2)
            that.dates[3] = that.currentdate.addDays(3)
            that.refresh()
        }
        that.showcustomer = function(name) {
            $usersvc.setcustomer(name)
            $mdDialog.show({
                    controller: 'CustomerDetailCtrl',
                    templateUrl: '/static/mobile/customerdetail.html',
                    parent: angular.element(document.body),
                    //targetEvent: ev,
                    clickOutsideToClose: true,
                    fullscreen: true
                })
                .then(function(answer) {
                    console.log('You said the information was "' + answer + '".');
                }, function() {
                    console.log('You cancelled the dialog.')
                });
        }

        that.showorder = function(orderid) {
            $ordersvc.setorder(orderid)
                //var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;
            $mdDialog.show({
                    controller: 'OrderDetailCtrl',
                    templateUrl: '/static/mobile/orderdetail.html',
                    parent: angular.element(document.body),
                    //targetEvent: ev,
                    clickOutsideToClose: true,
                    fullscreen: true
                })
                .then(function(answer) {
                    console.log('You said the information was "' + answer + '".');
                }, function() {
                    console.log('You cancelled the dialog.')
                });

        }
        that.refreshdates()
    }
])
app.controller("OrderDetailCtrl", ['$scope', 'Restangular', '$mdDialog', '$ordersvc', '$usersvc',
    function($scope, Restangular, $mdDialog, $ordersvc, $usersvc) {
        var that = this
        that.currentdate = new Date()
        that.dates = []

        that.actionlist = []

        that.timetable = undefined

        function processtimetable(td) {
            _.each(that.actionlist, function(book) {
                if (book.pendingaction == "remove") {
                    if (td.Format("yyyy-MM-dd") == book.date) {
                        that.timetable.availiable.push(book.hour)
                        that.timetable.availiable.push(book.hour + 1)
                    }
                }
                if (book.pendingaction == "add") {
                    if (td.Format("yyyy-MM-dd") == book.date) {
                        that.timetable.availiable = _.without(that.timetable.availiable, book.hour, book.hour + 1)
                        console.log(that.timetable.availiable)
                    }
                }
            })
        }
        that.select = function(td) {

            if (that.selected == td) {
                processtimetable()
                return
            }
            that.selected = td
            $usersvc.gettimetable(undefined, td, function(data) {
                that.timetable = data
                processtimetable(that.selected)
            }, undefined)
        }
        that.isAvaHour = function(hour) {
            if (that.timetable == undefined) {
                return false
            }
            if (that.timetable.availiable.indexOf(hour) >= 0) {
                return true
            }
            return false
        }
        that.timemap = TimeMap
        that.order = {}

        that.completedbook = []
        that.bookedbook = []

        that.refreshdates = function() {
            that.dates[0] = that.currentdate
            that.dates[1] = that.currentdate.addDays(1)
            that.dates[2] = that.currentdate.addDays(2)
            that.dates[3] = that.currentdate.addDays(3)
            that.select(that.currentdate)
                //that.refresh()
        }
        that.cancel = function() {
            $mdDialog.cancel();
        }
		that.recover = function(task){
			if(task.pendingaction == "remove"){
				that.bookedbook.push(task)
			}
			that.actionlist = _.reject(that.actionlist, function(item){ return task==item})
			processtimetable(that.selected)
		}

        that.refresh = function() {
            $ordersvc.getorder(undefined,
                function(data) {
                    that.order = data
                    that.completedbook = _.where(data.booked, {
                        done: true
                    })
                    that.bookedbook = _.where(data.booked, {
                        done: false
                    })
                },
                function(data) {
                    swal("", "获取信息失败，请稍后重试。", "warning")
                })
        }

        that.addbook = function(h) {
            //if reach max
            var count = 0
            for (var i in that.actionlist) {
                if (that.actionlist[i].pendingaction == "remove") {
                    count -= 1
                } else {
                    count += 1
                }
            }
            count += that.order.booked.length

            if (count < that.order.course_count && that.isAvaHour(h) && that.isAvaHour(h + 1)) {
                var newbook = {
                    date: that.selected.Format("yyyy-MM-dd"),
                    hour: h,
                    coach: that.order.coachdetail.id,
                    custom: that.order.customerdetail.id,
                    order: that.order.id,
                    pendingaction: "add"
                }
                that.actionlist.push(newbook)
                processtimetable(that.selected)
            }
        }
        that.removebook = function(bookid) {
            var tar = _.findWhere(that.bookedbook, {
                id: bookid
            })
            tar["pendingaction"] = "remove"
                //add to actionlist
            that.actionlist.push(tar)
                //remove from bookedbook
            that.bookedbook = _.reject(that.bookedbook, function(item) {
                    return item.id == bookid
                })
                //refresh time table
            processtimetable(that.selected)
        }
        that.completeditem = function() {
            that.pendingaction -= 1
            if (that.pendingaction == 0) {
                that.submitting = false
                swal({
                    type: "success",
                    title: "提交成功",
                    text: "",
                    timer: 1500,
                    showConfirmButton: false
                });
                $mdDialog.cancel();
            }
        }

        that.submit = function() {
            swal({
                title: "提交",
                text: "确认提交吗?",
                type: "warning",
                showCancelButton: true,
                cancelButtonText: "取消",
                confirmButtonText: "确认",
                confirmButtonColor: "#1fb5ad",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function() {
                var removelist = _.where(that.actionlist, {
                    pendingaction: "remove"
                })
                var addlist = _.where(that.actionlist, {
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
                    Restangular.one("api/", $.cookie("user"))
                        .one("b/" + datestr, item.hour)
                        .remove()
                        .then(function(data) {
                            console.log("remove success")
                            that.completeditem()
                        })
                })
                _.each(addlist, function(item, i) {
                    var datestr = item.date.replace(/-/g, "")
                    Restangular.one("api/", $.cookie("user"))
                        .post("b/" + datestr, item)
                        .then(function(data) {
                            that.completeditem()
                            console.log(data)
                        })
                })
            })
        }

        that.refreshdates()
        that.refresh()
    }
])
app.controller("CustomerDetailCtrl", ["$state", "$usersvc", "Restangular", "$mdDialog", "$ordersvc",
    function($state, $usersvc, Restangular, $mdDialog, $ordersvc) {
        var that = this
        that.customer = {}
        that.orderlist = {}
        that.cancel = function() {
            $mdDialog.cancel();
        }
        that.getorderlist = function() {
            Restangular.one("api", that.customer.name)
                .one("o")
                .get()
                .then(function(data) {
                        that.orderlist = _.where(data.results,{coach:$.cookie("user")})
                    },
                    function(data) {})
        }
		that.call = function(){
		}
        that.showorder = function(orderid) {
            $ordersvc.setorder(orderid)
                //var useFullScreen = ($mdMedia('sm') || $mdMedia('xs')) && $scope.customFullscreen;
            $mdDialog.show({
                    controller: 'OrderDetailCtrl',
                    templateUrl: '/static/mobile/orderdetail.html',
                    parent: angular.element(document.body),
                    //targetEvent: ev,
                    clickOutsideToClose: true,
                    fullscreen: true
                })
                .then(function(answer) {
                    console.log('You said the information was "' + answer + '".');
                }, function() {
                    console.log('You cancelled the dialog.')
                });

        }
        $usersvc.getcustomer(undefined, false, function(data) {
            that.customer = data
			that.getorderlist()
        }, function(data) {
            console.log("getuser failed")
        })


    }
])
