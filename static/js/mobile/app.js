var bukcet = "https://dn-o2fit.qbox.me"

function setmenu(userobj) {
    document.getElementById("avatar").setAttribute("src", userobj.avatar_small)
    $("#coachname").html(userobj.displayname)
}

function settitle(title) {
    $("#page-title").html(title)
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
String.prototype.fixSize = function(w, h) {
    if (w == undefined) {
        w = 200
    }
    if (h == undefined) {
        h = w
    }
    var str = this + "?imageView2/1/w/" + w.toString() + "/h/" + h.toString()
    return str
}

var TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]

var app = angular.module('o2m', [
    'ui.router',
    'restangular',
    'oitozero.ngSweetAlert',
    'ngMaterial',
    'angularQFileUpload',
    'LocalStorageModule'
])
app.config(function($stateProvider, $urlRouterProvider, RestangularProvider, $httpProvider, $mdDateLocaleProvider, $compileProvider) {
    // For any unmatched url, send to /route1
    $compileProvider.aHrefSanitizationWhitelist(/^\s*(https?|local|data|tel|sms):/);
    $mdDateLocaleProvider.formatDate = function(date) {
        return moment(date).format('');
    };
    $mdDateLocaleProvider.months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
    $mdDateLocaleProvider.shortMonths = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
    $mdDateLocaleProvider.days = ['周日', '周二', '周三', '周四', '周五', '周六']
    $mdDateLocaleProvider.shortDays = ['日', '一', '二', '三', '四', '五', '六']
    $mdDateLocaleProvider.firstDayOfWeek = 1

    RestangularProvider.setDefaultHeaders({
        Authorization: "JWT " + $.cookie("token")
    });
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
        .state('profile', {
            url: "/profile",
            templateUrl: "/static/mobile/profile.html"
        })
        .state('coachhome', {
            url: "/coach",
            templateUrl: "/static/mobile/coach.html",
        })
        .state('neworder', {
            url: "/neworder",
            templateUrl: "/static/mobile/neworder.html",
            //controller: "NewOrderCtrl"
        })
        .state('changepwd', {
            url: "/changepwd",
            templateUrl: "/static/mobile/changepwd.html",
            //controller: "NewOrderCtrl"
        })
        .state('order', {
            url: "/:coachname/:orderid",
            templateUrl: "/static/mobile/orderdetail.html",
        })

})

app.factory("$uploader", function($qupload) {
    var key = ""
    var token = ""

    function gettoken(onsuccess, onfail) {
        $.get("/api/p/token/", function(data, status) {
                key = data.key
                token = data.token
                onsuccess && onsuccess()
            })
            .error(onfail)
    }

    function upload(file, onsuccess, onfail) {
        $.get("/api/p/token", function(data, status) {
            key = data.key
            token = data.token
            file.upload = $qupload.upload({
                key: key,
                file: file,
                token: token
            });
            file.upload.then(function(response) {
                onsuccess && onsuccess(response)
            }, function(response) {
                onfail && onfail(response)
            }, function(evt) {});
        })
    }
    return {
        upload: upload
    }
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

    function changepwd(username, vcode, pwd, onsuccess, onfail) {
        $.post("/api/sms/" + username + "/", {
                    vcode: vcode,
                    password: pwd
                },
                function(data) {
                    Restangular.setDefaultHeaders({
                        Authorization: "JWT " + data.token
                    });
                    onsuccess && onsuccess(data)
                })
            .fail(onfail)
    }

    function loginwithvcode(username, vcode, onsuccess, onfail) {
        $.post("/api/sms/" + username + "/", {
                    vcode: vcode
                },
                function(data) {
                    Restangular.setDefaultHeaders({
                        Authorization: "JWT " + data.token
                    });
                    onsuccess && onsuccess(data)
                })
            .fail(onfail)
    }

    function sendvcode(username, onsuccess, onfail) {
        $.post("/api/sms/", {
                    number: username
                },
                function(data) {
                    Restangular.setDefaultHeaders({
                        Authorization: "JWT " + data.token
                    });
                    onsuccess && onsuccess(data)
                })
            .fail(onfail)
    }

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
                    data.avatar_small = data.avatar.fixSize()
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
                function(data) {
                    Restangular.setDefaultHeaders({
                        Authorization: "JWT " + data.token
                    });
                    onsuccess && onsuccess(data)
                })
            .fail(onfail)
    }
    return {
        login: login,
        getuser: getuser,
        gettimetable: gettimetable,
        setcustomer: setcustomer,
        getcustomer: getcustomer,
        sendvcode: sendvcode,
        loginwithvcode: loginwithvcode,
        changepwd: changepwd
    }
})
app.controller("LoginCtrl", ["$state", "$usersvc", "$mdDialog",
    function($state, $usersvc, $mdDialog) {
        var that = this
        that.user = {}
        that.loading = true
        that.vcodetext = "发送验证码"
        that.errmsg = false
        that.cancel = function() {
            $mdDialog.cancel();
        }
        that.startload = function() {
            $("#new-stack").css("opacity", 0.6)
        }
        that.endload = function() {
            $("#new-stack").css("opacity", 0)
        }
        that.endload()

        function onfail() {
            that.endload()
        }

        function trans(user) {
            that.loading = false
            if (user.iscoach) {
                $mdDialog.cancel();
            } else {
                swal("", "用户自助预约暂未开发完成，请耐心等待", "warning")
            }
            //$state.transitionTo(user.iscoach ? "coachhome" : "userhome")
        }
        if ($.cookie("token") == undefined) {
            var user = $usersvc.getuser(undefined, false, trans)
        } else {
            that.loading = false
        }
        that.login = function() {
            that.loading = true
            that.startload()
            $usersvc.login(that.user.name, that.user.pwd,
                function(data) {
                    that.loading = false

                    that.endload()
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

                    that.endload()
                    that.errmsg = "登录失败"
                })

        }
        that.sendvcode = function() {
            if (that.user.name == undefined || that.user.name.toString().length != 11) {
                that.errmsg = "请输入正确的11位手机号"
                return
            } else {
                that.errmsg = false
                that.startload()
                if (that.vcodetext == "发送验证码") {
                    that.vcodetext = "已发送"
                    $usersvc.sendvcode(that.user.name,
                        function(data) {

                            that.endload()
                            that.vcodetext = "30秒后重发"
                            setTimeout(function() {
                                that.vcodetext = "发送验证码"
                            }, 30000)
                        },
                        function(data) {
                            console.log(data)
                            that.errmsg = "发送失败,稍后重试"
                            that.endload()
                        })
                }
            }
        }
        that.loginwithvcode = function() {
            that.loading = true
            that.errmsg = false
            that.startload()
            $usersvc.loginwithvcode(that.user.name, that.user.vcode,
                function(data) {
                    that.loading = false
                    that.endload()
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
                    that.endload()
                    that.errmsg = "登录失败,请检查输入"
                })
        }
    }
])
app.controller("TodayCourseCtrl", ["$state", "$usersvc", "$date", "Restangular", "$booksvc", "$mdDialog", "$ordersvc", "$scope",
    function($state, $usersvc, $date, Restangular, $booksvc, $mdDialog, $ordersvc, $scope) {
        var user = $.cookie("user")
        var that = this
        settitle("课表")
        that.timemap = TimeMap
        that.courselist = []
        that.tabs = [true, false]

        that.currentdate = new Date()
        that.dates = []
        that.customerlist = []
        that.init = function() {
            user = $.cookie("user")
            $usersvc.getuser(undefined, false, function(data) {
                    that.user = data
                    setmenu(data)
                },
                function(data) {})
            Restangular.one("api", user)
                .all("customers")
                .getList()
                .then(function(data) {
                        that.customerlist = data
                        that.customerlist.sort(function(a, b) {
                            return a.displayname.localeCompare(b.displayname)
                        })
                    },
                    function(data) {})
        }

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
                            swal("", data.status + "获取信息失败，请稍后重试。", "warning")
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
        $scope.showneworder = function() {
            $mdDialog.show({
                    controller: "NewOrderDialgCtrl",
                    templateUrl: '/static/mobile/neworder.html',
                    parent: angular.element(document.body),
                    //targetEvent: ev,
                    clickOutsideToClose: true,
                    fullscreen: true
                })
                .then(function(answer) {
                    console.log('You said the information was "' + answer + '".');
                    $state.transitionTo("index")
                }, function() {
                    console.log('You cancelled the dialog.')
                    $state.transitionTo("index")
                });
        }

        $("#neworder").click(function() {
            $scope.showneworder()
        })

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
        if (user == undefined) {
            $mdDialog.show({
                    controller: 'LoginCtrl',
                    templateUrl: '/static/mobile/login.html',
                    parent: angular.element(document.body),
                    //targetEvent: ev,
                    clickOutsideToClose: true,
                    fullscreen: true
                })
                .then(function(answer) {
                    that.init()
                    that.refreshdates()

                }, function() {
                    that.init()
                    that.refreshdates()
                });
        } else {
            that.init()
            that.refreshdates()
        }
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
                } else if (book.pendingaction == "add") {
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

                if (that.timetable.na.indexOf(26) < 0) {
                    that.timetable.availiable.push(26)
                }

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
        that.recover = function(task) {
            if (task.pendingaction == "remove") {
                that.bookedbook.push(task)
            }
            that.actionlist = _.reject(that.actionlist, function(item) {
                return task == item
            })
            if (that.selected.Format("yyyy-MM-dd") == task.date) {
                that.timetable.availiable.push(task.hour, task.hour + 1)
            }
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
            count += that.bookedbook.length
            count += that.completedbook.length

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
            swal({
                title: "取消",
                text: "确认取消吗?",
                type: "warning",
                showCancelButton: true,
                cancelButtonText: "放弃",
                confirmButtonText: "确认",
                confirmButtonColor: "#1fb5ad",
                closeOnConfirm: false,
                showLoaderOnConfirm: true
            }, function() {
                var item = _.findWhere(that.bookedbook, {
                    id: bookid
                })

                var datestr = item.date.replace(/-/g, "")
                Restangular.one("api/", $.cookie("user"))
                    .one("b/" + datestr, item.hour)
                    .remove()
                    .then(function(data) {
                        swal({
                            type: "success",
                            title: "提交成功",
                            text: "",
                            timer: 1500,
                            showConfirmButton: false
                        });

                        console.log("remove success")
                        var tar = _.findWhere(that.bookedbook, {
                                id: bookid
                            })
                            //tar["pendingaction"] = "remove"
                            //add to actionlist
                            //that.actionlist.push(tar)
                            //remove from bookedbook
                        that.bookedbook = _.reject(that.bookedbook, function(item) {
                                return item.id == bookid
                            })
                            //refresh time table
                            //processtimetable(that.selected)
                        if (that.selected.Format("yyyy-MM-dd") == item.date) {
                            that.timetable.availiable.push(item.hour, item.hour + 1)
                        }
                    })

            })
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
            var removelist = _.where(that.actionlist, {
                pendingaction: "remove"
            })
            var addlist = _.where(that.actionlist, {
                pendingaction: "add"
            })
            that.pendingaction = removelist.length + addlist.length
            if (that.pendingaction == 0) {
                $mdDialog.cancel();
                return
            } else {
                that.submitting = true
            }

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
                        that.orderlist = _.where(data.results, {
                            coach: $.cookie("user")
                        })
                    },
                    function(data) {})
        }
        that.call = function() {}
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

app.controller("NewOrderDialgCtrl", ["$scope", "$state", "$usersvc", "$mdDialog", "$ordersvc", "SweetAlert", "Restangular",
    function($scope, $state, $usersvc, $mdDialog, $ordersvc, SweetAlert, Restangular) {
        var that = this
        that.cancel = function() {
            $mdDialog.cancel()
        }
        that.mo = {}
        that.mo.customer_displayname = ""
        that.mo.customer_phone = ""
        that.mo.product_introduction = "dummy"
        that.mo.product_price = ""
        that.mo.product_promotion = -1
        that.mo.product_amount = ""
        that.mo.product_duration = ""
        that.mo.sex = '0'
        that.mo.age = undefined
        that.changesex = function(i) {
            that.mo.sex = i
        }

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
                    that.mo.customer_phone = that.mo.customer_phone.toString()
                    Restangular.one("api/", $.cookie("user"))
                        .post("manualorder", that.mo)
                        .then(function(data) {
                            console.log(data)
                            swal({
                                title: "成功",
                                text: "订单提交成功",
                                type: "success",
                                timer: 1500,
                                showConfirmButton: false
                            });

                            $ordersvc.setorder(data.id)
                            $mdDialog.show({
                                    controller: 'OrderDetailCtrl',
                                    templateUrl: '/static/mobile/orderdetail.html',
                                    parent: angular.element(document.body),
                                    clickOutsideToClose: true,
                                    fullscreen: true
                                })
                                .then(function(answer) {
                                    console.log('You said the information was "' + answer + '".');
                                }, function() {
                                    console.log('You cancelled the dialog.')
                                });
                        }, function(data) {
                            swal("", "订单保存失败，请检查输入后重试", "warning")
                        })
                })
        }

    }
])
app.controller("ChangePwdCtrl", ["$state", "$usersvc", "$mdDialog",
    function($state, $usersvc, $mdDialog) {
        var that = this
        settitle("重置密码")
        that.user = {}
        that.loading = true
        that.vcodetext = "发送验证码"
        that.errmsg = false
        that.pwdset = {}

        that.startload = function() {
            $("#new-stack").css("opacity", 0.6)
        }
        that.endload = function() {
            $("#new-stack").css("opacity", 0)
        }
        $usersvc.getuser(undefined, false, function(usr) {
            that.user = usr
            that.pwdset["phone"] = usr.name
        })
        that.validate = function() {
            if (that.pwdset.vcode == undefined || that.pwdset.vcode.toString().length != 6) {
                that.errmsg = "请输入6位验证码"
                return false
            }
            if (that.pwdset.pwd == undefined || that.pwdset.pwd.length == 0) {
                that.errmsg = "请输入密码"
                return false
            }
            if (that.pwdset.pwd != that.pwdset.pwdconfirm) {
                that.errmsg = "两次输入的密码不同"
                return false
            }
            return true

        }
        that.submit = function() {
            if (that.validate() == false) {
                return
            }
            $usersvc.changepwd(that.pwdset.phone, that.pwdset.vcode, that.pwdset.pwd, function() {
                    swal({
                        title: "",
                        text: "密码已更新",
                        type: "success",
                        timer: 1500,
                        showConfirmButton: false
                    });
                },
                function(data) {
                    if (data.status == 403) {
                        swal("", "验证码错误，请检查后重新输入", "warning")
                    } else {
                        swal("", "密码修改失败，请检查后重新输入", "warning")
                    }
                })
        }
        that.sendvcode = function() {
            that.errmsg = false
            that.startload()
            if (that.vcodetext == "发送验证码") {
                that.vcodetext = "已发送"
                $usersvc.sendvcode(that.user.name,
                    function(data) {
                        that.endload()
                        that.vcodetext = "30秒后重发"
                        setTimeout(function() {
                            that.vcodetext = "发送验证码"
                        }, 30000)
                    },
                    function(data) {
                        console.log(data)
                        that.errmsg = "发送失败,稍后重试"
                        that.endload()
                    })
            }
        }
    }
])


app.controller("ProfileCtrl", ["$scope", "$usersvc", "$uploader", "$qupload", "Restangular",
        function($scope, $usersvc, $uploader, $qupload, Restangular) {
            var that = this
            settitle("个人资料")
            that.user = {}
            $scope.selectFiles = [];
            $usersvc.getuser(undefined, false, function(usr) {
                setmenu(usr)
                that.user = usr
            })

            that.onFileSelect = function($files) {
                $uploader.upload($files[0], function(data) {
                    that.user.avatar = bukcet + "/" + data.key
                    console.log(that.user.avatar)
                    that.save()
                })
            }
            that.save = function() {
                Restangular.one("api", that.user.name)
                    .patch({
                        avatar: that.user.avatar,
                        sex: that.user.sex,
                        displayname: that.user.displayname,
                        signature: that.user.signature
                    })
                    .then(function(data) {
                            swal({
                                title: "",
                                text: "已更新",
                                type: "success",
                                timer: 1500,
                                showConfirmButton: false
                            });
                            $usersvc.getuser(undefined, true, function(usr) {
                                that.user = usr
                                setmenu(usr)
                            })
                        },
                        function(data) {
                            swal("", "信息保存失败", "warning", 1500, false)
                        })
            }

            that.changesex = function(i) {
                that.user.sex = i
            }

        }
    ])
    /*
    $(function() {
        $("#neworder").click(function() {
    		var s = angular.element(document.getElementById("agcontainer")).scope()
    		var c = s.controller()
            s.$apply(function() {
                s.showneworder()
            })
        })
    })
    */
