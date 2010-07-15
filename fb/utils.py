from kay.utils import create_auth_url

def get_facebook_uid_from_cookie(cookie):
    """
    return the Facebook User ID from the cookie string
    """
    from cgi import parse_qs
    uids = parse_qs(cookie)['uid']
    if len(uids):
        return uids[0]
    return None

def get_facebook_uid(request):
    """
    return the Facebook UID from the request object
    """
    import settings
    cookie_key = 'fbs_%s' % settings.FACEBOOK_APP_ID
    if request.cookies.has_key(cookie_key):
        fbuid = get_facebook_uid_from_cookie(request.cookies[cookie_key])
    # TODO: find out why sessions dissappear on cookie changes
    # it's like this to run tests
    elif request.session.has_key(cookie_key):
        fbuid = get_facebook_uid_from_cookie(request.session[cookie_key])
    else:
        fbuid = None
    return fbuid

def create_facebook_login_url(url=None, **kwargs):
    """
    Get the URL for a facebook login page
    """
    return create_auth_url(url, 'facebook_login', **kwargs)

def update_facebook_user(user = None,  facebook_user_data = None):
    """
    Update the User's profile info based on the data
    returned from Facebook.
    Be careful to check if Facebook really returns what
    you expect.
    """
    if not user or not facebook_user_data:
        return 
    if facebook_user_data.has_key('first_name'):
        user.first_name = facebook_user_data['first_name']
    if facebook_user_data.has_key('last_name'):
        user.last_name = facebook_user_data['last_name']
    user.put() 
    return user

def posturl(url, fields, files):
    import urlparse
    urlparts = urlparse.urlsplit(url)
    logging.debug(urlparts[1])
    logging.debug(urlparts[2])
    return post_multipart(urlparts[1], urlparts[2], fields,files)

def post_multipart(host, selector, fields, files):
    """
    Post fields and files to an http host as multipart/form-data.
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return the server's response page.
    """
    import httplib
    content_type, body = encode_multipart_formdata(fields, files)
    h = httplib.HTTPS(host)
    h.putrequest('POST', selector)
    h.putheader('content-type', content_type)
    h.putheader('content-length', str(len(body)))
    h.endheaders()
    h.send(body)
    errcode, errmsg, headers = h.getreply()
    return h.file.read()

def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    listy = []
    for element in L:
        try:
            listy.append(element.decode('string_escape'))
        except:
            listy.append(element)
    body = CRLF.join(listy)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    import mimetypes
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'
