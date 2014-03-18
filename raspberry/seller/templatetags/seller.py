#coding=utf-8
from django import template
register = template.Library()

def display_shop_verification(shop_context, verification_form, shop_verification):
    return {
        "shop_context" : shop_context,
        "verification_form" : verification_form,
        "shop_verification" : shop_verification
    }
register.inclusion_tag("partial/shop_verification.html")(display_shop_verification)
