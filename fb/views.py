# -*- coding: utf-8 -*-
"""
fb.views
"""

"""
import logging

from google.appengine.api import users
from google.appengine.api import memcache
from werkzeug import (
  unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)

from kay.utils import (
  render_to_response, reverse,
  get_by_key_name_or_404, get_by_id_or_404,
  to_utc, to_local_timezone, url_for, raise_on_dev
)
from kay.i18n import gettext as _
from kay.auth.decorators import login_required

"""

from kay.utils import render_to_response
from werkzeug import (
    unescape, redirect, Response,
)
from werkzeug.exceptions import (
  NotFound, MethodNotAllowed, BadRequest
)
import logging

from google.appengine.api.urlfetch import DownloadError 
    
from fb.utils import get_facebook_uid, update_facebook_user

def index(request):
    return render_to_response('fb/index.html', {'message': 'Hello'})

def login(request):
    from kay.auth import login
    from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET
    import facebook
    fb_uid = get_facebook_uid(request)
    if not fb_uid:
        return NotFound()
    result = login(request, fb_uid = fb_uid)
    auth = facebook.get_user_from_cookie(request.cookies, FACEBOOK_APP_ID, FACEBOOK_SECRET)
    if auth:
        access_token = auth['access_token']
        graph = facebook.GraphAPI(access_token)
        try:
            user = graph.get_object("me")
            logging.debug(user)
        except DownloadError:
            user = None
            logging.debug(access_token)
            logging.debug(graph)
            logging.debug(auth)
            logging.debug(fb_uid)
            logging.debug("some strange error occurred on app engine")
        if user:
            update_facebook_user(user = request.user, facebook_user_data = user)

    return redirect(request.referrer)

def fb_login(request):
    fb_uid = get_facebook_uid(request)
    if not fb_uid:
        return render_to_response('fb/fb_login.html', {})
    else:
        return redirect('/projects/new/')

def set_test_session(request):
    """
    for testing purposes only
    """
    from tests import COOKIE_VALUE, COOKIE_NAME
    request.session[COOKIE_NAME] = COOKIE_VALUE
    return redirect('/')

def test_graph_api(request):
    from settings import FACEBOOK_APP_ID, FACEBOOK_SECRET
    import cgi, urllib, urllib2
    import simplejson as json
    from tests import FACEBOOK_UID
    import facebook
    import utils
    auth = facebook.get_user_from_cookie(request.cookies, FACEBOOK_APP_ID, FACEBOOK_SECRET)
    access_token = auth['access_token']
    #graph = facebook.GraphAPI(access_token)
    #user = graph.get_object("me")
    #logging.debug(user)
    #logging.debug(access_token)
    #graph.put_object("me", 'photos', image = urllib.urlopen('http://www.8squirrels.com/media/images/img1.jpg').read())
    #params = urllib.urlencode({'file': urllib.urlopen('http://www.8squirrels.com/media/images/img1.jpg').read()})
    #datagen, headers = multipart_encode(params)
    #request = urllib2.Request("https://graph.facebook.com/me/photos", params)
    #resp = urllib.urlopen('https://graph.facebook.com/me/photos', params)
    #logging.debug(request)
    #logging.debug(dir(request))
    #logging.debug(request.headers)
    #image_content = urllib.urlopen('http://www.8squirrels.com/media/images/img1.jpg').read()
    if request.method == "POST":
        out = utils.posturl('https://graph.facebook.com/me/photos', [('access_token', request.form['access_token'])], 
                      [('myfile', 'myimage.jpg', request.files['file'].stream.read())])

    post_url = "https://graph.facebook.com/me/photos"
    return render_to_response('fb/index.html', {'post_url': post_url, 'access_token': access_token})



