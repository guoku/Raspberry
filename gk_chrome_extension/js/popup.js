document.addEventListener('DOMContentLoaded', function () {
	var data = chrome.extension.getBackgroundPage().articleData;
	console.log(data);
	if ( data.status == 1) {
		// console.log("OKOk");
		var entity = data.entity;

		$("#message").hide();
		$("#entity").show();

		$("#entity h4").html(entity.brand + " - "+ entity.title);
		$("#entity em").html("创建：" + entity.created_time);
		$("#entity p").html("价钱：" + entity.price);
		$("<div class='col-xs-offset-2'><a target='_blank' class='btn btn-primary' href='http://guoku.com/detail/" + entity.entity_hash + "/'>查看</a></div>").appendTo($("#entity"));

		var image = $("#image");
		$("<div class='col-xs-12'><img src='" + entity.chief_image.url + "_64x64.jpg'></div>").appendTo(image);
	}

});