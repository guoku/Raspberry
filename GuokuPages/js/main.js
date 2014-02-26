	$(function(){
		$(".activity_item>ul").on("click",function(){
			$(this).parents(".activity_item").toggleClass("recent_selected");
			$(this).next(".activity_detail").toggle(200);
		});
	});