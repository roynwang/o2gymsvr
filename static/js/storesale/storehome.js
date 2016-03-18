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

var freecourse = ""
var currentCoach = ""

var WeekDays = ["日", "一", "二", "三", "四", "五", "六"]
var TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]

var app = new Framework7({
    template7Pages: true,
    template7Data: {},
    modalButtonOk: "确认",
    modalButtonCancel: "取消",
    modalTitle: "氧气健身"
});
Date.prototype.addDays = function(days) {
    var dat = new Date(this.valueOf());
    dat.setDate(dat.getDate() + days);
    return dat;
}



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
    "home": "/static/storesale/storehome.html",
    "alipayqr": "/static/storesale/alipayqr.html",
    "bookfree": "/static/storesale/bookfree.html",
    "firstcustomerform": "/static/storesale/firstcustomerform.html"
}

var $$ = Dom7;
var mainView = app.addView('.view-main');
var T = {
    coachintroduction: Template7.compile($$("#tpl-coach-introduction").html()),
    coachfree: Template7.compile($$("#tpl-coach-free").html())
}

var R = {
        login: "/api/lg/",
        refreshToken: "/api/t/",
        wxinit: "/api/wx/signature/",
        gym: function(gymid) {
            return "/api/g/" + gymid + "/"
        },
        customerfreecourse: function(phone) {
            return "/api/" + phone + "/free/"
        },
        coachfreecourse: function(phone) {
            return "/api/" + phone + "/coachfree/"
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
    /*
    $$.post(R.wxinit, {
        url: window.location.href
    }, function(data) {
        var config = JSON.parse(data)
        config.jsApiList = ["chooseImage", "uploadImage"] // 必填，需要使用的JS接口列表，所有JS接口列表见附录2
        config.debug = false
        wx.config(config);
        wx.ready(function() {
            console.log("load wechat success")
                // config信息验证后会执行ready方法，所有接口调用都必须在config接口获得结果之后，config是一个客户端的异步操作，所以如果需要在页面加载时就调用相关接口，则须把相关接口放在ready函数中调用来确保正确执行。对于用户触发时才调用的接口，则可以直接调用，不需要放在ready函数中。
        });
        wx.error(function(res) {
            alert("load wechat sdk fail")
        })
    })
    */

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

    function refreshFreeCourse(phone, onsuccess) {
        $$.getJSON(R.coachfreecourse(phone), onsuccess)
    }

    function getCoach(phone) {
        for (var i = 0; i < coaches.length; i++) {
            if (coaches[i].name == phone) {
                return coaches[i]
            }
        }
        return false;
    }
    return {
        gym: function() {
            return gym
        },
        coaches: function() {
            return coaches
        },
        refreshPhoto: refreshPhoto,
        refreshFreeCourse: refreshFreeCourse,
        init: init,
        getFreeCourse: getFreeCourse,
        cancelFreeCourse: cancelFreeCourse,
        newFreeCourse: newFreeCourse,
        getCoach: getCoach
    }
}()




app.onPageInit("gymhome", function(page) {
    var basedate = new Date().addDays(1)
    var dates = [0, 0, 0, 0, 0, 0, 0]
    var selected = false
    var month = false

    function getgymdayfree(tar) {
        if (moment(tar).format("YYYYMMDD") < moment().format("YYYYMMDD")) {
            $$(".free-date-detail").html('<p style="text-align:center;font-size:20px;color:#aaa;margin-top:80px">选错日期了，换一天试试</p>')
            return
        }

        svc_gym.getFreeCourse(moment(tar).format("YYYYMMDD"), function(data) {
            $$(".free-date-detail").html("")
            if (data.length == 0) {
                $$(".free-date-detail").html('<p style="text-align:center;font-size:20px;color:#aaa;margin-top:80px">今天没有课程，换一天试试</p>')
                return
            }
            $$.each(data, function(i, v) {
                v.hour_str = TimeMap[v.hour]
                v.endhour_str = TimeMap[v.hour + 2]
                v.availiable = true
                if (v.sealed == 1) {
                    v.availiable = false
                }
                $$(".free-date-detail").append(T.coachfree(v))
            })
            $$(".free-coachavatar").on("click", function() {
                var playerphotos = []
				var coach = svc_gym.getCoach($$(this).attr("data-coach"))
                playerphotos.push(coach.avatar)
                $$.each(coach.album, function(i, v) {
                    playerphotos.push(v.url)
                })
                app.photoBrowser({
                    photos: playerphotos,
                    theme: 'dark',
                    ofText: "/",
                    backLinkText: "",
                    toolbar: false,
                    initialSlide: 0
                }).open();
            })

            $$(".book-free-round").on("click", function() {
                if ($$(this).hasClass("disable")) {
                    return
                }
                freecourse = $$(this).attr("data-freeid")
                if (freecourse == "-1") {
                    app.alert("请先选择时段")
                    return
                }
                mainView.router.loadPage(pages.bookfree)
            })
        })
    }

    function renderDate() {
        $$(".free-date-row").html("")
        $$("#month-str").html(month)
        var dayitem = '<div data-daystr="#daystr#" class="col-auto free-date-item"><p class="free-date-weekday">#weekday#</p><p class="free-date-day">#day#</p></div>'
        for (var i = 0; i < 7; i++) {
            var weekday = WeekDays[i]
            var day = moment(dates[i]).format("D")
            var daystr = moment(dates[i]).format("YYYYMMDD")
            var stat = ""
            if (moment().format("YYYYMMDD") > moment(dates[i]).format("YYYYMMDD")) {
                stat = "disable"
            }
            $$(".free-date-row").append(dayitem.replace("#stat#", stat).replace("#weekday#", weekday).replace("#day#", day).replace("#daystr#", daystr))
        }
        $$(".free-date-item").on("click", function() {
            selectDate(moment($$(this).attr("data-daystr")))
        })
        selectDate(selected)
    }

    function selectDate(tar) {
        if (tar) {
            selected = tar
        }
        $$('.free-date-item').removeClass("active")
        $$('.free-date-item[data-daystr="' + moment(selected).format("YYYYMMDD") + '"]').addClass("active")
        getgymdayfree(selected)
    }

    function fillDateRow() {
        var curweekday = basedate.getDay()
        for (var i = 0; i < 7; i++) {
            dates[i] = basedate.addDays(i - curweekday)
        }
        month = moment(basedate).format('MMMM')
        selected = dates[curweekday]
        renderDate()
    }

    function getcurrentgym() {
        var currentUrl = window.location.href;
        return currentUrl.split("/")[4]
    }


    function renderFreeCourse(coach) {
        svc_gym.refreshFreeCourse(coach.name, function(resp) {
            coach.freecourse = resp
            if (coach.freecourse.length == 0) {
                $$("#free-" + coach.name + "-row").hide()
            }
        })
    }

    function renderCoach(coach) {
        var playerphotos = []
        playerphotos.push(coach.avatar)
        coach.playerphotos = []
        $$.each(coach.album, function(i, v) {
            if (i < 6) {
                playerphotos.push(v.url)
                coach.playerphotos.push({
                    ind: i + 1,
                    name: coach.name,
                    url: v.url
                })
            }
        })
        $$("#coach-introduction-card").append(T.coachintroduction(coach))
        $$('div[data-phone="' + coach.name + '"]').on("click", function() {
            app.photoBrowser({
                photos: playerphotos,
                theme: 'dark',
                ofText: "/",
                backLinkText: "",
                toolbar: false,
                initialSlide: this.dataset["id"]
            }).open();
        })
        renderFreeCourse(coach)
        $$("#book-now-" + coach.name).on("click", function() {
            currentCoach = coach.name
            mainView.router.loadPage(pages.firstcustomerform)
        })
        $$("#free-" + coach.name).on("click", function() {
            var clickedLink = this;
            var tpl = '<li><a data-course="#id#" class="free-course-option list-button item-link" style="color:rgb(87,193,199)">#timestr#</a></li>'
            var options = ""
            $$("#popover-freecourse ul").html("")
            if (coach.freecourse.length == 0) {
                return;
            }
            $$.each(coach.freecourse, function(i, v) {
                $$("#popover-freecourse ul").append(tpl.replace(/#id#/, v.id).replace(/#timestr#/, v.day.replace(/-/g, "/").substr(5) + " " + TimeMap[v.hour]))
            })
            $$(".free-course-option").on("click", function() {
                app.closeModal()
                $$("#free-" + coach.name).html(this.text)
                $$("#free-" + coach.name).attr("data-course", this.dataset["course"])
            })
            app.popover('#popover-freecourse', clickedLink);
        })
        $$('#book-free-' + coach.name).on("click", function() {
            //TODO
            freecourse = $$("#free-" + coach.name).attr("data-course")
            if (freecourse == "-1") {
                app.alert("请先选择时段")
                return
            }
            mainView.router.loadPage(pages.bookfree)
        })


        /*
		var w = (screen.width-20)/5
        $$('div[data-phone="' + coach.name + '"] .coach-photo').width(w)
        $$('div[data-phone="' + coach.name + '"] .coach-photo').height(w)
		*/


        /*
		var node = $('<div class="col-33 coach-dating" style="position:relative;"><div class="coach-dating-btn">约</div></div>')
		var w = (screen.width-20)/5
		node.height(w)
		node.width(w)
		node.css("line-height", w + "px")
        $('div[data-coach="' + coach.name + '"] .coach-photos').append(node)
		if(coach.album.length != 0 ){
			node.css({top: -w +"px"})
		}
		*/
    }

    function renderCoaches(gym) {
        $$.each(gym.coaches_set, function(i, v) {
            if (v.can_book) {
                svc_gym.refreshPhoto(v.name, function(data) {
                    v.album = data.results
                    renderCoach(v)
                })
            }
        })
    }


    function renderSwiper(gym) {
        var pictmp = '<div><img style="width:100%" src="##"></div>'
        $$.each(JSON.parse(gym.imgs), function(i, v) {
            if (i < 3) {
                $$("#gym-pics").append(pictmp.replace("##", v))
            }
        })

        /*
        var mySwiper = app.swiper('.swiper-container', {
            speed: 400,
            spaceBetween: 0,
            pagination: '.swiper-pagination',
            autoplay: 10000
        });
		*/
    }
    svc_gym.init(getcurrentgym(), function(gym) {
        renderSwiper(gym)
            //render avatar
        renderCoaches(gym)
        fillDateRow()

        $$("#contact-me").on("click", function() {
            app.closeModal()
            app.alert(gym.phone)
        })
    })

    function nextweek(e) {
        basedate = dates[0].addDays(7)
        fillDateRow()
    }

    function prevweek(e) {
        basedate = dates[0].addDays(-7)
        fillDateRow()
    }
    $$(".prev-week-btn").on("click", prevweek)
    $$(".next-week-btn").on("click", nextweek)

}).trigger()

app.onPageInit("bookfree", function(page) {
    setTimeout(function() {
        app.alert("每个人只有一次免费体验的机会，并且你约了别人就不能约了。所以当你不能来的时候请及时在主页右上角菜单中取消预约。")
    }, 1000)
    $$("#book-free-submit").on("click", function() {
        var cid = freecourse
        var cp = $$("#customerphone").val()
        if (cp.length != 11) {
            app.alert("请输入正确的电话号码")
            return
        }
        if ($$("#customerdisplayname").val().length == 0) {
            app.alert("请输入您的姓名")
            return
        }

        app.showPreloader("预约中")
        $$.ajax({
            url: R.freecourseitem(cid),
            method: "PATCH",
            data: {
                customer: cp,
                displayname: $$("#customerdisplayname").val(),
                sex: $$("#customersex").val()
            },
            success: function(data) {
                app.hidePreloader()
                var resp = JSON.parse(data)
                if (resp.error == "existed") {
                    app.alert("您已经使用过免费体验机会了")
                    return
                }
                if (resp.error == "sealed") {
                    app.alert("已经被别人秒掉了，下次要手快哦!")
                    return
                }
                app.alert("预约成功，请准时前来。如有变更请及时取消。", function() {
                    mainView.router.back()
                })
            },
            error: function(data) {
                app.hidePreloader()
                console.log(data)
                notify("提交失败", "")
            }
        })

    })
})

app.onPageInit("cancelfree", function(page) {
    app.closeModal()
    $$("#cancel-free-submit").on("click", function() {
        var cid = freecourse
        var cp = $$("#cancelphone").val()
        if (cp.length != 11) {
            app.alert("请输入正确的电话号码")
            return
        }

        function cancel(cid) {
            app.showPreloader("取消中")
            $$.ajax({
                url: R.freecourseitem(cid),
                method: "PATCH",
                data: {
                    customer: "-1"
                },
                success: function(data) {
                    app.hidePreloader()
                    app.alert("已经取消", function() {
                        mainView.router.back()
                    })
                },
                error: function(data) {
                    app.hidePreloader()
                    console.log(data)
                    notify("提交失败", "")
                }
            })
        }

        app.showPreloader("查询中")
        $$.ajax({
            url: R.customerfreecourse(cp),
            method: "GET",
            success: function(data) {
                app.hidePreloader()
                var f = JSON.parse(data)
                cancel(f.id)
            },
            error: function(data) {
                app.hidePreloader()
                console.log(data)
                notify("未查询到结果", "")
            }
        })

    })
})
app.onPageInit("firstcustomerform", function(page) {
    var that = this;
    var mySwiper = app.swiper('.swiper-container-2', {
        speed: 400,
        spaceBetween: 0,
        autoplay: 10000
    });


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
    $$("#coach-name").html(svc_gym.getCoach(currentCoach).displayname)

    $$("#hide-introduction, .next-step").on("click", function() {
        $$("#customerform").show()
        $$("#customerform").addClass("fadeIn animated")
        $$("#introduction").addClass("fadeOutLeft animated")
        setTimeout(function() {
            $$("#introduction").hide()
        }, 500)
    })

    function buildOrder() {
        that.mo = {}
        that.mo.customer_displayname = ""
        that.mo.customer_phone = ""
        that.mo.product_introduction = "dummy"
        that.mo.product_price = ""
        that.mo.product_promotion = -1
        that.mo.product_amount = ""
        that.mo.product_duration = 0
        that.mo.sex = '0'
        that.mo.age = undefined
        that.mo.subsidy = undefined

        that.birthday_str = $$("#customerbirtyday").val()
        that.mo.customer_displayname = $$("#customername").val()
        that.mo.customer_phone = $$("#customerphone").val()
        that.mo.sex = $$("#customersex").val()
        that.mo.product_price = 120
        that.mo.product_amount = 1
    }
    $$("#wx-submit").on("click", function() {
        currentQr = ""
        buildOrder()
        if (!validate()) {
            return
        }
        app.confirm('确认提交吗?', function() {
            that.mo.channel = "alipay_wap"
            app.showPreloader('订单创建中')

            var onsuccess = function(resp) {
                app.hidePreloader()
                resp = JSON.parse(resp)
                pingpp.createPayment(resp, function(result, error) {
                        console.log(result)
                        if (result == "success") {
                            // 只有微信公众账号 wx_pub 支付成功的结果会在这里返回，其他的 wap 支付结果都是在 extra 中对应的 URL 跳转。
                        } else if (result == "fail") {
                            // charge 不正确或者微信公众账号支付失败时会在此处返回
                        } else if (result == "cancel") {
                            // 微信公众账号支付取消支付
                        }
                    })
                    /*
                currentQr = resp.credential.alipay_qr
                currentOrderNo = resp.order_no
                app.hidePreloader()
                mainView.router.loadPage(pages.alipayqr)
				*/
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
