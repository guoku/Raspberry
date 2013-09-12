# coding=utf-8
from django import template
register = template.Library()


def display_entity_row(entity_context):
    return {
        "entity_context" : entity_context,
    } 
register.inclusion_tag("entity/partial/row.html")(display_entity_row)


def count(value):
    if value == None:
        return 0
    return len(value)
register.filter(count)

