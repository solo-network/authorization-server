from django.http import HttpResponseForbidden

def allow_specific_origin(view_func):
    def wrapper(request, *args, **kwargs):
        allowed_origin = "https://celepar-knowbe4-connector.scm.azurewebsites.net"
        origin = request.META.get('HTTP_ORIGIN') or request.META.get('HTTP_REFERER')
        if origin and origin.startswith(allowed_origin):
            return view_func(request, *args, **kwargs)
        return HttpResponseForbidden('Unauthorized origin')
    return wrapper
