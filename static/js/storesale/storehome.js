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
    "home": "/static/storesale/storehome.html",
    "alipayqr": "/static/storesale/alipayqr.html"
}


app.onPageInit("home", function(page) {
    var mySwiper = app.swiper('.swiper-container', {
        speed: 400,
        spaceBetween: 0,
		pagination:'.swiper-pagination',
		autoplay: 10000
    });
}).trigger()
