from django.views.defaults import server_error
from django.views.defaults import page_not_found
# from django.shortcuts import render_to_response
from django.views.generic import TemplateView

def page_error(request):
    return server_error(request, template_name='500.html')

def webpage_not_found(request):
    return page_not_found(request, template_name='404.html')


class AboutView(TemplateView):
    template_name = "about.html"
