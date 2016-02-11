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
	var current_accordion = undefined

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
			if(v==""){
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

		if(m != undefined){
			curmonth = curmonth.add(m, 'months')
		}
        var month = '<div class="monthview"><div class="content-block-title">' + curmonth.format("MMMM") + '</div>' +
            '<div class="content-block accordion-list custom-accordion o2-book-month">' +
            '##</div>' +
            '</div></div>';
		
		var week = []
		var wd = curmonth.format("d")
		var lastday = curmonth.add(1, 'months').subtract(1,"days").format("D")
		
		for(var i = 0; i < wd; i++){
			week.push("")
		}
	
        var weeks = ""
		for(var i=1; i<= lastday; i++){
			week.push(i)
			if(week.length == 7){
				weeks += buildMonthRow(week)
				week = []
			}
		}
		if(week.length != 0){
			while(week.length != 7) { week.push("")}
			weeks += buildMonthRow(week)
		}

        return month.replace("##", weeks)
    }

    function loadmore() {
        var months = buildMonth();
        months += buildMonth(1);
        months += buildMonth(1);
        $$(".months").append(months)
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
	$$("#o2-book-overlay-top, #o2-book-overlay-bottom").on("click", function(){
		app.accordionClose(current_accordion)
	})
    $$('.accordion-item').on('close', function(e) {
        $$(".o2-book-days .col-auto").removeClass("active")
		$$("#o2-book-overlay-top, #o2-book-overlay-bottom").css("height", 0)
		$$("#o2-book-overlay-top").hide()
		$$(this).find(".o2-book-hours").html("");
    });
    $$('.accordion-item').on('open', function(e) {
        expanding.addClass("active")
		//set overlay
		current_accordion = $$(this)
		var to = 0;
		var actual = $$(".months").offset().top + current_accordion.offset().top
		if(actual> 160){
			to = actual - $$(".page").height() * 0.4
		}
		function cb(){
			$$("#o2-book-overlay-top").css("height", current_accordion.offset().top + 10 + "px")
			$$("#o2-book-overlay-bottom").css("height", $$(".views").height() - current_accordion.offset().top - 350  + "px")
			$$("#o2-book-overlay-top").show()
			current_accordion.find(".o2-book-hours").html(buildDayView());
		    bindHour(current_accordion)
			e.stopPropagation()
		}
		if(to <= 0){
			cb()
		} else {
			$$(".page-content").scrollTop(to,300, cb)
		}
    });
	$$('.accordion-item').on('opened', function(e){	
	});
});

$$("#book-detail").on("click", function() {
    mainView.router.loadPage(pages.bookdetail);
})
