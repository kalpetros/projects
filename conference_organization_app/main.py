#!/usr/bin/env python

"""
main.py -- Udacity conference server-side Python App Engine
    HTTP controller handlers for memcache & task queue access

$Id$

created by wesc on 2014 may 24
updated by Petros Kalogiannakis on 2016 feb 02
"""

__author__ = 'Wesley Chun, Petros Kalogiannakis'

import webapp2
from google.appengine.api import app_identity
from google.appengine.api import mail
from google.appengine.ext import ndb
from google.appengine.api import memcache
from conference import ConferenceApi
from models import Session
from models import Speaker

class SetAnnouncementHandler(webapp2.RequestHandler):
    def get(self):
        """Set Announcement in Memcache."""
        ConferenceApi._cacheAnnouncement()
        self.response.set_status(204)

class SendConfirmationEmailHandler(webapp2.RequestHandler):
    def post(self):
        """Send email confirming Conference creation."""
        mail.send_mail(
            'noreply@%s.appspotmail.com' % (
                app_identity.get_application_id()),     # from
            self.request.get('email'),                  # to
            'You created a new Conference!',            # subj
            'Hi, you have created a following '         # body
            'conference:\r\n\r\n%s' % self.request.get(
                'conferenceInfo')
        )

class SetFeaturedSpeakerHandler(webapp2.RequestHandler):
    def post(self):
        """Set featured speaker in Memcache."""
        ConferenceApi._cacheFeaturedSpeaker(self.request.get('websafeConferenceKey'))
        self.response.set_status(204)

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/featured_speaker', SetFeaturedSpeakerHandler)
], debug=True)
