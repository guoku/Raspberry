# coding=utf8
from base.category import Category
from mobile.lib.http import SuccessJsonResponse, ErrorJsonResponse

def all_category(request):
    _all_categories = Category.all_group_with_full_category()
    return SuccessJsonResponse(_all_categories)

