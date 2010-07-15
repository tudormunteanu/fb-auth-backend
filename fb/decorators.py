from functools import update_wrapper
from werkzeug import redirect
from werkzeug.urls import url_quote_plus
from kay.utils import render_to_response, reverse, url_for
from kay.utils import (
    create_auth_url, create_login_url, create_logout_url
)
import logging

from fb.utils import create_facebook_login_url

def fb_required(func):

    def inner(request, *args, **kwargs):
        if request.user.is_anonymous():
            if request.is_xhr:
                return Forbidden()
            else:
                logging.debug("This is the url we are going to.")
                logging.debug(request.url)
                logging.debug("Check it!")
                return redirect(create_facebook_login_url(request.url))
        return func(request, *args, **kwargs)

    update_wrapper(inner, func)
    return inner
