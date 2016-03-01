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
var pages = {
    "productpage": "/static/storesale/storesale.html"
}

var $$ = Dom7;
var mainView = app.addView('.view-main');

var P = [
	{id: 0,
	level:"1",
	 subtitle:"Change",
	 course_count: 10,
	 off: 9,
	 price: 2700,
	 duration: 1},
	{id: 1,
	level:"2",
	 subtitle:"Habituate",
	 course_count: 20,
	 off: 8.5,
	 price: 5000,
	 duration: 6},
	{ id:2,
     level:"3",
	 subtitle:"Enjoy",
	 course_count: 40,
	 off: 6.6,
	 price: 8000,
	 duration: 12}
]



var T = {
    coach_avatar: Template7.compile($$("#tpl-coach-avatar").html()),
	product_header: Template7.compile($$("#tpl-product-header").html()),
	product_course_row: Template7.compile($$("#tpl-product-course-row").html()),
	product_course_head: Template7.compile($$("#tpl-product-course-head").html()),
	product_off: Template7.compile($$("#tpl-product-off").html()),
	product_duration: Template7.compile($$("#tpl-product-duration").html())
}
var R = {
    login: "/api/lg/",
    refreshToken: "/api/t/",
    wxinit: "/api/wx/signature/",
    gym: function(gymid) {
        return "/api/g/" + gymid + "/"
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
            username: name.replace(" ",""),
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
            url: R.user(phone.replace(/ /g,"")),
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
        init: init
    }
}()

var currentCoach = ""


app.onPageInit("home", function(page) {
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
                }, 1000 * Math.random())
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
                var node = $$(T.coach_avatar(v))
                node.on("click", function() {
                    swithCoach(v.name)
                })
                $$(".coach-list").prepend(node)
            })
            //$$(".coach-list .coach-item-new:nth-of-type(1)").addClass("active")
        swithCoach(coaches[0].name)
    }
    svc_login.refreshToken(function() {
        svc_usr.init(Cookies.get("user"), function() {
                isBusy = false
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

	function renderCourse(num){
		$$(".price-detail-price").html("")
		$$(".price-detail-price").append(T.product_course_head({count:num}))
		var rowcount = Math.floor(num/10)
		for(var i=0; i<rowcount; i++){
			$$(".price-detail-price").append(T.product_course_row())
		}
		var half = num%10
		if(half != 0){
			var last = $$(T.product_course_row())
			var m = $$(".price-detail-price").append(last)
			for(var i = 10; i >= half; i--){
				var t = 10 - i
				$$(".price-detail-price .price-detail-item-iconrow:nth-last-of-type(1)>div:nth-of-type("+ t + ")>.course-item").addClass("hide")
			}
		}
	}
	function renderOff(num){
		$$(".price-detail-off").html("")
		$$(".price-detail-off").append(T.product_off({num:num}))
		$$(".price-detail-off .price-detail-off-percent").css("width", (10-num +1)*10 + "%")
		$$(".price-detail-off .price-detail-on-percent").css("width", (num-1)*10 + "%")
	}
	function renderDuration(num){
        var tpl = '<span class="ion-ionic active"></span>'
		$$(".price-detail-duration").html("")
		$$(".price-detail-duration").append(T.product_duration({num:num}))
		for(var i = 0; i<Math.ceil(num);i++){
			$$(".price-detail-duration .price-detail-duration-iconrow").append(tpl)
		}
	}
	function swichProduct(i){
		$$(".price-item").removeClass("active")
		$$("#product" + i).addClass("active")
		renderCourse(P[i].course_count)
		renderOff(P[i].off)
		renderDuration(P[i].duration)
		var len = P[i].price.toString().length
	    var head = P[i].price.toString().substr(0,len-3)	
		var tail = "," + P[i].price.toString().substr(len-3)
		$$("#price-head").html(head)
		$$("#price-tail").html(tail)
		
	}
	function renderProductHeader(){
		$$.each(P, function(i,v){
			var node = $$(T.product_header(v))
			node.on("click",function(){
				swichProduct(i)
			})
			$$(".price-row").append(node)
		})
	}
	renderProductHeader()
	swichProduct(1)
})
