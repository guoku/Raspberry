$(function(){
	$(".form_container input[name='password'],.form_container input[name='email']").on("keyup",function(){
		if($(".form_container input[name='password']").val()!="" && $.trim($(".form_container input[name='email']").val())!=""){
			$(".form_container input[type='submit']").removeAttr("disabled").removeClass("submit_disabled").addClass("submit");
		}else{
			$(".form_container input[type='submit']").attr("disabled",true).removeClass("submit").addClass("submit_disabled");
		}
	});
});