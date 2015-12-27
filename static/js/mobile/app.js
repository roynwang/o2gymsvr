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

var app = angular.module('o2m', [
    'ui.router',
    'restangular',
    'oitozero.ngSweetAlert'
])
app.config(function($stateProvider, $urlRouterProvider, RestangularProvider, $httpProvider) {
    // For any unmatched url, send to /route1
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

app.factory("$usersvc", function(Restangular) {
    var userlist = {}
    var usr = false

    function getuser(username, refresh, onsuccess, onfail) {
        if (username == undefined) {
            username = $.cookie("user")
        }
        if (username == undefined) {
            return
        }
        if (userlist[username] != undefined && !refresh) {
            onsuccess && onsuccess(userlist[username])
        }
        Restangular.one("api", username)
            .get()
            .then(function(data) {
                userlist[username] = data
                onsuccess && onsuccess(userlist[username])
            }, function(data) {
                onfail && onfail()
            })
        return
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
        getuser: getuser
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
app.controller("TodayCourseCtrl", ["$state", "$usersvc", "$date", "Restangular", "$booksvc",
    function($state, $usersvc, $date, Restangular, $booksvc) {
        var user = $.cookie("user")
        var that = this
        that.timemap = TimeMap
        that.courselist = []
        that.tabs = [true, false]
        that.refresh = function() {
            Restangular.one("api", user)
                //.one("b", $date.seleteddate())
                .one("b", new Date().Format("yyyyMMdd"))
                .getList()
                .then(function(data) {
                        that.courselist = data
                    },
                    function(data) {
                        console.log(data.data)
                    })
        }
        that.toggle = function(i) {
            that.tabs = [false, false]
            that.tabs[i] = true
        }
        that.complete = function(book) {
			if(book.done){
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
            }, function(yes){
                if (!yes) {
                    return
                }
                $booksvc.complete(book, that.refresh)
            });
        }
		that.refresh()
    }
])
