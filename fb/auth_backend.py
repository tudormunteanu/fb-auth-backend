import settings

from werkzeug.urls import url_quote_plus
from werkzeug.utils import import_string
from kay.utils import (
  local, url_for
)
from kay.auth.backends.datastore import DatastoreBackend

from models import FacebookProfile

class FacebookBackend(DatastoreBackend):

    def login(self, request, fb_uid):
        auth_model_class = import_string(settings.AUTH_USER_MODEL)
        user = auth_model_class.get_user_by_fbuid(fb_uid)
        if user is None:
            return False
        self.store_user(user)
        return True


    def create_facebook_login_url(self, url):
        return url_for("fb/fb_login", next=url_quote_plus(url))


