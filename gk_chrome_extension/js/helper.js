var gk_host = "http://test.guoku.com/";
var gk_read_state_url = gk_host + "management/entity/item/taobao/state";
var location_href = location.href;


if (/id|item_id/ig.test(location_href)) {
    var options = {
        url: gk_read_state_url + "?url=" + encodeURIComponent(location_href)
    };
    console.log(options.url);
    $.ajax({
        url:options.url,
        type: "get",
        success: function (data) {
            // console.log(data);
            var obj = $.parseJSON(data);
            chrome.runtime.sendMessage(obj);
        },
        error: function (data) {
            console.log(data);
        }
    })
}
// chrome.runtime.sendMessage(location_href); 