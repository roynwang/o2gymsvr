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
    'restangular'
])
app.config(function($stateProvider, $urlRouterProvider, RestangularProvider, $httpProvider) {
    // For any unmatched url, send to /route1
    /*
    RestangularProvider.setDefaultHeaders({
        Authorization: "JWT " + $.cookie("token")
    });
	*/
    $httpProvider.defaults.headers.common.Authorization = "JWT " + $.cookie("token")
    RestangularProvider.setRequestSuffix('/')
    $urlRouterProvider.otherwise("/");
    $stateProvider
        .state('index', {
            url: "/",
            templateUrl: "/static/mobile/login.html",
        })
        .state('coachhome', {
            url: "/",
            templateUrl: "/static/mobile/login.html",
        })
        .state('userhome', {
            url: "/",
            templateUrl: "/static/mobile/login.html",
        })
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
        Restangular.one("api")
            .post("lg",{
                username: username,
                password: pwd
            })
            .then(
                onsuccess,
                onfail)

        /*
        $.post("/api/lg/", {
                    username: username,
                    password: pwd
                },
                onsuccess)
            .fail(onfail)
		*/
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
                    $usersvc.getuser(that.user.name, false, trans)
                },
                function(data) {
                    that.loading = false
                    that.errmsg = "登录失败"
                })

        }
    }
])
