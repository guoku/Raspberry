;(function ($) {
    var url = "/management/entity/categories";
    var groups_and_categories;

    var category_group = $("#category_group");
    var category = $("#category_id");
    var all_categories = [];

    $.post(url, function (data) {
        groups_and_categories = $.parseJSON(data);

        for (var group_title in groups_and_categories) {
            $("<option>" + group_title + "</option>").val(group_title).appendTo(category_group);

            var categories = groups_and_categories[group_title];

            for (var i = 0; i < categories.length; i++) {
                var category_title = categories[i]["category_title"];
                var category_id = categories[i]["category_id"];

                all_categories.push({
                    "title": category_title,
                    "id": category_id
                });

                $("<option >" + category_title + "</option>").val(category_id).appendTo(category);
            }
        }
    });

    category_group.change(function () {
        $("option", category).each(function () {
            $(this).remove();
        });

        var group_title = category_group.val();

        if (group_title === "all") {
            for (var i = 0; i < all_categories.length; i++) {
                $("<option >" + all_categories[i].title + "</option>").val(all_categories[i].id).appendTo(category);
            }

        } else {
            var categories = groups_and_categories[group_title];

            for (var j = 0; j < categories.length; j++) {
                var category_title = categories[j]["category_title"];
                var category_id = categories[j]["category_id"];

                $("<option >" + category_title + "</option>").val(category_id).appendTo(category);
            }
        }
    });

})(jQuery);