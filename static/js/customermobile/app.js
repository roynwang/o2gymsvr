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
