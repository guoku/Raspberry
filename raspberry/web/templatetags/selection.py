# coding=utf-8
from django import template

register = template.Library()


def display_selections(selection_list):
    return {
        'selection_list' : selection_list
    }

register.inclusion_tag("main/partial/selection_item_list.html")(display_selections)