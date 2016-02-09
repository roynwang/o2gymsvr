var app = new Framework7({
	template7Pages: true,
	template7Data: {}
});
var $$ = Dom7;
var mainView = app.addView('.view-main');

var pages = {
	"bookdetail": "/static/customermobile/book.html"
}


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

app.onPageInit('about', function (page) {
	//bind hours click
	var busy = false
	var busycount = "·"

	function bindHour(){
		function prepareSubmit(ele){
			var btnp = $$('<p class="animated slideInRight"><span class="o2-book-submit">预约</span></p>')
			$$(ele).prepend(btnp)
			function submit(){
				if(busy) return;
				var btn = $$(this)
				btn.html(busycount)
				busy = setInterval(function(){
					if(busy){
						if(busycount.length == 5){
							busycount = ""
						}
						busycount += "·"
						btn.html(busycount)
					} else {
						btn.html("")
						btn.addClass("ion-ios-checkmark-empty")
						btn.addClass("animated o2-pulse")
						btn.css("font-size","60px")
						window.clearInterval(busy)
						btn.off("click", submit)
					}
				},300)
				busy=true;
				btnp.removeClass("animated slideInRight")
				setTimeout(function(){ busy = false}, 2000);
			}

			btnp.find(".o2-book-submit").on("click", submit)
		}
		function cleanSubmit(){
			$$(".o2-book-hours ul li.booking>p").remove()
			$$(".o2-book-hours ul li.booking").toggleClass("booking")
		}
		$$(".o2-book-hours ul li").on("click", function(event){
			if(busy || $$(this).hasClass("booking")) return;
			cleanSubmit()
			$$(this).addClass("booking")
			prepareSubmit($$(this))
		})
	}

	bindHour()


	var expanding = undefined
	$$(".back").on("click", function(){
		mainView.router.back();
	})
	$$(".o2-book-days .col-auto").on("click", function(){
			expanding = $$(this)
	})
	$$('.accordion-item').on('close', function (e) {
		$$(".o2-book-days .col-auto").removeClass("active")
	});                   
	$$('.accordion-item').on('open', function (e) {
		expanding.addClass("active")
	});                   
	console.log('One more callback for About page');
	console.log(page);
});

$$("#book-detail").on("click", function(){
	mainView.router.loadPage(pages.bookdetail);
})
