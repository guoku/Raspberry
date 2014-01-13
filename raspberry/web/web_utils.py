from django.conf import settings

def get_login_redirect_url(request):
    next_url = get_redirect_url(request)
    if next_url:
        return next_url
    return settings.LOGIN_REDIRECT_URL

def get_redirect_url(request):
    next_url = request.REQUEST.get("next", None)
    return next_url

def parse_taobao_id_from_url(url):
    params = url.split("?")[1]
    for param in params.split("&"):
        tokens = param.split("=")
        if len(tokens) >= 2 and (tokens[0] == "id" or tokens[0] == "item_id"):
            return tokens[1]
    return None
