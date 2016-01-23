var bukcet = "https://dn-o2fit.qbox.me"

function b64toBlob(b64Data, contentType, sliceSize) {
    contentType = contentType || '';
    sliceSize = sliceSize || 512;

    var byteCharacters = atob(b64Data.split(',')[1]);
    var byteArrays = [];

    for (var offset = 0; offset < byteCharacters.length; offset += sliceSize) {
        var slice = byteCharacters.slice(offset, offset + sliceSize);

        var byteNumbers = new Array(slice.length);
        for (var i = 0; i < slice.length; i++) {
            byteNumbers[i] = slice.charCodeAt(i);
        }

        var byteArray = new Uint8Array(byteNumbers);

        byteArrays.push(byteArray);
    }

    var blob = new Blob(byteArrays, {
        type: contentType
    });
    return blob;
}

function setmenu(userobj) {
    //document.getElementById("avatar").setAttribute("src", userobj.avatar_small)
    //$("#coachname").html(userobj.displayname)
}

function settitle(title, hidemenu) {
        $("#page-title").html(title)
        if (hidemenu) {
            $("#menu-button").hide()
            $("#neworder").hide()
            $("#back-button").show()
        } else {
            $("#menu-button").show()
            $("#neworder").show()
            $("#back-button").hide()
        }
    }
    /*
    document.addEventListener('WeixinJSBridgeReady', function onBridgeReady() {
    	    WeixinJSBridge.call('hideToolbar');
    		    WeixinJSBridge.call('hideOptionMenu');
    })
    */

$(function() {
    $("#back-button").click(function() {
        history.back()
    })
})

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
        'LocalStorageModule',
        //'ngAnimate', 
        //'anim-in-out'
    ])
    /*
    app.directive("scroll", function($window) {
        return function(scope, element, attrs) {
            angular.element($window).bind("scroll", function() {
                scope.$apply(scope.scrolled(this.pageXOffset, this.pageYOffset))
            });
        };
    });
    */
    /*
    app.directive('infiniteScroll', [ "$window", function ($window) {
            return {
                link:function (scope, element, attrs) {
                    var offset = parseInt(attrs.threshold) || 0;
                    var e = element[0];

                    element.bind('scroll', function () {
                        if (scope.$eval(attrs.canLoad) && e.scrollTop + e.offsetHeight >= e.scrollHeight - offset) {
                            scope.$apply(attrs.infiniteScroll);
                        }
                    });
                }
            };
        }]);
    */
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
        .state('our', {
            url: "/our",
            templateUrl: "/static/mobile/ourcourse.html",
        })
        .state('index', {
            url: "/",
            templateUrl: "/static/mobile/coachtabs.html",
        })
        .state('profile', {
            url: "/profile",
            templateUrl: "/static/mobile/profile.html"
        })
        .state('customerdetail', {
            url: "/customer/:name",
            templateUrl: "/static/mobile/customerdetail.html"
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
        /*
        .state('orderdetail', {
            url: "/orderdetail/:orderid",
            templateUrl: "/static/mobile/orderdetailnew.html",
        })
		*/
        .state('customerlist', {
            url: "/customers",
            templateUrl: "/static/mobile/customerlist.html",
        })
        .state('orderdetail', {
            url: "/orderdetail/:orderid?date",
            templateUrl: "/static/mobile/orderdetail.html",
        })
})


app.factory("$paramssvc", function() {
    var params = {}
    return {
        params: params
    }
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

        function compress(source_img_obj, quality) {
            var mime_type = "image/jpeg";
            var cvs = document.createElement('canvas');
            cvs.width = source_img_obj.naturalWidth;
            cvs.height = source_img_obj.naturalHeight;
            var ctx = cvs.getContext("2d").drawImage(source_img_obj, 0, 0);
            var newImageData = cvs.toDataURL(mime_type, quality / 100);
            return newImageData
        }

        $.get("/api/p/token", function(data, status) {
            key = data.key
            token = data.token

            var reader = new FileReader();
            reader.readAsDataURL(file);
            reader.onload = function(event) {
                var imgori = new Image();
                imgori.onload = function() {
                    var compressed = compress(imgori, 20)
                    var newf = b64toBlob(compressed, "image/jpeg")
                        /*
                var newf = new Blob([b64toBlob( compressed.src], {
                    type: "image/jpeg"
                });
				*/
                    newf.upload = $qupload.upload({
                        key: key,
                        file: newf,
                        token: token
                    });

                    newf.upload.then(function(response) {
                        onsuccess && onsuccess(response)
                    }, function(response) {
                        onfail && onfail(response)
                    }, function(evt) {});
                }
                imgori.src = reader.result
            }
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
    function create(coachname, book, onsuccess, onfail) {
        var datestr = book.date.replace(/-/g, "")
        Restangular.one("api/", coachname)
            .post("b/" + datestr, book)
            .then(onsuccess, onfail)

    }

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

    function bookremove(book, onsuccess, onfail) {
        var datestr = book.date.replace(/-/g, "")
        Restangular.one("api/", book.coachprofile.name)
            .one("b/" + datestr, book.hour)
            .remove()
            .then(onsuccess, onfail)
    }

    function savedetail(book, onsuccess, onfail) {
        var bookdone = Restangular.one("api", book.coachprofile.name)
            .one("b", book.date.replace(/-/g, ""))
            .all(book.hour)
        bookdone.patch({
                order: book.order,
                detail: book.detail
            })
            .then(onsuccess, onfail)
    }
    return {
        complete: complete,
        create: create,
        remove: bookremove,
        savedetail: savedetail,

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

    function getorders(username, onsuccess, onfail) {
        Restangular.one("api", username)
            .one("o")
            .get()
            .then(onsuccess, onfail)
    }
    return {
        setorder: setorder,
        getorder: getorder,
        getorders: getorders
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
app.controller("CustomerListCtrl", ["Restangular",
    function(Restangular) {
        Restangular.one("api", user)
            .all("customers")
            .getList()
            .then(function(data) {
                    that.customerlist = data
                    that.customerlist.sort(function(a, b) {
                        return a.pinyin.localeCompare(b.pinyin)
                    })
                    console.log(that.customerlist)
                },
                function(data) {})

        that.showcustomer = function(customer) {
            $state.transitionTo("customerdetail", {
                name: customer.name
            })
        }
    }
])

app.controller("TodayCourseCtrl", ["$state", "$usersvc", "$date", "Restangular", "$booksvc", "$mdDialog", "$ordersvc", "$scope", "$paramssvc", "$mdToast", "$mdSidenav", "$document", "$mdSidenav", "$timeout",
    function($state, $usersvc, $date, Restangular, $booksvc, $mdDialog, $ordersvc, $scope, $paramssvc, $mdToast, $mdSidenav, $document, $mdSidenav, $timeout) {
        var user = $.cookie("user")
        var that = this
        that.timemap = TimeMap
        that.courselist = []
        that.tabs = [true, false]
        that.currentdate = new Date()
        that.dates = []
        that.customerlist = []
        that.selectedItem = undefined
        that.querystatus = "unset"
        that.pendingbook = {}
        that.isSelecting = false
        that.animating = -1
		that.inited = false

		$timeout(function(){
            that.inited = true
		},2000)

        that.showneworder = function() {
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



        that.toggleMenu = function(direction) {
            $mdSidenav(direction)
                .toggle()
                .then(function() {});
        }
        that.cancelselect = function() {
            that.isSelecting = false
            that.editing = false
            _.each(that.bookmap, function(item) {
                item.editing = false
                item.editingitem = false
            })
        }

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
                            return a.pinyin.localeCompare(b.pinyin)
                        })
                        that.selecting = that.customerlist
                    },
                    function(data) {})
        }
        that.logtrain = function(book) {
            $paramssvc.params["traindetail"] = book
            $mdDialog.show({
                    controller: "TrainDetailCtrl",
                    templateUrl: '/static/mobile/traindetail.html',
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

        that.bookmap = []
        that.editingtime = undefined
        that.edit = function(c, edit) {
            that.editingtime = that.timemap[c.index]
            if (c.book || that.bookmap[parseInt(c.index) + 1].book) {
                return
            }
            var editingitem = _.find(that.bookmap, function(item) {
                return item.editing == true
            })
            if (editingitem == undefined) {
                that.isSelecting = true
                c.editing = true
                if (that.selectedItem) {
                    that.searchText = that.selectedItem.displayname
                }
            } else {
                if (editingitem != c) {
                    editingitem.editing = false
                    that.querystatus = "unset"
                    that.searchText = undefined
                }
            }
        }
        that.queryOrder = function(c) {
            if (that.querystatus == "querying") {
                return
            }
            that.querystatus = "querying"
            var customer = that.selectedItem
            if (!customer) {
                that.querystatus = "unset"
                return
            }

            $ordersvc.getorders(customer.name, function(data) {
                    var os = _.reject(data.results, function(item) {
                        return item.all_booked == true
                    })

                    if (os && os.length > 0) {
                        var o = os[0]
                        that.pendingbook = {
                            date: that.selected.Format("yyyy-MM-dd"),
                            hour: c.index,
                            coach: that.user.id,
                            custom: o.customerdetail.id,
                            order: o.id
                        }
                        that.querystatus = "pending"
                        console.log(that.pendingbook)
                    } else {
                        that.showtoast = true
                        $mdToast.show(
                            $mdToast.simple()
                            .textContent('没有匹配的订单')
                            .parent(angular.element(document.querySelector("#toast-placeholder")))
                            .hideDelay(3000)
                        ).then(function() {
                            $timeout(function() {
                                that.showtoast = false
                            }, 500)
                        });
                        that.querystatus = "unmatch"
                    }
                },
                function(data) {
                    that.showtoast = true
                    $mdToast.show(
                        $mdToast.simple()
                        .textContent('查询订单失败')
                        .parent(angular.element(document.querySelector("#toast-placeholder")))
                        .hideDelay(3000)
                    ).then(function() {
                        $timeout(function() {
                            that.showtoast = false
                        }, 500)
                    });
                    that.querystatus = "unmatch"
                })
        }
        that.submitbook = function() {
            that.querystatus = "querying"
            Restangular.one("api/", that.user.name)
                .post("b/" + that.selected.Format("yyyyMMdd"), that.pendingbook)
                .then(function(data) {
                    that.querystatus = "unset"
                    that.showtoast = true
                    $mdToast.show(
                        $mdToast.simple()
                        .textContent('预约已提交')
                        .parent(angular.element(document.querySelector("#toast-placeholder")))
                        .hideDelay(3000)
                    ).then(function() {
                        $timeout(function() {
                            that.showtoast = false
                        }, 500)
                    });
                    _.each(that.bookmap, function(item) {
                        item.editing == false
                    })

                    that.courselist.push(data)
                    that.buildbookmap()
                }, function(data) {
                    that.querystatus = "unset"
                    swal("", "预约失败", "warning")
                })
        }
        that.querySearch = function() {
            var key = that.searchText
            if (key == undefined) {
                that.selecting = that.customerlist
                return
            }
            that.selecting = _.filter(that.customerlist, function(item) {
                return item.displayname.indexOf(key) >= 0 || item.pinyin.replace(/ /g, "").indexOf(key) >= 0
            })
        }

        that.bookmap = []
        that.buildbookmap = function() {
            for (var i in that.timemap) {
                var tmp = that.bookmap[i]
                if (tmp == undefined) {
                    tmp = {}
                    tmp["time"] = that.timemap[i]
                    that.bookmap.push(tmp)
                }
                tmp["editing"] = false
                tmp["book"] = undefined
                tmp["index"] = i
                tmp["extend"] = false
            }
            _.each(that.courselist, function(item) {
                that.bookmap[item.hour]["book"] = item
                that.bookmap[item.hour + 1]["book"] = item
                that.bookmap[item.hour + 1]["extend"] = true
            })
        }

        that.selectcustomer = function(customer) {
            that.selectedItem = customer
            that.searchText = customer.displayname
            that.querySearch()
            that.isSelecting = false
            var c = _.find(that.bookmap, function(item) {
                return item.editing == true
            })
            that.queryOrder(c)
        }


        that.refresh = function() {
            that.searchText = undefined
			if(that.animating == -1){
				that.animating = 0
				$timeout(function(){
					that.animating = -1
				}, 700)
			}
	

            Restangular.one("api", user)
                .one("b", that.selected.Format("yyyyMMdd"))
                .getList()
                .then(function(data) {
                        that.courselist = data
                        that.buildbookmap()
                        console.log(that.bookmap)
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
        that.removebook = function(book) {
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
                var datestr = book.date.replace(/-/g, "")
                Restangular.one("api/", book.coachprofile.name)
                    .one("b/" + datestr, book.hour)
                    .remove()
                    .then(function(data) {
                        swal({
                            type: "success",
                            title: "提交成功",
                            text: "",
                            timer: 1500,
                            showConfirmButton: false
                        });
                        that.courselist = _.reject(that.courselist, function(item) {
                            return item.id == book.id
                        })
                        that.buildbookmap()
                    }, function(data) {
                        swal("", "删除失败", "warning")
                    })

            })
        }
        that.nextweek = function() {
            console.log("next")
			/*
            that.animating = 1
            $timeout(function() {
				that.animating = -1
            }, 700)
			*/
            that.currentdate = that.dates[6].addDays(7)
            that.refreshdates()
        }
        that.prevweek = function() {
            console.log("prev")
			/*
            that.animating = 2
            $timeout(function() {
				that.animating = -1
            }, 700)
			*/

            that.currentdate = that.dates[0].addDays(-7)
            that.refreshdates()
        }
        that.refreshdates = function() {
            var curweekday = that.currentdate.getDay()
            for (var i = 0; i < 7; i++) {
                that.dates[i] = that.currentdate.addDays(i - curweekday)
            }
            that.month = moment(that.currentdate).format('MMMM')
            that.selected = that.dates[curweekday]
            that.refresh()
        }

        that.showcustomer = function(customer) {
            $state.transitionTo("customerdetail", {
                name: customer.name
            })
        }

        that.showorder = function(book) {
            $state.transitionTo("orderdetail", {
                orderid: book.order,
                date: book.date
            })
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
app.controller("OrderDetailCtrlNew", ['$scope', 'Restangular', '$ordersvc', '$usersvc', "$stateParams", "$mdToast", "$booksvc", "$timeout", "$document", "$mdBottomSheet",
    function($scope, Restangular, $ordersvc, $usersvc, $stateParams, $mdToast, $booksvc, $timeout, $document, $mdBottomSheet) {
        var that = this
        that.currentdate = new Date()
        that.dates = []
        that.actionlist = []
        that.user = {}
        that.timemap = TimeMap
        that.orderid = {}
        that.hourstyle = {
            position: "fixed",
            "min-width": "60px",
            "margin-top": "30px"
        }
        that.daystyle = {
                position: "absolute",
                height: "60px",
                "min-height": "60px",
                padding: 0,
                width: "180%",
            }
            //read user
        $usersvc.getuser(undefined, false, function(data) {
            that.user = data
        })

        that.getweekday = function(date) {
            return moment(date).format('dd')
        }


        $scope.scrolled = function(offsetx, offsety) {
            /*"position:fixed;min-width:44px;margin-top: 70px;"	*/
            that.hourstyle["margin-top"] = 30 - offsety + "px"
            that.daystyle['top'] = offsety + "px"
        }
        that.execution = {}
        that.buildexecution = function(action, c, d) {
            if (action == "remove") {
                _.each(that.bookmap, function(item) {
                    item.editing = [false, false, false, false, false, false, false]
                })
                that.execution['action'] = that.removebook
            }
            if (action == "add") {
                _.each(that.bookmap, function(item) {
                    item.stats = [false, false, false, false, false, false, false]
                })
                that.execution['action'] = that.addbook
            }
            that.execution['c'] = c
            that.execution['day'] = d
            that.execution.c.stats[that.execution.day] = "pending"

            $timeout(function() {
                if (c.stats[d] != "inprogress") {
                    c.stats[d] = false
                } else {
                    console.log("ignore")
                }
            }, 5000)
        }
        that.executionstatus = function(stat) {
            that.execution.c.stats[that.execution.day] = stat
        }
        that.execute = function() {
            var tar = that.execution.c.booked[that.execution.day] || that.execution.c.completed[that.execution.day] || that.execution.c.editing[that.execution.day]
            that.execution["action"](tar)
        }
        that.removebook = function(book) {
            that.executionstatus("inprogress")
            $booksvc.remove(book, function(data) {
                that.executionstatus(false)
                $mdToast.show(
                    $mdToast.simple()
                    .parent($document[0].querySelector('.bottom-action-bar'))
                    .textContent('预约已取消')
                    .hideDelay(3000)
                );

                //update booked infomation
                that.execution.c.booked[that.execution.day] = false
                that.execution.c.extend[that.execution.day] = false

                var prev = that.bookmap[that.execution.c.index - 1]
                prev.booked[that.execution.day] = false
                prev.extend[that.execution.day] = false
                    //update na
                that.execution.c.na[that.execution.day] = true
                prev.na[that.execution.day] = true
                    //update status
                that.executionstatus("false")

                that.execution = {}
                that.refreshorder()

            }, function(data) {
                that.executionstatus(false)
                $mdToast.show(
                    $mdToast.simple()
                    .textContent('取消预约失败')
                    .hideDelay(3000)
                );
            })
        }
        that.addbook = function(book) {
            that.executionstatus("inprogress")
            $booksvc.create(that.user.name, book, function(data) {
                that.executionstatus(false)
                $mdToast.show(
                    $mdToast.simple()
                    .parent($document[0].querySelector('.bottom-action-bar'))
                    .textContent('预约已提交')
                    .hideDelay(3000)
                );

                that.execution = {}
                that.refreshorder(that.buildweekmap)

            }, function(data) {
                that.executionstatus(false)
                $mdToast.show(
                    $mdToast.simple()
                    .parent($document[0].querySelector('.bottom-action-bar'))
                    .textContent('取消提交失败')
                    .hideDelay(3000)
                );
            })
        }

        that.editnew = function(c, d) {
            if (c.stats[d]) {
                return
            }
            var next = that.bookmap[parseInt(c.index) + 1]

            //cancel other editing
            _.each(that.bookmap, function(item) {
                item.editing = [false, false, false, false, false, false, false]
            })

            //isvalid
            if (c.booked[d] || c.completed[d] || next.booked[d] || next.booked[d]) {
                return
            }
            if (that.order.booked.length == that.order.course_count) {
                return
            }

            //create new book
            var newbook = {
                date: that.dates[d].Format("yyyy-MM-dd"),
                hour: c.index,
                coach: that.user.id,
                custom: that.order.customerdetail.id,
                order: that.order.id,
            }
            c.editing[d] = newbook
            c.extend[d] = false
            next.editing[d] = newbook
            next.extend[d] = true

        }

        that.refreshorder = function(cb) {
            $ordersvc.getorder($stateParams.orderid,
                function(data) {
                    that.order = data
                    that.completedbook = _.where(data.booked, {
                        done: true
                    })
                    that.bookedbook = _.where(data.booked, {
                            done: false
                        })
                        /*
                    for (var hour in that.bookmap) {
                        var hourdetail = that.bookmap[hour]
                        _.each(that.dates, function(day) {
                            hourdetail.completed.push(false)
                            hourdetail.booked.push(false)
                        })
                    }
					*/
                    _.each(data.booked, function(book) {
                        var dayindex = function() {
                            var i = undefined
                            for (var d in that.dates) {
                                if (that.dates[d].Format("yyyy-MM-dd") == book.date) {
                                    i = parseInt(d)
                                }
                            }
                            return i
                        }()
                        if (dayindex != undefined) {
                            if (book.done) {
                                that.bookmap[book.hour].completed[dayindex] = book
                                that.bookmap[book.hour + 1].completed[dayindex] = book
                                that.bookmap[book.hour + 1].extend[dayindex] = true
                            } else {
                                that.bookmap[book.hour].booked[dayindex] = book
                                that.bookmap[book.hour + 1].booked[dayindex] = book
                                that.bookmap[book.hour + 1].extend[dayindex] = true
                            }
                        }
                    })
                    console.log(that.bookmap)
                    cb && cb()
                },
                function(data) {
                    $mdToast.show(
                        $mdToast.simple()
                        .textContent('获取日程失败')
                        .hideDelay(3000)
                    );
                })
        }
        that.showorderbottom = function() {
            $mdBottomSheet.show({
                templateUrl: '/static/mobile/bottomsheetorder.html',
                controller: 'BottomSheetOrderCtrl',
                clickOutsideToClose: true,
                locals: {
                    order: that.order
                }
            })
        }

        //get current user information
        $usersvc.getuser(undefined, false, function(usr) {
            that.user = usr
        })
        that.refreshdates = function() {
            var wd = that.currentdate.getDay()
                //get start of the day
            that.currentdate = that.currentdate.addDays(-wd)
            curweekday = that.currentdate.getDay()
            if (that.dates.length > 0) {
                curweekday = that.dates[0].getDay()
            }
            for (var i = 0; i < 7; i++) {
                that.dates[i] = that.currentdate.addDays(i - curweekday)
            }
            that.month = moment(that.currentdate).format('MMMM')
            that.buildweekmap()
        }

        //build dateview
        that.bookmap = []
        that.buildweekmap = function() {
            function builddaymap() {
                for (var i in that.timemap) {
                    var tmp = that.bookmap[i]
                    if (tmp == undefined) {
                        tmp = {}
                        tmp["time"] = that.timemap[i]
                        tmp["index"] = i
                        that.bookmap.push(tmp)
                    }
                    tmp["na"] = []
                    tmp["booked"] = [false, false, false, false, false, false, false]
                    tmp["completed"] = [false, false, false, false, false, false, false]
                    tmp["editing"] = [false, false, false, false, false, false, false]
                    tmp["extend"] = [false, false, false, false, false, false, false]
                    tmp["stats"] = [false, false, false, false, false, false, false]
                }
            }

            function getweek() {
                builddaymap()
                var wd = that.currentdate.getDay()
                    //get start of the day
                that.currentdate = that.currentdate.addDays(-wd)
                Restangular.one("api", that.user.name)
                    .all("d/" + that.currentdate.Format("yyyyMMdd"))
                    .getList({
                        days: 7
                    })
                    .then(function(data) {
                            for (var i = 0; i < 7; i++) {
                                var daydetail = data[i]
                                for (var hour in that.bookmap) {
                                    that.bookmap[parseInt(hour)].na.push(daydetail.na.indexOf(parseInt(hour)) < 0)
                                }
                            }

                            that.refreshorder()
                        },
                        function(data) {
                            $mdToast.show(
                                $mdToast.simple()
                                .textContent('获取日程失败')
                                .hideDelay(3000)
                            );
                        })
            }
            getweek()
        }
        that.refreshdates()
    }
])

app.controller("BottomSheetOrderCtrl", function($scope, $mdBottomSheet, order) {
    console.log(order)
    $scope.timemap = TimeMap
    $scope.items = order.booked
})

app.controller("OrderDetailCtrl", ['$scope', 'Restangular', '$mdDialog', '$ordersvc', '$usersvc', "$stateParams", "$timeout",
    function($scope, Restangular, $mdDialog, $ordersvc, $usersvc, $stateParams, $timeout) {
        var that = this
        that.animating = false

        that.currentdate = new Date()
        if ($stateParams.date) {
            that.currentdate = new Date(Date.parse($stateParams.date))
        }

        that.dates = []

        that.actionlist = []

        that.timetable = undefined
        that.user = {}
        $usersvc.getuser(undefined, false, function(usr) {
            that.user = usr
        })


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

            that.animating = true
            $timeout(function() {
                that.animating = false
            }, 700)

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
            that.animating = true
            for (var i = 0; i < 5; i++) {
                that.dates[i] = that.currentdate.addDays(i)
            }
            that.month = moment(that.currentdate).format('MMMM')
            that.select(that.dates[0])
            that.refresh()
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
            $ordersvc.getorder($stateParams.orderid,
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
            $("#order-detail-list").css("height", screen.height - 266 + "px")
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
                    coach: that.user.id,
                    custom: that.order.customerdetail.id,
                    order: that.order.id,
                    pendingaction: "add"
                }
                that.actionlist.push(newbook)
                processtimetable(that.selected)
            }
        }
        that.removebook = function(book) {
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

                var datestr = book.date.replace(/-/g, "")
                Restangular.one("api/", book.coachprofile.name)
                    .one("b/" + datestr, book.hour)
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
                                id: book.id
                            })
                            //tar["pendingaction"] = "remove"
                            //add to actionlist
                            //that.actionlist.push(tar)
                            //remove from bookedbook
                        that.bookedbook = _.reject(that.bookedbook, function(item) {
                                return item.id == book.id
                            })
                            //refresh time table
                            //processtimetable(that.selected)
                        if (that.selected.Format("yyyy-MM-dd") == book.date) {
                            that.timetable.availiable.push(book.hour, book.hour + 1)
                        }
                    }, function(data) {
                        swal("", "删除失败", "warning")
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
                history.back()
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
                history.back()
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
            //that.selected = that.dates[0]

    }
])
app.controller("CustomerDetailCtrl", ["$state", "$usersvc", "Restangular", "$mdDialog", "$ordersvc", "$stateParams",
    function($state, $usersvc, Restangular, $mdDialog, $ordersvc, $stateParams) {
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
            $state.transitionTo("orderdetail", {
                orderid: orderid
            })
        }
        var customername = $stateParams.name
        $usersvc.getcustomer(customername, false, function(data) {
            that.customer = data
            settitle(that.customer.displayname, true)
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
            $mdDialog.hide()
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
        that.mo.subsidy = 0
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

app.controller("TrainDetailCtrl", ["Restangular", "$paramssvc", "$mdDialog", "$uploader", "$booksvc", "$mdToast",
    function(Restangular, $paramssvc, $mdDialog, $uploader, $booksvc, $mdToast) {
        var that = this
        that.editing = false
        that.book = $paramssvc.params["traindetail"]
        that.images = []
        that.title = that.book.customerprofile.displayname + " " + that.book.date + " " + TimeMap[that.book.hour]
        that.cancel = function() {
            $mdDialog.cancel();
        }
        that.uploading = false
        that.addphoto = function($files) {
            that.uploading = true
            $uploader.upload($files[0], function(data) {
                console.log(data.key)
                that.uploading = false
                var imgurl = bukcet + "/" + data.key
                if (that.images.indexOf(imgurl)) {
                    that.images.push(bukcet + "/" + data.key)
                    that.save()
                }
            }, function() {
                that.uploading = false
            })
        }
        that.removephoto = function(img) {
            that.images = _.reject(that.images, function(item) {
                return item == img
            })
            that.save()
        }
        that.showphoto = function(img) {
            $mdToast.show({
                controller: function($scope) {
                    $scope.img = img;
                    $scope.hide = $mdToast.hide
                },
                template: '<md-toast style="position: absolute;top: 0;height: inherit;background: rgb(66,66,66);"  ng-click="hide()"><img  style="margin-top:50px;border-radius:2px" ng-src="{{img}}"></md-toast>',
                hideDelay: 0,
                position: top,
                autoWrap: false,
                parent: angular.element(document.body),
            });
        }

        function loadimgs() {
            if (that.book.detail && that.book.detail.length > 2) {
                var details = JSON.parse(that.book.detail)
                that.images = _.map(_.where(details, {
                    contenttype: "image"
                }), function(item) {
                    return item.content
                })
                console.log(that.images)
            }
        }

        function buildpatchdata() {
            var details = []
            for (var img in that.images) {
                details.push({
                    contenttype: "image",
                    content: that.images[img]
                })
            }
            return JSON.stringify(details)
        }
        that.save = function() {
            that.book.detail = buildpatchdata()
            $booksvc.savedetail(that.book)
        }
        loadimgs()
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
app.controller("OurCourseCtrl", ["$state", "$usersvc", "$date", "Restangular", "$booksvc", "$mdDialog", "$ordersvc", "$scope", "$paramssvc", "$mdToast", "$mdSidenav", "$document", "$mdSidenav", "$timeout",
    function($state, $usersvc, $date, Restangular, $booksvc, $mdDialog, $ordersvc, $scope, $paramssvc, $mdToast, $mdSidenav, $document, $mdSidenav, $timeout) {

        var user = $.cookie("user")
        var that = this
        that.timemap = TimeMap
        that.courselist = []
        that.currentdate = new Date()
        that.dates = []
        that.customerlist = []
        that.selectedItem = undefined
        that.querystatus = "unset"
        that.pendingbook = {}
        that.isSelecting = false
        that.gymid = undefined

        that.back = function() {
            history.back()
        }

        that.init = function() {
            user = $.cookie("user")
            $usersvc.getuser(undefined, false, function(data) {
                    that.user = data
                    that.gymid = that.user.gym_id[0]
                    that.refreshdates()
                },
                function(data) {})

        }

        that.bookmap = []
        that.colors = [
            ["lavenderblush", "rgb(189, 0, 78)"],
            ["rgb(224,247,217)", "rgb(54,98,44)"],
            ["rgb(204,239,255)", "rgb(30,147,213)"],
            ["rgb(242,224,246)", "rgb(77,110,136)"],
            ["rgb(253,243,205)", "rgb(126,99,130)"]
        ]
        that.buildcoaches = function() {
            that.coachset = []
            that.colorset = []
            _.each(that.courselist, function(c) {
                if (that.coachset.indexOf(c.coachprofile.name) < 0) {
                    that.coachset.push(c.coachprofile.name)
                    that.colorset.push(that.colors[that.coachset.indexOf(c.coachprofile.name) % 5])
                }
            })
        }
        that.buildbookmap = function() {
            that.buildcoaches()
            for (var i in that.timemap) {
                var tmp = that.bookmap[i]
                if (tmp == undefined) {
                    tmp = {}
                    tmp["time"] = that.timemap[i]
                    that.bookmap.push(tmp)
                }
                tmp["index"] = i
                tmp["extend"] = []
                tmp["book"] = []
                tmp["color"] = that.colorset
                _.each(that.coachset, function(i) {
                    tmp["extend"].push(false)
                    tmp["book"].push(false)
                })
            }
            _.each(that.courselist, function(item) {
                that.bookmap[item.hour]["book"][that.coachset.indexOf(item.coachprofile.name)] = item
                that.bookmap[item.hour]["extend"][that.coachset.indexOf(item.coachprofile.name)] = false

                that.bookmap[item.hour + 1]["book"][that.coachset.indexOf(item.coachprofile.name)] = item
                that.bookmap[item.hour + 1]["extend"][that.coachset.indexOf(item.coachprofile.name)] = true
            })
        }

        that.refresh = function() {
            that.searchText = undefined
            Restangular.one("api/g", that.gymid)
                .one(that.selected.Format("yyyyMMdd"))
                .getList()
                .then(function(data) {
                        that.courselist = data
                        that.buildbookmap()
                        console.log(that.bookmap)
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
        that.select = function(td) {
            that.selected = td
            that.refresh()
        }
        that.nextweek = function() {
            console.log("next")
            that.currentdate = that.dates[6].addDays(7)
            that.refreshdates()
        }
        that.prevweek = function() {
            console.log("prev")
            that.currentdate = that.dates[0].addDays(-7)
            that.refreshdates()
        }
        that.refreshdates = function() {
            var curweekday = that.currentdate.getDay()
            for (var i = 0; i < 7; i++) {
                that.dates[i] = that.currentdate.addDays(i - curweekday)
            }
            that.month = moment(that.currentdate).format('MMMM')
            that.selected = that.dates[curweekday]
            that.refresh()
        }

        that.showorder = function(book) {
            if (!book) {
                return
            }
            $state.transitionTo("orderdetail", {
                orderid: book.order,
                date: book.date
            })
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
        }
    }
])
