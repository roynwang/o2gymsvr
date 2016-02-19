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
var T = {
    timelineitem: Template7.compile($$("#tpl_timelineitem").html())
}
var R = {
        login: "/api/lg/",
        refreshToken: "/api/t/",
        user: function(phone) {
            return "/api/" + phone + "/"
        }
    }
    /*end init template*/



$$(".isimg").on("click", function() {
    app.photoBrowser({
        photos: [
            "http://img3.imgtn.bdimg.com/it/u=1410273274,160173719&fm=21&gp=0.jpg",
            "http://img3.imgtn.bdimg.com/it/u=1410273274,160173719&fm=21&gp=0.jpg",
            "http://img3.imgtn.bdimg.com/it/u=1410273274,160173719&fm=21&gp=0.jpg",
        ],
        theme: 'dark'
    }).open();
})
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
        },

    ]
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

    function refreshToken(onsuccess) {
        var token = Cookies.get("token")
        if (!token) {
			setTimeout(function(){
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
		setTimeout(function(){
			if(isOK){
				onsuccess()
			}else{
				timeOut = true
			}
		},2700)
        $$.ajax({
            url: R.refreshToken,
            method: "POST",
            data: pdata,
            success: function(data) {
				isOK = true
                Cookies.set("token", JSON.parse(data).token)
				if(timeOut){
	                onsuccess()
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
    var history = undefined

    function init(phone, onsuccess, onfail) {
        $$.ajax({
            url: R.user(phone),
            success: function(data) {
                onsuccess(data)
            },
            function(data) {
                onfail(data)
            }
        })
    }

    function getHistory(onsuccess, onfail) {}
    return {
        init: init,
        getHistory: getHistory
    }
}()





app.onPageInit("home", function(page) {
    var item0 = {
        booking: false,
        date: {
            day: "10",
            month: "十二月"
        },
        showscale: true,
        photos: ["http://img3.imgtn.bdimg.com/it/u=1410273274,160173719&fm=21&gp=0.jpg"],
        showcamera: true
    }
    var item1 = {
        booking: true,
        date: {
            day: "",
            month: ""
        }
    }
    $$("#o2-timeline").prepend(T.timelineitem(item0))
    $$("#o2-timeline").prepend(T.timelineitem(item1))

    svc_login.refreshToken(function() {
        app.closeModal()
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
        function prepareSubmit(ele) {
            var btnp = $$('<p class="animated fadeIn o2-fadeIn" style="display:none"><span class="o2-book-submit">预约</span></p>')
            $$(ele).prepend(btnp)
            var btn = btnp.find(".o2-book-submit")
            btnp.show()

            function submit() {
                if (busy) return;
                btn.html(busycount)
                busy = setInterval(function() {
                    if (busy) {
                        if (busycount.length == 5) {
                            busycount = ""
                        }
                        busycount += "·"
                        btn.html(busycount)
                    } else {
                        btn.html("")
                        btn.addClass("ion-ios-checkmark-empty")
                        btn.addClass("animated o2-pulse")
                        btn.css("font-size", "60px")
                        window.clearInterval(busy)
                        btn.off("click", submit)
                    }
                }, 300)
                busy = true;
                btnp.removeClass("animated slideInRight")
                setTimeout(function() {
                    busy = false
                }, 2000);
            }

            btnp.find(".o2-book-submit").on("click", submit)
        }

        function cleanSubmit() {
            tar.find(".o2-book-hours ul li.booking>p").remove()
            tar.find(".o2-book-hours ul li.booking").toggleClass("booking")
        }
        tar.find(".o2-book-hours ul li").on("click", function(event) {
            if (busy || $$(this).hasClass("booking")) return;
            cleanSubmit()
            $$(this).addClass("booking")
            prepareSubmit($$(this))
        })
    }


    function buildMonthRow(arr) {
        var container = '<div class="accordion-item">' +
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
        var month = '<div class="monthview"><div class="content-block-title">' + curmonth.format("MMMM") + '</div>' +
            '<div class="content-block accordion-list custom-accordion o2-book-month">' +
            '##</div>' +
            '</div></div>';

        var week = []
        var wd = curmonth.format("d")
        var lastday = curmonth.add(1, 'months').subtract(1, "days").format("D")

        for (var i = 0; i < wd; i++) {
            week.push("")
        }

        var weeks = ""
        for (var i = 1; i <= lastday; i++) {
            week.push(i)
            if (week.length == 7) {
                weeks += buildMonthRow(week)
                week = []
            }
        }
        if (week.length != 0) {
            while (week.length != 7) {
                week.push("")
            }
            weeks += buildMonthRow(week)
        }

        return month.replace("##", weeks)
    }

    function loadmore() {
        var months = buildMonth();
        months += buildMonth(1);
        months += buildMonth(2);
        $$(".months").append(months)
    }

    function buildDayView() {
        var rows = '<div class="list-block"><ul>##</ul></div>'
        var hour = '<li class="item-content">' +
            '<div class="item-media"><span class="hour">##</span><span class="min">00</span></div>' +
            '<div class="item-inner"><div class="item-title"></div></div>' +
            '</li>';
        var hourhalf = '<li class="item-content">' +
            '<div class="item-media"><span class="hour hide"></span><span class="min">30</span></div>' +
            '<div class="item-inner"><div class="item-title"></div></div>' +
            '</li>';
        var alltext = ""
        for (var i = 0; i < TimeMap.length; i++) {
            if (i % 2 == 0) {
                alltext += hour.replace("##", 9 + i / 2)
            } else {
                alltext += hourhalf
            }
        }
        return rows.replace("##", alltext);
    }

    loadmore()

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
        current_accordion.find(".o2-book-hours").html(buildDayView());
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
    $$('.accordion-item').on('opened', function(e) {});
});

$$("#booknow").on("click", function() {
        mainView.router.loadPage(pages.bookdetail);
    })
    /*
    $$("#setweight").on("click",function() {
    	weightPicker.open()
    })
    */
