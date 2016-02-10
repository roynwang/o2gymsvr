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

    function bindHour(tar) {
        function prepareSubmit(ele) {
            var btnp = $$('<p class="animated slideInRight" style="display:none"><span class="o2-book-submit">预约</span></p>')
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
            rows += row.replace("##", v);
        })
        return container.replace("##", rows)
    }

    function buildMonth() {
        var month = '<div class="monthview"><div class="content-block-title"><h2 style="margin:0px">十月</h2></div>' +
            '<div class="content-block accordion-list custom-accordion o2-book-month">' +
            '##</div>' +
            '</div></div>';
        var days = [1, 2, 3, 4, 5, 6, 7]
        var weeks = ""
        for (var i = 0; i < 4; i++) {
            weeks += buildMonthRow(days)
        }
        return month.replace("##", weeks)
    }

    function loadmore() {
        var months = buildMonth();
        months += buildMonth();
        months += buildMonth();
        $$(".infinite-scroll .months").append(months)
    }

	function buildDayView() {
		var rows = '<div class="list-block"><ul>##</ul></div>'
		var hour = '<li class="item-content">'+
                    	'<div class="item-media"><span class="hour">##</span><span class="min">00</span></div>' + 
                       	 '<div class="item-inner"><div class="item-title"></div></div>' +
                    '</li>' ;
		var hourhalf = '<li class="item-content">'+
                    	'<div class="item-media"><span class="hour hide"></span><span class="min">30</span></div>' + 
                       	 '<div class="item-inner"><div class="item-title"></div></div>' +
                    '</li>';
		var alltext = ""
		for(var i = 0; i < TimeMap.length; i++){
			if(i%2 == 0){
				alltext += hour.replace("##", 9 + i/2)
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
    $$('.accordion-item').on('close', function(e) {
        $$(".o2-book-days .col-auto").removeClass("active")
    });
    $$('.accordion-item').on('open', function(e) {
        expanding.addClass("active")
		$$(this).find(".o2-book-hours").html(buildDayView());
	    bindHour($$(this))
    });
    $$('.infinite-scroll').on('infinite', function() {
        // Exit, if loading in progress
        if (loading) return;
        // Set loading flag
        loading = true;
        // Emulate 1s loading
        // Reset loading flag
        loading = false;
        if (lastIndex >= maxItems) {
            // Nothing more to load, detach infinite scroll events to prevent unnecessary loadings
            app.detachInfiniteScroll($$('.infinite-scroll'));
            // Remove preloader
            $$('.infinite-scroll-preloader').remove();
            return;
        }
        // Generate new items HTML

        // Append new items
        //$$('.list-block ul').append(html);
        loadmore()

        // Update last loaded index
        lastIndex = $$('.list-block .monthview').length;
    });
});

$$("#book-detail").on("click", function() {
    mainView.router.loadPage(pages.bookdetail);
})
