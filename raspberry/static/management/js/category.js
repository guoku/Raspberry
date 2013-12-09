;
(function ($) {
    var url = "/management/entity/categories";
    var groups_and_categories;
    var category_group = $("#category_group");
    var category = $("#category_id");

    // initial groups and categories
    $.post(url, function (data) {
        groups_and_categories = $.parseJSON(data);
        var init_category = category.attr("data-init");
        var init_group;
        var group_titles = [];

        for (var title in groups_and_categories) {
            group_titles.push(title);

            var categories = groups_and_categories[title];
            for (var i = 0; i < categories.length; i++) {
                if (categories[i]["category_id"] == init_category) {
                    init_group = title;
                }
            }
        }
        group_titles.sort();

        for (var j = 0; j < group_titles.length; j++) {
            var group_title = group_titles[j];

            var group_option = $("<option>" + group_title + "</option>");
            group_option.val(group_title).appendTo(category_group);
            
            if (group_title == init_group) {
                group_option.attr("selected", "selected");
            }
        }

        var categories = groups_and_categories[init_group];
        for (var i = 0; i < categories.length; i++) {
            var category_title = categories[i]["category_title"];
            var category_id = categories[i]["category_id"];

            var cat_option = $("<option >" + category_title + "</option>");
            cat_option.val(category_id).appendTo(category);

            if (init_category == category_id) {
                cat_option.attr("selected", "selected");
            }
        }
    });

    category_group.change(function () {
        $("option", category).each(function () {
            $(this).remove();
        });

        var group_title = category_group.val();
        var categories = groups_and_categories[group_title];

        for (var j = 0; j < categories.length; j++) {
            var category_title = categories[j]["category_title"];
            var category_id = categories[j]["category_id"];

            $("<option >" + category_title + "</option>").val(category_id).appendTo(category);
        }
    });

})(jQuery);