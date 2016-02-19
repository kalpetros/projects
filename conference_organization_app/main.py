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

class SpeakerCheck(webapp2.RequestHandler):
    def post(self):
        """When a new session is added to a conference, check the speaker."""
        c_key = ndb.Key(urlsafe=self.request.get('c_key_str'))
        # Get conference's sessions
        conf_sess = Session.query(ancestor=c_key)
        # Get speakers
        speakers = Speaker.query()
        # Sort speakers by name
        speakers = speakers.order(Speaker.name)
        featured_speakers = []
        for speaker in speakers:
            count = 0
            # Check how many times a speaker speaks (at a conference)
            for session in conf_sess:
                for speaker_key in session.speakers:
                    if speaker.key == speaker_key:
                        count += 1
                        # Feature a speaker (>2 sessions)
                        if count == 2:
                            featured_speakers.append(speaker_key)
        MEMCACHE_CONFERENCE_KEY = "FEATURED:%s" % c_key.urlsafe()
        # Set featured speakers announcement in memcache
        if featured_speakers:
            count = 0
            featured = "Featured speakers: "
            for speakr_key in featured_speakers:
                count += 1
                featured += " FEATURED %s: %s SESSIONS: " % (
                    count, speakr_key.get().name)
                sessionsOfFeatured = conf_sess.filter(
                    Session.speakers == speakr_key)
                featured += ", ".join(sess.name for sess in sessionsOfFeatured)
            memcache.set(MEMCACHE_CONFERENCE_KEY, featured)
        else:
            # Delete the memcache entry (if there are no featured speakers)
            featured = ""
            memcache.delete(MEMCACHE_CONFERENCE_KEY)

app = webapp2.WSGIApplication([
    ('/crons/set_announcement', SetAnnouncementHandler),
    ('/tasks/send_confirmation_email', SendConfirmationEmailHandler),
    ('/tasks/check_speaker', SpeakerCheck)
], debug=True)
