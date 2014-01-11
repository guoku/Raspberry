//var gk_host = "http://10.0.1.148:8000/";
var gk_host = "http://114.113.154.47:8000/";

var gk_add_url = gk_host + "management/entity/new/";
var gk_read_state_url = gk_host + "management/entity/item/taobao/state";

var location_href = location.href;

if (/id|item_id/ig.test(location_href)) {
    var options = {
        url: gk_read_state_url + "?url=" + encodeURIComponent(location_href)
    };

    http_request(options, function (err, data) {
        if (!err) {
            var body = document.body;
            init_ui(body, JSON.parse(data));
        } else {
            console.log("Error: " + JSON.stringify(err));
        }
    });
}


function init_ui(body, data) {
    var gk_helper_box = document.createElement("div");
    gk_helper_box.id = "gk-help-box";

    var gk_header = document.createElement("div");
    gk_header.className = "gk-header";
    gk_header.innerHTML = '<img src="http://static.guoku.com/static/images/guoku_icon_32.png" alt="guoku">';
    gk_helper_box.appendChild(gk_header);

    var gk_content = document.createElement("div");
    gk_content.className = "gk-content";

    var data_status = Number(data.status);
    var gk_form;

    if (data_status === 1) {
        var entity = data.entity;
        gk_content.innerHTML = "<a target='_blank' href='" + "http://www.guoku.com/detail/" + entity.entity_hash + "'>" + entity.title + "</a>" +
            "<div>" +
            "<span>" + "品牌:" + entity.brand + "</span>" +
            "<span>" + " 价格:" + Number(entity.price).toFixed(2) + "</span>" +
            "<span>" + " 点评数:" + entity.note_count + "</span>" +
            "</div>";

        gk_form = create_form({
            text: "管理",
            action: gk_host + "management/entity/" + entity.entity_id + "/edit/"
        });

    } else if (data_status === -1) {
        gk_content.innerText = "此商品已经入库，但尚未添加到具体Entity";

    } else {
        gk_content.innerText = "此商品未添加";
        gk_form = create_form({
            text: "添加",
            action: gk_add_url,
            method: "POST",
            data: {
                name: "url",
                value: location_href
            }
        });

        var alimama = document.createElement('a');
        alimama.appendChild(document.createTextNode(' 查看佣金'));
        alimama.href =  'http://pub.alimama.com/index.htm#!/promo/self/items?q=' + encodeURIComponent(location_href);
        gk_content.appendChild(alimama);
    }

    gk_helper_box.appendChild(gk_content);
    if (gk_form) {
        gk_helper_box.appendChild(gk_form);
    }

    body.appendChild(gk_helper_box);
}

function create_form(options) {
    var form = document.createElement("form");
    form.action = options.action;
    form.method = options.method || "GET";
    form.target = "_blank";

    if (options.data) {
        var input = document.createElement("input");
        input.type = "text";
        input.hidden = "hidden";
        input.name = options.data.name;
        input.value = options.data.value;

        form.appendChild(input);
    }

    var submit = document.createElement("input");
    submit.type = "submit";
    submit.value = options.text;
    submit.className = "gk-button";

    form.appendChild(submit);
    return form;
}


function http_request(options, callback) {
    var url = options.url;
    var method = options.method || "GET";
    var async = options.async || true;
    var data = options.data || null;

    var xhr = new XMLHttpRequest();
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            if (xhr.status >= 200 && xhr.status < 300 || xhr.status == 304) {
                callback(null, xhr.responseText);
            } else {
                callback({ status: xhr.status, statusText: xhr.statusText });
            }
        }
    };
    xhr.open(method, url, async);
    xhr.send(data);
}