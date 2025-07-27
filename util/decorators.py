from functools import wraps
from flask import redirect,url_for,g,abort

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if not hasattr(g,"user"):
            return redirect(url_for("user.login"))
        else:
            return func(*args,**kwargs)
    return inner

def permission_required(permission):
    def outer(func):
        @wraps(func)
        def inner(*args,**kwargs):
            if hasattr(g,"user") and g.user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return abort(403)
        return inner
    return outer