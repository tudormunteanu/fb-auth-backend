from kay.ext.testutils.gae_test_base import GAETestBase
from werkzeug import BaseResponse, Client, Request
from kay.app import get_application
from kay.utils.test import (
  init_recording, get_last_context, get_last_template, disable_recording,
)
from kay.auth.models import DatastoreUser
import settings

from userprofile.tests import _user_creation
from userprofile.models import UserProfile
from fb.models import FacebookProfile, _create_fb_user
from utils import update_facebook_user

FACEBOOK_UID = '676578004'
COOKIE_NAME = 'fbs_%s' % settings.FACEBOOK_APP_ID
COOKIE_VALUE = 'access_token=106736729377441%7C2.OYzpDwMUzyq6LHGjyUwz1g__.3600.1278068400-676578004%7Cg2qDiJu-5oEenufauY1DX0uYYTE.&expires=1278068400&secret=QCOWrDntYehFbXijcfkPqA__&session_key=2.OYzpDwMUzyq6LHGjyUwz1g__.3600.1278068400-676578004&sig=ab71e438bbfd759468c2c59a3dfb2271&uid=' + FACEBOOK_UID


class FbTest(GAETestBase):

    def setUp(self):
        init_recording()
        app = get_application()
        self.client = Client(app, BaseResponse)

    def test_facebook_cookie_parsing(self):
        from fb.utils import get_facebook_uid_from_cookie
        cookies = {COOKIE_NAME: COOKIE_VALUE, 
                  '__qca': u'P0-1132520767-1274949618785'}
        fb_cookie = cookies[COOKIE_NAME] 
        self.assertEquals(get_facebook_uid_from_cookie(fb_cookie), '676578004')

    def test_facebook_profile_creation(self, fbuid = '123'):
        from werkzeug.utils import import_string
        dudes_profile = _user_creation(self)
        dudes_facebook = FacebookProfile(fb_uid = fbuid, userprofile = dudes_profile)
        dudes_facebook.put()
        auth_model_class = import_string(settings.AUTH_USER_MODEL)
        user = auth_model_class.get_user_by_fbuid(fbuid)
        self.assertEquals(dudes_facebook.userprofile.user.key(), user.key())

    def test_facebook_login_url(self):
        self.test_facebook_profile_creation(fbuid = FACEBOOK_UID)
        response = self.client.get('/facebook/login/')
        self.assertEquals(response.status_code, 404)
        resp = self.client.get('/facebook/set_test_session/')
        response = self.client.get('/facebook/login/')
        self.assertEquals(response.status_code, 302)

    def test_facebook_first_visit(self):
        profiles = UserProfile.all().fetch(100)
        self.assertEquals(len(profiles), 0)
        fb_profiles = FacebookProfile.all().fetch(100)
        self.assertEquals(len(fb_profiles), 0)
        users = DatastoreUser.all().fetch(100)
        self.assertEquals(len(users), 0)
        _facebook_login(self)

        fb_profiles = FacebookProfile.all().fetch(100)
        self.assertEquals(len(fb_profiles), 1)
        profiles = UserProfile.all().fetch(100)
        self.assertEquals(len(profiles), 1)
        users = DatastoreUser.all().fetch(100)
        self.assertEquals(len(users), 1)

    def test_facebook_return_visit(self):

        _create_fb_user(FACEBOOK_UID)

        profiles = UserProfile.all().fetch(100)
        self.assertEquals(len(profiles), 1)
        fb_profiles = FacebookProfile.all().fetch(100)
        self.assertEquals(len(fb_profiles), 1)
        users = DatastoreUser.all().fetch(100)
        self.assertEquals(len(users), 1)
        _facebook_login(self)

        fb_profiles = FacebookProfile.all().fetch(100)
        self.assertEquals(len(fb_profiles), 1)
        profiles = UserProfile.all().fetch(100)
        self.assertEquals(len(profiles), 1)
        users = DatastoreUser.all().fetch(100)
        self.assertEquals(len(users), 1)

    #def test_graph_authorization(self):
        #resp = self.client.get('/facebook/test_graph_api/')
        #self.assertEquals(resp.status_code, 302)

    def test_update_facebook_user(self):
        _create_fb_user(FACEBOOK_UID)
        facebook_data = dict(first_name = 'Mos', last_name = "Def")
        user = DatastoreUser.all().fetch(100)[0]
        self.assertTrue(user.user_name.find(FACEBOOK_UID) > -1)
        user = update_facebook_user(user = user, 
                             facebook_user_data = facebook_data)
        self.assertTrue(user.first_name == "Mos")

    def test_fb_login_decorator(self):
        _create_fb_user(FACEBOOK_UID)
        resp = self.client.get('/projects/new/')
        # fb user is not logged in and attempts to access this url. redirection expected, hence 302.
        self.assertEquals(resp.status_code, 302)
        # fb user is logged in and now should be able to access the url.
        _facebook_login(self)
        resp = self.client.get('/projects/new/')
        self.assertEquals(resp.status_code, 200)

    def test_fb_login_decorator_again(self):
        # fb user is not logged in and goes to /facebook/fb_login page.
        pass


def _facebook_login(self):
    resp = self.client.get('/facebook/set_test_session/')
    resp = self.client.get('/facebook/login/')
    self.assertEquals(resp.status_code, 302)
        



