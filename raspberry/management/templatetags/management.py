# coding=utf-8
from django import template
register = template.Library()


def display_candidate_row(candidate_context):
    return {
        "candidate_context" : candidate_context,
    } 
register.inclusion_tag("candidate/partial/row.html")(display_candidate_row)

def display_entity_row(entity_context):
    return {
        "entity_context" : entity_context,
    } 
register.inclusion_tag("entity/partial/row.html")(display_entity_row)

def display_category_row(category_context):
    return {
        "category_context" : category_context,
    } 
register.inclusion_tag("category/partial/row.html")(display_category_row)


def count(value):
    if value == None:
        return 0
    return len(value)
register.filter(count)

