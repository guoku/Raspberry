#coding=utf-8
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from base.user import User
from base.taobao_shop import TaobaoShop
def staff_only(func=None):
    def staff_wrapped(request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return func(request, *args, **kwargs)
    return staff_wrapped

def seller_only(func = None):
    def seller_only_decorator(request, *args, **kwargs):
        user_inst = User(request.user.id)
        user_context = user_inst.read()
        shop_nick = user_context.get("shop_nick", None)
        if shop_nick:
            shop_inst = TaobaoShop(shop_nick)
            kwargs['user_context'] = user_context
            kwargs['shop_inst'] = shop_inst
            print func
            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("bind_taobao_shop"))
    return seller_only_decorator
