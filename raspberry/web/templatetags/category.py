from django import template

register = template.Library()

def display_category(entity):

    return


def show_category(value):

    title = value.split('-')
    return title[0]

register.filter(show_category)

__author__ = 'edison7500'
