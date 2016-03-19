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

var app = new Framework7({
    template7Pages: true,
    template7Data: {},
    modalButtonOk: "确认",
    modalButtonCancel: "取消",
    modalTitle: "氧气健身"
});

function notify(title, message, keep) {
    var noti = app.addNotification({
        title: title,
        message: message,
    });
    if (!keep) {
        setTimeout(function() {
            app.closeNotification(noti)
        }, 3000);
    }
}
var pages = {
    "home": "/static/storesale/storesale.html",
    "alipayqr": "/static/storesale/alipayqr.html"
}

var $$ = Dom7;
var mainView = app.addView('.view-main');

var P = [{
    id: 0,
    level: "改变",
    subtitle: "Change",
    course_count: 10,
    off: 9.3,
    price: 3000,
    duration: 2
}, {
    id: 1,
    level: "习惯",
    subtitle: "Habituate",
    course_count: 20,
    off: 8.2,
    price: 5200,
    duration: 4
}, {
    id: 2,
    level: "乐享",
    subtitle: "Enjoy",
    course_count: 40,
    off: 7.0,
    price: 9000,
    duration: 8
}]



var T = {
    coach_avatar: Template7.compile($$("#tpl-coach-avatar").html()),
    product_header: Template7.compile($$("#tpl-product-header").html()),
    product_course_row: Template7.compile($$("#tpl-product-course-row").html()),
    product_course_head: Template7.compile($$("#tpl-product-course-head").html()),
    product_off: Template7.compile($$("#tpl-product-off").html()),
    product_duration: Template7.compile($$("#tpl-product-duration").html()),
    freecourse: Template7.compile($$("#tpl-free-course").html())
}
var R = {
    login: "/api/lg/",
    refreshToken: "/api/t/",
    wxinit: "/api/wx/signature/",
    gym: function(gymid) {
        return "/api/g/" + gymid + "/"
    },
    freecourseitem: function(cid) {
        return "/api/f/" + cid + "/"
    },
    gymfreecourse: function(gymid, date) {
        date = date.replace(/-/g, '')
        return "/api/g/" + gymid + "/d/" + date + "/free/"
    },
    manualorder: function(phone) {
        return "/api/" + phone + "/manualorder/"
    },
    album: function(phone) {
        return "/api/" + phone + "/album/"
    },
    user: function(phone) {
        return "/api/" + phone + "/"
    },
    orders: function(phone) {
        return "/api/" + phone + "/o/"
    },
    order: function(phone, orderid) {
        return "/api/" + phone + "/o/" + orderid + "/"
    },
    order_by_no: function(phone, orderno) {
        return "/api/" + phone + "/b/" + orderno + "/"
    },

    train: function(train) {
        return "/api/" + train.coachprofile.name + "/b/" + train.date.replace(/-/g, "") + "/" + train.hour + "/"
    },
    coachSchedule: function(phone, day) {
        return "/api/" + phone + "/d/" + day + "/"
    },
    book: function(coachname, datestr) {
        return "/api/" + coachname + "/b/" + datestr + "/"
    },
    picFetch: function() {
        return "/api/p/fetch/"
    }
}



var svc_login = function() {
    function login(name, pwd, onsuccess, onfail) {
        var pdata = {
            username: name.replace(" ", ""),
            password: pwd
        }
        $$.ajax({
            url: R.login,
            method: "POST",
            data: pdata,
            success: onsuccess,
            error: onfail
        })
    }

    function refreshToken(onsuccess, afteranimation) {
        var token = Cookies.get("token")
        if (!token) {
            setTimeout(function() {
                $$(".o2-login-form").addClass("o2-login-form-show")
                $$(".o2-login-form").css("opacity", 1)
                $$(".o2-logo").addClass("o2-logo-move-up")
                $$(".o2-logo").css("top", "10%")
            }, 2000)
            return
        }
        var pdata = {
            token: token
        }
        var isOK = false
        var timeOut = false
        setTimeout(function() {
            if (isOK) {
                afteranimation()
            } else {
                timeOut = true
            }
        }, 3000)
        $$.ajax({
            url: R.refreshToken,
            method: "POST",
            data: pdata,
            success: function(data) {
                isOK = true
                onsuccess()
                Cookies.set("token", JSON.parse(data).token)
                if (timeOut) {
                    afteranimation()
                }
            },
            error: function(data) {}
        })

    }
    return {
        login: login,
        refreshToken: refreshToken
    }
}()
var svc_usr = function() {
    var usr = undefined
    var count_items = 0
    var that = this
    var history = []
    var needReload = false

    function submitBook(coachname, datestr, book, onsuccess, onfail) {
        $$.ajax({
            url: R.book(coachname, datestr),
            method: "POST",
            data: book,
            success: onsuccess,
            error: onfail
        })
    }

    function init(phone, onsuccess, onfail) {
        $$.ajax({
            url: R.user(phone.replace(/ /g, "")),
            success: function(data) {
                usr = JSON.parse(data)
                onsuccess(data)
            },
            error: function(data) {
                onfail(data)
            }
        })
    }
    return {
        init: init,
        user: function() {
            return usr
        }
    }
}()

var svc_gym = function() {
    var gym = null
    var coaches = []

    function init(gymid, onsuccess) {
        $$.getJSON(R.gym(gymid), function(data) {
            gym = data
            onsuccess(gym)
            $$.each(gym.coaches_set, function(i, v) {
                coaches.push(v)
                refreshPhoto(v.name, function(data) {
                    v.album = data.results
                })
            })
        })
    }

    function getCoachId(phone) {
        for (var i = 0; i < coaches.length; i++) {
            if (coaches[i].name == phone) {
                return coaches[i].id
            }
        }
        return false
    }

    function newFreeCourse(coachphone, date, hour, onsuccess) {
		var pdata = {
			coach: getCoachId(coachphone),
			day: date.format("YYYY-MM-DD"),
			hour: hour,
			budget: 1,
			sealed: 0,
			displayname: "",
			gym: gym.id
		}
        $$.ajax({
            url: R.gymfreecourse(gym.id, date.format("YYYYMMDD")),
            method: "POST",
            data: pdata,
            success: onsuccess,
            error: function(data) {
                app.hidePreloader()
                console.log(data)
                notify("创建免费课程失败", "")
            }
        })
    }

    function getFreeCourse(date, onsuccess) {
        $$.getJSON(R.gymfreecourse(gym.id, date), onsuccess)
    }

    function cancelFreeCourse(cid, onsuccess) {
        app.showPreloader("正在取消")
        $$.ajax({
            url: R.freecourseitem(cid),
            method: "DELETE",
            success: function(data) {
                app.hidePreloader()
                onsuccess()
            },
            error: function(data) {
                app.hidePreloader()
                console.log(data)
                notify("取消免费课程失败", "")
            }
        })

    }

    function refreshPhoto(phone, onsuccess) {
        $$.getJSON(R.album(phone), onsuccess)
    }
    return {
        gym: function() {
            return gym
        },
        coaches: function() {
            return coaches
        },
        refreshPhoto: refreshPhoto,
        init: init,
        getFreeCourse: getFreeCourse,
        cancelFreeCourse: cancelFreeCourse,
		newFreeCourse: newFreeCourse
    }
}()

var currentCoach = ""
var currentProduct = null
var currentQr = ""
var currentOrderNo = ""


app.onPageInit("home", function(page) {
    app.closePanel()
    var isBusy = false

    function swithCoach(phone) {
        currentCoach = phone
        $$(".coach-item-new").removeClass("active")
        $$("#" + phone).addClass("active")

        function draw(photos) {
            var tmpl = '<div class="coach-img" style="visibility:hidden"><img src="##""></div>'
            $$(".coach-gallary>div").html("")
            var playerphotos = []
            $$.each(photos, function(i, v) {
                playerphotos.push(v.url)
            })

            $$.each(photos, function(i, v) {
                var node = $$(tmpl.replace("##", v.url.fixSize()))
                node.on("click", function() {
                        app.photoBrowser({
                            photos: playerphotos,
                            theme: 'dark',
                            ofText: "/",
                            backLinkText: "",
                            toolbar: false,
                            initialSlide: i
                        }).open();
                    })
                    //node.hide()
                $$(".coach-gallary>div").append(node)
                setTimeout(function() {
                    node.css("visibility", "visible")
                    node.addClass("animated fadeIn")
                }, 300 * Math.random())
            })
        }
        var found = false
        $$.each(svc_gym.coaches(), function(i, v) {
            if (v.name == phone && v.album) {
                draw(v.album)
                found = true
            }
        })
        if (!found) {
            svc_gym.refreshPhoto(phone, function(resp) {
                draw(resp.results)
            })
        }

    }

    function renderCoachesAvatar(coaches) {
        $$.each(coaches, function(i, v) {
				if(v.can_book){
                var node = $$(T.coach_avatar(v))
                node.on("click", function() {
                    swithCoach(v.name)
                })
                $$(".coach-list").prepend(node)
				}
            })
            //$$(".coach-list .coach-item-new:nth-of-type(1)").addClass("active")
        swithCoach(coaches[0].name)
    }
    svc_login.refreshToken(function() {
        svc_usr.init(Cookies.get("user"), function() {
                isBusy = false
				var targym = svc_usr.user().gym_id[0]
				if(!targym){
					targym = JSON.parse(svc_usr.user().corps)[0]
				}
                svc_gym.init(svc_usr.user().gym_id[0], function(gym) {
                    //render avatar
                    renderCoachesAvatar(gym.coaches_set)
                })
                isBusy = false
                $$("#o2-login-btn").html("登录")
                app.closeModal()
            },
            function() {
                var noti = app.addNotification({
                    title: '读取信息失败',
                    message: '获取用户信息失败，请稍后重试',
                });
                setTimeout(function() {
                    app.closeNotification(noti)
                }, 3000);
            })
    }, function() {
        app.closeModal()
    })
    $$("#o2-login-btn-touch").on("click", function() {
        if (isBusy) return
        isBusy = true
        var toast = $$('<span class="preloader"></span>')
        $$("#o2-login-btn").html("")
        $$("#o2-login-btn").append(toast)
        svc_login.login($$("#phone").val(), $$("#pwd").val(),
            function(data) {
                //write to cookie
                Cookies.set("user", $$("#phone").val(), {
                    expires: 365
                })
                var t = JSON.parse(data).token
                Cookies.set("token", t, {
                    expires: 365
                })
                svc_usr.init($$("#phone").val(), function() {
                        svc_gym.init(svc_usr.user().gym_id[0], function(gym) {
                            //render avatar
                            renderCoachesAvatar(gym.coaches_set)
                        })
                        isBusy = false
                        console.log(data);
                        $$("#o2-login-btn").html("登录")
                        app.closeModal()
                    },
                    function() {
                        var noti = app.addNotification({
                            title: '读取信息失败',
                            message: '获取用户信息失败，请稍后重试',
                        });
                        setTimeout(function() {
                            app.closeNotification(noti)
                        }, 3000);
                    }, function() {
                        console.log("xxxxxxxxxxx")
                    })

            },
            function(data) {
                isBusy = false
                console.log(data)
                var noti = app.addNotification({
                    title: '登录失败',
                    message: '请检查输入后重试',
                });
                setTimeout(function() {
                    app.closeNotification(noti)
                }, 3000);
                $$("#o2-login-btn").html("登录")
            })
    })
}).trigger()


app.onPageInit("price", function(page) {
    console.log(currentCoach)

    function renderCourse(num) {
        $$(".price-detail-price").html("")
        $$(".price-detail-price").append(T.product_course_head({
            count: num
        }))
        var rowcount = Math.floor(num / 10)
        for (var i = 0; i < rowcount; i++) {
            $$(".price-detail-price").append(T.product_course_row())
        }
        var half = num % 10
        if (half != 0) {
            var last = $$(T.product_course_row())
            var m = $$(".price-detail-price").append(last)
            for (var i = 10; i >= half; i--) {
                var t = 10 - i
                $$(".price-detail-price .price-detail-item-iconrow:nth-last-of-type(1)>div:nth-of-type(" + t + ")>.course-item").addClass("hide")
            }
        }
    }

    function renderOff(num) {
        $$(".price-detail-off").html("")
        $$(".price-detail-off").append(T.product_off({
            num: num
        }))
        $$(".price-detail-off .price-detail-off-percent").css("width", (10 - num + 1) * 10 + "%")
        $$(".price-detail-off .price-detail-on-percent").css("width", (num - 1) * 10 + "%")
    }

    function renderDuration(num) {
        var tpl = '<span class="ion-ionic active"></span>'
        $$(".price-detail-duration").html("")
        $$(".price-detail-duration").append(T.product_duration({
            num: num
        }))
        for (var i = 0; i < Math.ceil(num); i++) {
            $$(".price-detail-duration .price-detail-duration-iconrow").append(tpl)
        }
    }

    function swichProduct(i) {
        $$(".price-item").removeClass("active")
        $$("#product" + i).addClass("active")
        currentProduct = P[i]
        renderCourse(P[i].course_count)
        renderOff(P[i].off)
        renderDuration(P[i].duration)
        var len = P[i].price.toString().length
        var head = P[i].price.toString().substr(0, len - 3)
        var tail = "," + P[i].price.toString().substr(len - 3)
        $$("#price-head").html(head)
        $$("#price-tail").html(tail)

    }

    function renderProductHeader() {
        $$.each(P, function(i, v) {
            var node = $$(T.product_header(v))
            node.on("click", function() {
                swichProduct(i)
            })
            $$(".price-row").append(node)
        })
    }
    renderProductHeader()
    swichProduct(1)
})

app.onPageInit("customerform", function(page) {
    var that = this;

    function validate() {
        if (that.mo.subsidy == undefined) {
            that.mo.subsidy = 0
        }
        if (that.birthday_str) {
            that.mo.birthday = that.birthday_str
        }
        if (that.mo.age == undefined) {
            that.mo.age = 0
        }
        var data = that.mo
        if (that.mo.customer_phone.toString().length != 11) {
            notify("订单信息错误", "请输入正确的11位电话号码")
            return false
        }
        for (var k in data) {
            if (data[k] == undefined) {
                notify("订单信息错误", "请填完所有选项")
                return false
            }
        }
        return true
    }
    $$("#offline-submit").on("click", function() {
        buildOrder()
        if (!validate()) {
            return
        }
        app.confirm('确定支付已经完成了吗?', function() {
            app.showPreloader('订单创建中')
            var onsuccess = function(resp) {
                resp = JSON.parse(resp)
                app.hidePreloader()
                notify("支付成功", "支付成功,祝您健身愉快")
                setTimeout(function() {
                    mainView.router.loadPage(pages.home)
                }, 1500)
            }
            $$.ajax({
                url: R.manualorder(currentCoach),
                method: "POST",
                data: that.mo,
                success: onsuccess,
                error: function(data) {
                    app.hidePreloader()
                    console.log(data)
                    notify("创建订单失败", "")
                }
            })
        })
    })

    function buildOrder() {
        that.mo = {}
        that.mo.customer_displayname = ""
        that.mo.customer_phone = ""
        that.mo.product_price = ""
        that.mo.product_promotion = -1
        that.mo.product_amount = ""
        that.mo.product_duration = 0
        that.mo.sex = '0'
        that.mo.age = undefined
        that.mo.subsidy = undefined
		that.mo.advance = true

        that.birthday_str = $$("#customerbirtyday").val()
        that.mo.customer_displayname = $$("#customername").val()
        that.mo.customer_phone = $$("#customerphone").val()
        that.mo.sex = $$("#customersex").val()
        that.mo.product_price = currentProduct.price
        that.mo.product_amount = currentProduct.course_count
        that.mo.product_introduction = "氧气健身: 私教课 " +  currentProduct.course_count + "节"
    }

    $$("#alipay-submit").on("click", function() {
        currentQr = ""
        buildOrder()
        if (!validate()) {
            return
        }

        app.confirm('确认提交吗?', function() {
            that.mo.channel = "alipay_qr"

            app.showPreloader('订单创建中')

            var onsuccess = function(resp) {
                resp = JSON.parse(resp)
                currentQr = resp.credential.alipay_qr
                currentOrderNo = resp.order_no
                app.hidePreloader()
                mainView.router.loadPage(pages.alipayqr)
            }

            $$.ajax({
                url: R.manualorder(currentCoach),
                method: "POST",
                data: that.mo,
                success: onsuccess,
                error: function(data) {
                    app.hidePreloader()
                    console.log(data)
                    notify("创建订单失败", "")
                }
            })
        });
    })
})

app.onPageInit("alipayqr", function(page) {
    $$("#ali-qr-area").attr("src", currentQr)
    var node = qr.image(currentQr)
    $$("#qrarea").append(node)

    function checkorder(onsuccess, onfail) {
        $$.ajax({
            url: R.order_by_no(currentCoach, currentOrderNo),
            method: "GET",
            success: onsuccess,
            error: onfail
        })
    }
    $$("#pay-done").on("click", function() {
        app.showPreloader('查询中')
        checkorder(function(data) {
                var order = JSON.parse(data)
                app.hidePreloader()
                if (order.status == "paid" || order.status == "inprogress") {
                    notify("支付已确认", "支付成功,祝您健身愉快")
                    setTimeout(function() {
                        mainView.router.loadPage(pages.home)
                    }, 1500)
                } else {
                    app.alert("还未查询到您的支付信息，请支付完成后点击该按钮")
                }
            },
            function() {
                app.hidePreloader()
                app.alert("查询支付状态失败,轻稍后再试")
            })
    })
})
app.onPageAfterAnimation("storemanage", function(page){
    app.closePanel()
    app.modalPassword('请再次输入密码', function(password) {
        svc_login.login(Cookies.get("user"), password, function() {
            notify("成功", "密码验证通过")
        }, function() {
            alert("密码验证失败")
            mainView.router.back()
        })
    });
})
app.onPageInit("storemanage", function(page) {
    var currentdate = moment(new Date())

    function cancelFreeCourse(cid) {
        svc_gym.cancelFreeCourse(cid, function() {
            notify("成功", "免费课程已取消")
            refresh()
        })
    }

    function refresh(date) {
        if (date == undefined) {
            date = currentdate
        } else {
            date = moment(date)
            currentdate = date
        }
        svc_gym.getFreeCourse(date.format("YYYY-MM-DD"), function(resp) {
            $$("#day-free-course").html("")
                //wrap course
            $$.each(resp, function(i, v) {
                v.hour_str = TimeMap[v.hour]
                if (v.customer == null) {
                    v.nocustomer = true
                }
				v.sexstr = "男"
				if(!v.sex){
					v.sexstr = "女"
				}
                $$("#day-free-course").append(T.freecourse(v))
            })
            $$(".cancel-course").on("click", function() {
                var cid = this.dataset["id"]
                app.confirm("确认取消吗", function() {
                    cancelFreeCourse(cid)
                })
            })
        })
    }

    var calendarDefault = app.calendar({
        input: '#calendar-default',
        closeOnSelect: true,
        value: [new Date()],
        onClose: function(p) {
            refresh(p.input.val())
        }
    });
    refresh()
})

app.onPageInit("freecourseform", function(page) {
    var currentdate = moment(new Date())
    var calendarDefault = app.calendar({
        input: '#free-course-date',
        closeOnSelect: true,
        value: [new Date()],
        onClose: function(p) {
            renderhour(p.input.val())
        }
    });

    function rendercoach() {
        $$("#free_coach").html("")
        var tmpl = '<option value="#phone#">#name#</option>'
        $$.each(svc_gym.coaches(), function(i, v) {
            $$("#free_coach").append(tmpl.replace("#phone#", v.name).replace("#name#", v.displayname))
        })
        renderhour()
    }

    function renderhour(date) {
        if (date == undefined) {
            date = currentdate
        } else {
            date = moment(date)
            currentdate = date
        }
        var coach = $$("#free_coach").val()
        $$.getJSON(R.coachSchedule(coach, date.format("YYYYMMDD")), function(resp) {
            $$("#free_hour").html("")
            var tmpl = '<option value="#hour#">#hour_str#</option>'
            $$.each(resp.availiable, function(i, v) {
                $$("#free_hour").append(tmpl.replace("#hour#", v).replace("#hour_str#", TimeMap[v]))
            })
        })
    }
    $$("#free-course-submit").on("click", function() {
		svc_gym.newFreeCourse($$("#free_coach").val(),
			moment($$("#free-course-date").val()), 
			$$("#free_hour").val(),
			function(){
				notify("成功","添加免费课程成功")
				/*
				setTimeout(function(){
		            mainView.router.back()
				}, 2000)
				*/
			})
    })

    $$("#free_coach").on("change", function() {
        renderhour()
    })

    rendercoach()

})
