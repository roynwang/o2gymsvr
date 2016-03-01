var HOST = "https://dn-o2fit.qbox.me/"
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
var app = new Framework7({
    template7Pages: true,
    template7Data: {}
});

var $$ = Dom7;
var mainView = app.addView('.view-main');

var pages = {
    "bookdetail": "/static/customermobile/book.html"
}
var TimeMap = ["09:00", "09:30", "10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00", "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", "22:00"]
    //init wx



function range(start, end, step) {
        var ret = []
        if (step == undefined) {
            step = 1
        }
        var tmp = start
        while (tmp <= end) {
            ret.push(tmp)
            tmp += step
        }
        return ret
    }
    /*init template */

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
var T = {
    timelineitem: Template7.compile($$("#tpl_timelineitem").html())
}
var R = {
        login: "/api/lg/",
        refreshToken: "/api/t/",
        wxinit: "/api/wx/signature/",
        user: function(phone) {
            return "/api/" + phone + "/"
        },
        orders: function(phone) {
            return "/api/" + phone + "/o/"
        },
        order: function(phone, orderid) {
            return "/api/" + phone + "/o/" + orderid + "/"
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
    /*end init template*/
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

function notifyFetchPic(mediaid, onsuccess) {
    $$.getJSON(R.picFetch(), {
        mediaid: mediaid
    }, onsuccess)
}



var current_train_weight = undefined

var weightPicker = app.picker({
    input: "#weight-picker",
    toolbarTemplate: '<div class="toolbar"><div class="toolbar-inner"><div class="left"></div><div class="right"><a href="#" class="link close-picker o2-custom">保存</a></div></div></div>',
    cols: [{
        textAlign: 'center',
        values: range(40, 100)
    }, {
        textAlign: 'center',
        values: "."
    }, {
        textAlign: 'center',
        values: range(0, 9)
    }],
    onOpen: function() {
        $$(".close-picker.o2-custom").on("click", function() {
            var weight = $$("#weight-picker").val()
            current_train_weight.setweight(weight.replace(/ /g, ""))
        })
    }
});

var svc_login = function() {
    function login(name, pwd, onsuccess, onfail) {
        var pdata = {
            username: name,
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
    that.onloaded = undefined
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

    function init(phone, onsuccess, onfail, onloaded) {
        that.onloaded = onloaded
        $$.ajax({
            url: R.user(phone),
            success: function(data) {
                usr = JSON.parse(data)
                loadOrders()
                onsuccess(data)
            },
            error: function(data) {
                onfail(data)
            }
        })
    }
	function refreshWhenNeed(skipcallback) {
		if(needReload){
			history = []
			loadOrders(skipcallback)
			needReload = false
		}
	}

    function completeOrderLoad(skipcallback) {
        count_items--;
        if (count_items == 0) {
            history.sort(function(a, b) {
                if(moment(a.date).isAfter(moment(b.date))){
					return 1
				}
				return -1
            })
			if(skipcallback != true){
				that.onloaded(history)
			}
        }
    }

    function loadOrderDetail(order, skipcallback) {
        $$.get(R.order(usr.name, order.id), function(data) {
            var tmp = JSON.parse(data)
			order.booked = tmp.booked
            if (!tmp.detail || tmp.detail == "") {
                tmp.detail = "[]"
            }
            $$.each(tmp.booked, function(i, v) {
                var submit = function(pdata, onsuccess, onfail) {
                    $$.ajax({
                        url: R.train(v),
                        method: "PATCH",
                        data: pdata,
                        success: onsuccess,
                        error: onfail
                    })
                }

                v.setweight = function(weight) {
                    //TODO  set weight
                    var detail = JSON.parse(v.detail)
                    var found = false
                    var pdata = {}
                    $$.each(detail, function(i, v) {
                        if (v.contenttype == "weight") {
                            v.content = weight
                            found = true
                        }
                    })
                    if (!found) {
                        detail.push({
                            "contenttype": "weight",
                            "content": weight
                        })
                    }
                    var pdata = {
                        id: v.id,
                        date: v.date,
                        hour: v.hour,
                        detail: JSON.stringify(detail)
                    }
                    $$.each(history, function(i) {
                        if (history[i].id == v.id) {
                            history[i].detail = JSON.stringify(detail)
                            v.detail = history[i].detail
                            submit(pdata, function() {
                                    that.onloaded(history)
                                },
                                function() {
                                    var noti = app.addNotification({
                                        title: '更新失败',
                                        message: '更新体重数据失败，轻稍后再试',
                                    });
                                    setTimeout(function() {
                                        app.closeNotification(noti)
                                    }, 3000);
                                })
                        }
                    })
                }
                v.addPic = function(imgid) {
                    //upload file
                    var detail = JSON.parse(v.detail)
                    wx.uploadImage({
                        localId: imgid, // 需要上传的图片的本地ID，由chooseImage接口获得
                        isShowProgressTips: 1, // 默认为1，显示进度提示
                        success: function(res) {
                            var serverId = res.serverId; // 返回图片的服务器端ID
                            notifyFetchPic(res.serverId, function(pic) {
                                //TODO
                                //add to train
                                var newpic = {
                                    contenttype: "image",
                                    content: HOST + pic.pic
                                }
                                detail.push(newpic)
                                    //save
                                var pdata = {
                                    id: v.id,
                                    date: v.date,
                                    hour: v.hour,
                                    detail: JSON.stringify(detail)
                                }
                                $$.each(history, function(i) {
                                    if (history[i].id == v.id) {
                                        history[i].detail = JSON.stringify(detail)
                                        v.detail = history[i].detail
                                        submit(pdata, function() {
                                                that.onloaded(history)
                                            },
                                            function() {
                                                var noti = app.addNotification({
                                                    title: '更新失败',
                                                    message: '照片刷新失败，轻稍后再试',
                                                });
                                                setTimeout(function() {
                                                    app.closeNotification(noti)
                                                }, 3000);
                                            })
                                    }
                                })

                            })
                        }
                    });
                    //TODO add pic
                }
                v.getTimeLineCard = function() {
                    var item = {
                            booking: false,
                            date: {
                                day: "10",
                                month: "十二月"
                            },
                            completed: false,
                            showscale: false,
                            weight: 0,
                            //photos: ["http://img3.imgtn.bdimg.com/it/u=1410273274,160173719&fm=21&gp=0.jpg"],
                            photos: [],
                            showcamera: false,
                            id: this.id,
							fromnow: "",
							hourstr: TimeMap[v.hour]
                        }
                        //set date
                    item.id = this.id
                    var date = moment(this.date)
                    item.date.day = date.format("DD")
                    item.date.month = date.format("MMMM")
                        //set photos weight
                    if (!this.detail || this.detail == "") {
                        this.detail = "[]"
                    }

                    var start = moment().subtract(2, "days")
                    var end = moment()
                    var details = JSON.parse(this.detail)
					var delta = date.diff(moment(), "days")
					if(delta > 0){
						item.fromnow = delta+"天后"
					}
					if(delta == 0){
						item.fromnow = "今天"
					}

					if(date.isBefore(end)){
						item.showscale = true
						item.fromnow = false
					}

                    $$.each(details, function(i, v) {
                            if (v.contenttype == "image") {
                                item.photos.push(v.content.fixSize())
                            }
							if (v.contenttype == "weight") {
                                item.showscale = false
                                item.weight = v.content
                            }
						
                        })
                        //set show camera
                    if (date.isBetween(start, end)) {
                        item.showcamera = true
                    }
                    //set done
                    item.completed = this.done

                    return item
                }
                history.push(v)
            })
            if (!order.alltrains) {
                order.alltrains = []
            }
            order.alltrains.push(tmp)
            completeOrderLoad()
        })
    }

    function loadOrders(skipcallback) {
        $$.get(R.orders(usr.name), function(data) {
            usr.orders = JSON.parse(data).results
			usr.history = []
            count_items = usr.orders.length
            $$.each(usr.orders, function(i, v) {
                loadOrderDetail(v)
            })
        })
    }

    function getCurrentOrder() {
        for (var i in usr.orders) {
            var order = usr.orders[i]
            if (order.status != 'done' && order.status != 'unpaid' && order.booked.length < order.course_count) {
                return order
            }
        }
        return false
    }
	function needRefresh(isneed){
		if(isneed == undefined){
			needReload = true
		} else {
		needReload = isneed
		}
	}

    return {
        user: function() {
            return usr
        },
        init: init,
        getCurrentOrder: getCurrentOrder,
        submitBook: submitBook,
		refreshWhenNeed: refreshWhenNeed,
		needRefresh: needRefresh
    }
}()

var home = app.onPageInit("home", function(page) {
    var booking = {
        booking: true,
        date: {
            day: "",
            month: ""
        }
    }
	

    function renderTimeline(history) {
        $$("#o2-timeline").html("")
		var today = moment()
		var tolasttrain = "?"
        for (var i = 0; i < history.length; i++) {
            var v = history[i]
            var item = T.timelineitem(v.getTimeLineCard())
            $$("#o2-timeline").prepend(item)
			if(v.done){
				var tmp = today.diff(moment(v.date), "days")
				if(tolasttrain == "?" || (tmp>=0 && tmp<tolasttrain)){
					tolasttrain = tmp
				}
			}
        }
		console.log(tolasttrain)
		$$("#o2-last-train").html(tolasttrain)
        if (current_train_weight != undefined) {
            $$('.pickweight[data-id="' + current_train_weight.id + '"]').addClass("animated tada")
			current_train_weight = undefined
        }
        $$(".pickweight").on("click", function(e) {
            var tar = this
            e.stopPropagation()
            $$.each(history, function(i, v) {
                if (v.id == tar.dataset["id"]) {
                    weightPicker.open()
                    current_train_weight = v
                    console.log(v.date)
                }
            })
        })
        $$(".camera").on("click", function(e) {
            var tar = this
            e.stopPropagation()
            $$.each(history, function(i, v) {
                if (v.id == tar.dataset["id"]) {
                    console.log("picking img")
                    wx.chooseImage({
                        count: 1, // 默认9
                        sizeType: ['original', 'compressed'], // 可以指定是原图还是压缩图，默认二者都有
                        sourceType: ['album', 'camera'], // 可以指定来源是相册还是相机，默认二者都有
                        success: function(res) {
                            var localIds = res.localIds; // 返回选定照片的本地ID列表，localId可以作为img标签的src属性显示图片
                            v.addPic(localIds[0])
                        }
                    });
                }
            })
        })
		//add booking
		if(svc_usr.getCurrentOrder() && moment().isAfter(moment(history[history.length-1].date))){
	        $$("#o2-timeline").prepend(T.timelineitem(booking))
		}

        $$("#booknow").on("click", function() {
			if(svc_usr.getCurrentOrder()){
	            mainView.router.loadPage(pages.bookdetail);
			} else {
				notify("没有匹配的订单","")
			}
        })
        $$(".isimg").on("click", function(e) {
			var cur = this
            var tar = this.parentElement
            e.stopPropagation()
            $$.each(history, function(i, v) {
                if (v.id == tar.dataset["id"]) {
					var photos = []
					$$.each(JSON.parse(v.detail), function(i, v){
						if(v.contenttype == "image"){
							photos.push(v.content)
						}
					})
                    app.photoBrowser({
                        photos: photos,
                        theme: 'dark',
						ofText: "/",
						backLinkText: "",
						toolbar: false,
						initialSlide: cur.dataset["index"]
                    }).open();
                }
            })
        })

    }

    svc_login.refreshToken(function() {
        svc_usr.init(Cookies.get("user"), function() {
                isBusy = false
                $$("#o2-login-btn").html("登录")
                $$(".o2-book-header-coach img").attr("src", svc_usr.user().avatar.fixSize())
            },
            function() {
                var noti = app.addNotification({
                    title: '读取信息失败',
                    message: '获取用户信息失败，请稍后重试',
                });
                setTimeout(function() {
                    app.closeNotification(noti)
                }, 3000);
            },
            renderTimeline)
    }, function() {
        app.closeModal()
    })
	app.onPageAfterAnimation("home", function(page){
			console.log("I'm backing ... ....")
			svc_usr.refreshWhenNeed()
	})


    var isBusy = false
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
                        isBusy = false
                        $$(".o2-book-header-coach img").attr("src", svc_usr.user().avatar.fixSize())
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
                    }, renderTimeline)

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




app.onPageInit('about', function(page) {
    //busy flat	
    var busy = false
    var busycount = "·"

    // Loading flag
    var loading = false;
    // Last loaded index
    var lastIndex = $$('.list-block .monthview').length;
    // Max items to load
    var maxItems = 10;
    // Append items per load
    var itemsPerLoad = 4;

    var expanding = undefined
    var current_accordion = undefined

    function bindHour(tar) {
        var done = null

        function prepareSubmit(ele) {
            var btnp = $$('<p class="animated fadeIn o2-fadeIn" style="display:none"><span class="o2-book-submit">预约</span></p>')
            $$(ele).prepend(btnp)
            var btn = btnp.find(".o2-book-submit")
            btnp.show()

            function submit() {
                var date = ele.attr("data-date")
                var hour = ele.attr("data-hour")
                if (busy) return;
                btn.html(busycount)
                busy = window.setInterval(function() {
                    if (done == null) {
                        if (busycount.length == 5) {
                            busycount = ""
                        }
                        busycount += "·"
                        btn.html(busycount)
                    }
                    if (done == true) {
                        btn.html("")
                        btn.addClass("ion-ios-checkmark-empty")
                        btn.addClass("animated o2-pulse")
                        btn.css("font-size", "60px")
                        window.clearInterval(busy)
                        btn.off("click", submit)
                        busy = false
                        setTimeout(function() {
                            mainView.router.back();
                            //should refresh
							svc_usr.needRefresh();
                        }, 1300)
                    }
                    if (done == false) {
                        btnp.remove()
                        window.clearInterval(busy)
                        busy = false
                        ele.removeClass("booking")
                        notify("失败", "提交预约失败,请稍后再试")
                    }
                }, 300)
                btnp.removeClass("animated slideInRight")

                var curOrder = svc_usr.getCurrentOrder()
                var newbook = {
                    date: moment(date).format("YYYY-MM-DD"),
                    hour: hour,
                    coach: curOrder.coachdetail.id,
                    custom: svc_usr.user().id,
                    order: curOrder.id
                }
                svc_usr.submitBook(curOrder.coachdetail.name, date, newbook, function(data) {
                    var mdate = moment(ele.attr("data-date"))
                    $$("#o2-book-time .month").html(mdate.format("MM/DD"))
                    $$("#o2-book-time .hour").html(TimeMap[ele.attr("data-hour")])
                    done = true
                }, function(data) {
                    done = false
                })

                /* submit the book */
                /*
                setTimeout(function() {
                    done = false
                }, 2000);
				*/
            }

            btnp.find(".o2-book-submit").on("click", submit)
        }

        function cleanSubmit() {
            tar.find(".o2-book-hours ul li.booking>p").remove()
            tar.find(".o2-book-hours ul li.booking").toggleClass("booking")
        }
        tar.find(".o2-book-hours ul li").on("click", function(event) {
            //if submitted then return
            if (done == true) {
                return
            }
            if (busy || $$(this).hasClass("booking")) return;

            //do not show submit btn if next is na
            if ($$(this).next().find(".o2-hour-status").hasClass("na")) {
                return;
            }
            cleanSubmit()
            $$(this).addClass("booking")
            prepareSubmit($$(this))
        })
    }


    function buildMonthRow(arr, month, monthstr) {
        var container = '<div class="accordion-item" data-month=' + month + ' data-monthstr="' + monthstr + '">' +
            '<div class="accordion-item-toggle row no-gutter o2-book-days">' +
            '##</div>' +
            '<div class="accordion-item-content">' +
            '<div class="row no-gutter"><div class="col-100 o2-timeline-header-hr"></div></div>' +
            '<div class="content-block o2-book-hours o2-bg-gradient"></div>' +
            '</div></div>'
        var row = '<div class="col-auto"><p><span>##</span></p></div>'
        var rows = ""
        $$.each(arr, function(i, v) {
            if (v == "") {
                rows += '<div class="col-auto"></div>'
            } else {
                rows += row.replace("##", v);
            }
        })
        return container.replace("##", rows)
    }

    function buildMonth(m) {
        var days = []
        var curmonth = moment()
        curmonth.set('date', 1)

        if (m != undefined) {
            curmonth = curmonth.add(m, 'months')
        }
        var month = '<div class="monthview"><div class="content-block-title"><span>' + curmonth.format("MMMM") + '</span></div>' +
            '<div class="content-block accordion-list custom-accordion o2-book-month">' +
            '##</div>' +
            '</div></div>';

        var week = []
        var wd = curmonth.format("d")
        var lastday = curmonth.add(1, 'months').subtract(1, "days").format("D")

        for (var i = 0; i < wd; i++) {
            week.push("")
        }
        var datamonth = curmonth.format("YYYYMM")
        var weeks = ""
        for (var i = 1; i <= lastday; i++) {
            week.push(i)
            if (week.length == 7) {
                weeks += buildMonthRow(week, datamonth, curmonth.format("MMMM"))
                week = []
            }
        }
        if (week.length != 0) {
            while (week.length != 7) {
                week.push("")
            }
            weeks += buildMonthRow(week, datamonth, curmonth.format("MMMM"))
        }

        return month.replace("##", weeks)
    }

    function loadmore() {
        var months = buildMonth();
        months += buildMonth(1);
        $$(".months").append(months)
    }

    function setDayView(phone, month, day) {
        var date = month
        if (day.length == 1) {
            day = "0" + day
        }
        date += day
        current_accordion.find("li").attr("data-date", date)
        $$.getJSON(R.coachSchedule(phone, date), function(data) {
            var ava = data.availiable
            var nodes = current_accordion.find(".o2-book-hours .o2-hour-status")
            for (var i = 0; i < TimeMap.length; i++) {
                if (ava.indexOf(i) == -1) {
                    $$(nodes[i]).addClass("na")
                } else {
                    $$(nodes[i]).removeClass("na")
                }
            }
        })
    }

    function buildDayView() {
        //TODO get date status


        var rows = '<div class="list-block"><ul>##</ul></div>'
        var hour = '<li class="item-content" data-hour="#hour#">' +
            '<div class="item-media"><span class="hour">##</span><span class="min">00</span></div>' +
            '<div class="item-inner"><div class="item-title o2-hour-status"><span class="ion-ios-minus"></span></div></div>' +
            '</li>';
        var hourhalf = '<li class="item-content" data-hour="#hour#">' +
            '<div class="item-media"><span class="hour hide"></span><span class="min">30</span></div>' +
            '<div class="item-inner"><div class="item-title o2-hour-status"><span class="ion-ios-minus"></span></div></div>' +
            '</li>';
        var alltext = ""
        for (var i = 0; i < TimeMap.length; i++) {
            if (i % 2 == 0) {
                alltext += hour.replace("##", 9 + i / 2).replace("#hour#", i)
            } else {
                alltext += hourhalf.replace("#hour#", i)
            }
        }
        return rows.replace("##", alltext);
    }

    loadmore()

    $$(".o2-book-header-coach img").attr("src", svc_usr.user().avatar.fixSize())

    $$(".back").on("click", function() {
        mainView.router.back();
    })
    $$(".o2-book-days .col-auto").on("click", function() {
        expanding = $$(this)
    })

    $$("#o2-book-overlay-top, #o2-book-overlay-bottom").on("scroll", function() {
        alert("xxxxxxxxxxxx");
    })
    $$("#o2-book-overlay-top, #o2-book-overlay-bottom").on("click", function() {
        app.accordionClose(current_accordion)
    })
    $$('.accordion-item').on('close', function(e) {
        $$(".o2-book-days .col-auto").removeClass("active")
        $$("#o2-book-overlay-top, #o2-book-overlay-bottom").hide()
        $$(this).find(".o2-book-hours").html("");
    });

    $$('.accordion-item').on('open', function(e) {
        current_accordion = $$(this)
        $$("#o2-book-overlay-top span").html(this.dataset["monthstr"])
        current_accordion.find(".o2-book-hours").html(buildDayView());
        setDayView(svc_usr.getCurrentOrder().coachdetail.name, this.dataset["month"], expanding.find("p>span").html())
    })
    $$('.accordion-item').on('opened', function(e) {
        expanding.addClass("active")
        $$(".months").css("margin-bottom", "400px")
            //set overlay
        current_accordion = $$(this)
        var to = 0;
        var minheight = $$(".page").height() * 0.2

        if (current_accordion.offset().top > minheight) {
            to = $$('#month-scroll').scrollTop() + current_accordion.offset().top - minheight
        }

        function cb() {
            $$("#o2-book-overlay-top").css("height", current_accordion.offset().top + 10 + "px")
            $$("#o2-book-overlay-bottom").css("height", $$(".views").height() - current_accordion.offset().top - 350 + "px")
            $$("#o2-book-overlay-top").addClass("animated fadeIn")
            $$("#o2-book-overlay-bottom").addClass("animated fadeIn")
            $$("#o2-book-overlay-top, #o2-book-overlay-bottom").show()
            e.stopPropagation()
        }
        bindHour(current_accordion)
        if (to <= 0) {
            cb()
        } else {
            //scroll
            $$("#month-scroll").scrollTop(to, 300, cb)
        }
    });
});

/*
$$("#setweight").on("click",function() {
	weightPicker.open()
})
*/
