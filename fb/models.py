# -*- coding: utf-8 -*-
# fb.models
from datetime import datetime
from google.appengine.ext import db

from userprofile.models import UserProfile


class FacebookProfile(db.Model):
    fb_uid = db.StringProperty(required = True)
    first_name = db.StringProperty()
    userprofile = db.ReferenceProperty(UserProfile)

    @classmethod
    def get_user_by_fbuid(self, fb_uid):
        """
        Return a Userprofile based on an Facebook ID
        If there is no Userprofile associated with this Facebook ID,
        create a new one.
        """
        facebook_profiles = self.all().filter('fb_uid =', fb_uid).fetch(100)
        if len(facebook_profiles):
            return facebook_profiles[0].userprofile.user
        else:
            return _create_fb_user(fb_uid)

def _create_fb_user(fb_uid):
    from kay.auth.models import DatastoreUser
    user = DatastoreUser(email = '%s@facebook.profile.com' % fb_uid, 
                         user_name = 'facebook_user_%s' % fb_uid,
                         password = '123',
                         key_name = 'u:' + str(fb_uid))
    user.put()
    #facebook_data = get_facebook_data_for_uid(fb_uid)
    # TODO: Use OAuth2 to retrieve userprofile values from fb
    userprofile = UserProfile(location = '',
                              bio = '',
                              website = '',
                              user = user)
    userprofile.put()
    facebook_profile = FacebookProfile(fb_uid = fb_uid, userprofile = userprofile) 
    facebook_profile.put()
    return user

