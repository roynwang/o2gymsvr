$(function(){
	$("#btn-login").click(function(){
		var usrname = $("#phone").val()
		var pwd = $("#pwd").val()
		//validate the user
		$.post("/api/lg/",{username:usrname, password:pwd}, function(data,status){
			$.cookie("token",data.token)
			$("#login-error").html("登录成功,2秒后跳转")
			setTimeout(function(){
			  window.location = "/console/dashboard/"
			}, 2000)
			//$("#login-error").html(data.token)
		}).fail(function(resp){
			if(resp.status == 403){
				$("#login-error").html("错误的电话号码或密码")
			}
		})
	})
})
