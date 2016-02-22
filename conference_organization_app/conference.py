#!/usr/bin/env python

"""
conference.py -- Udacity conference server-side Python App Engine API;
    uses Google Cloud Endpoints

$Id: conference.py,v 1.25 2014/05/24 23:42:19 wesc Exp wesc $

created by wesc on 2014 apr 21
updated by Petros Kalogiannakis on 2016 feb 02
"""

__author__ = 'Wesley Chun, Petros Kalogiannakis'

from datetime import datetime

import endpoints
from protorpc import messages
from protorpc import message_types
from protorpc import remote

from google.appengine.api import memcache
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

from models import ConflictException
from models import Profile
from models import ProfileMiniForm
from models import ProfileForm
from models import StringMessage
from models import BooleanMessage
from models import Conference
from models import ConferenceForm
from models import ConferenceForms
from models import ConferenceQueryForm
from models import ConferenceQueryForms
from models import Session
from models import SessionForm
from models import SessionForms
from models import Speaker
from models import SpeakerForm
from models import SessionType
from models import TeeShirtSize

from settings import WEB_CLIENT_ID
from settings import ANDROID_CLIENT_ID
from settings import IOS_CLIENT_ID
from settings import ANDROID_AUDIENCE

from utils import getUserId

EMAIL_SCOPE = endpoints.EMAIL_SCOPE
API_EXPLORER_CLIENT_ID = endpoints.API_EXPLORER_CLIENT_ID
MEMCACHE_ANNOUNCEMENTS_KEY = "RECENT_ANNOUNCEMENTS"
ANNOUNCEMENT_TPL = ('Last chance to attend! The following conferences '
                    'are nearly sold out: %s')

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

DEFAULTS = {
    "city": "Default City",
    "maxAttendees": 0,
    "seatsAvailable": 0,
    "topics": [ "Default", "Topic" ],
}

DEFAULTS_SESSION = {
    "highlights": ["Default", "Highlight"],
    "typeOfSession": SessionType("Lecture"),
    "date": "2016-01-01",
    "duration": "00:00",
    "startTime": "18:00"
}

OPERATORS = {
            'EQ':   '=',
            'GT':   '>',
            'GTEQ': '>=',
            'LT':   '<',
            'LTEQ': '<=',
            'NE':   '!='
            }

FIELDS =    {
            'CITY': 'city',
            'TOPIC': 'topics',
            'MONTH': 'month',
            'MAX_ATTENDEES': 'maxAttendees',
            }

CONF_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeConferenceKey=messages.StringField(1),
)

CONF_POST_REQUEST = endpoints.ResourceContainer(
    ConferenceForm,
    websafeConferenceKey=messages.StringField(1),
)

SESSION_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeConferenceKey=messages.StringField(1),
)

SESSION_BY_TYPE_GET_REQUEST = endpoints.ResourceContainer(
    typeOfSession=messages.EnumField(SessionType, 1),
    websafeConferenceKey=messages.StringField(2),
)

SESSION_POST_REQUEST = endpoints.ResourceContainer(
    SessionForm,
    websafeConferenceKey=messages.StringField(1),
)

WISHLIST_GET_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeConferenceKey=messages.StringField(1)
)

WISHLIST_POST_REQUEST = endpoints.ResourceContainer(
    message_types.VoidMessage,
    websafeSessionKey=messages.StringField(1)
)

SESSION_BY_SPK_GET_REQUEST = endpoints.ResourceContainer(
    SpeakerForm,
    websafeConferenceKey=messages.StringField(1)
)

CONF_BY_CITY_REQUEST = endpoints.ResourceContainer(
    city=messages.StringField(1)
)

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

@endpoints.api(name='conference', version='v1', audiences=[ANDROID_AUDIENCE],
    allowed_client_ids=[WEB_CLIENT_ID, API_EXPLORER_CLIENT_ID, ANDROID_CLIENT_ID, IOS_CLIENT_ID],
    scopes=[EMAIL_SCOPE])
class ConferenceApi(remote.Service):
    """Conference API v0.5"""

# - - - Conference objects - - - - - - - - - - - - - - - - -

    def _copyConferenceToForm(self, conf, displayName):
        """Copy relevant fields from Conference to ConferenceForm."""
        cf = ConferenceForm()
        for field in cf.all_fields():
            if hasattr(conf, field.name):
                # convert Date to date string; just copy others
                if field.name.endswith('Date'):
                    setattr(cf, field.name, str(getattr(conf, field.name)))
                else:
                    setattr(cf, field.name, getattr(conf, field.name))
            elif field.name == "websafeKey":
                setattr(cf, field.name, conf.key.urlsafe())
        if displayName:
            setattr(cf, 'organizerDisplayName', displayName)
        cf.check_initialized()
        return cf

    def _createConferenceObject(self, request):
        """Create or update Conference object, returning ConferenceForm/request."""
        # preload necessary data items
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        if not request.name:
            raise endpoints.BadRequestException("Conference 'name' field required")

        # copy ConferenceForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}
        del data['websafeKey']
        del data['organizerDisplayName']

        # add default values for those missing (both data model & outbound Message)
        for df in DEFAULTS:
            if data[df] in (None, []):
                data[df] = DEFAULTS[df]
                setattr(request, df, DEFAULTS[df])

        # convert dates from strings to Date objects; set month based on start_date
        if data['startDate']:
            data['startDate'] = datetime.strptime(data['startDate'][:10], "%Y-%m-%d").date()
            data['month'] = data['startDate'].month
        else:
            data['month'] = 0
        if data['endDate']:
            data['endDate'] = datetime.strptime(data['endDate'][:10], "%Y-%m-%d").date()

        # set seatsAvailable to be same as maxAttendees on creation
        if data["maxAttendees"] > 0:
            data["seatsAvailable"] = data["maxAttendees"]
        # generate Profile Key based on user ID and Conference
        # ID based on Profile key get Conference key from ID
        p_key = ndb.Key(Profile, user_id)
        c_id = Conference.allocate_ids(size=1, parent=p_key)[0]
        c_key = ndb.Key(Conference, c_id, parent=p_key)
        data['key'] = c_key
        data['organizerUserId'] = request.organizerUserId = user_id

        # create Conference, send email to organizer confirming
        # creation of Conference & return (modified) ConferenceForm
        Conference(**data).put()
        taskqueue.add(params={'email': user.email(),
            'conferenceInfo': repr(request)},
            url='/tasks/send_confirmation_email'
        )
        return request

    @ndb.transactional()
    def _updateConferenceObject(self, request):
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        # copy ConferenceForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in request.all_fields()}

        # update existing conference
        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()
        # check that conference exists
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % request.websafeConferenceKey)

        # check that user is owner
        if user_id != conf.organizerUserId:
            raise endpoints.ForbiddenException(
                'Only the owner can update the conference.')

        # Not getting all the fields, so don't create a new object; just
        # copy relevant fields from ConferenceForm to Conference object
        for field in request.all_fields():
            data = getattr(request, field.name)
            # only copy fields where we get data
            if data not in (None, []):
                # special handling for dates (convert string to Date)
                if field.name in ('startDate', 'endDate'):
                    data = datetime.strptime(data, "%Y-%m-%d").date()
                    if field.name == 'startDate':
                        conf.month = data.month
                # write to Conference object
                setattr(conf, field.name, data)
        conf.put()
        prof = ndb.Key(Profile, user_id).get()
        return self._copyConferenceToForm(conf, getattr(prof, 'displayName'))

    @endpoints.method(ConferenceForm, ConferenceForm, path='conference',
            http_method='POST', name='createConference')
    def createConference(self, request):
        """Create new conference."""
        return self._createConferenceObject(request)

    @endpoints.method(CONF_POST_REQUEST, ConferenceForm,
            path='conference/{websafeConferenceKey}',
            http_method='PUT', name='updateConference')
    def updateConference(self, request):
        """Update conference w/provided fields & return w/updated info."""
        return self._updateConferenceObject(request)

    @endpoints.method(CONF_GET_REQUEST, ConferenceForm,
            path='conference/{websafeConferenceKey}',
            http_method='GET', name='getConference')
    def getConference(self, request):
        """Return requested conference (by websafeConferenceKey)."""
        # get Conference object from request; bail if not found
        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % request.websafeConferenceKey)
        prof = conf.key.parent().get()
        # return ConferenceForm
        return self._copyConferenceToForm(conf, getattr(prof, 'displayName'))

    @endpoints.method(message_types.VoidMessage, ConferenceForms,
            path='getConferencesCreated',
            http_method='POST', name='getConferencesCreated')
    def getConferencesCreated(self, request):
        """Return conferences created by user."""
        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        # create ancestor query for all key matches for this user
        confs = Conference.query(ancestor=ndb.Key(Profile, user_id))
        prof = ndb.Key(Profile, user_id).get()
        # return set of ConferenceForm objects per Conference
        return ConferenceForms(
            items=[self._copyConferenceToForm(conf, getattr(prof, 'displayName')) for conf in confs]
        )

    def _getQuery(self, request):
        """Return formatted query from the submitted filters."""
        q = Conference.query()
        inequality_filter, filters = self._formatFilters(request.filters)

        # If exists, sort on inequality filter first
        if not inequality_filter:
            q = q.order(Conference.name)
        else:
            q = q.order(ndb.GenericProperty(inequality_filter))
            q = q.order(Conference.name)

        for filtr in filters:
            if filtr["field"] in ["month", "maxAttendees"]:
                filtr["value"] = int(filtr["value"])
            formatted_query = ndb.query.FilterNode(filtr["field"], filtr["operator"], filtr["value"])
            q = q.filter(formatted_query)
        return q

    def _formatFilters(self, filters):
        """Parse, check validity and format user supplied filters."""
        formatted_filters = []
        inequality_field = None

        for f in filters:
            filtr = {field.name: getattr(f, field.name) for field in f.all_fields()}

            try:
                filtr["field"] = FIELDS[filtr["field"]]
                filtr["operator"] = OPERATORS[filtr["operator"]]
            except KeyError:
                raise endpoints.BadRequestException("Filter contains invalid field or operator.")

            # Every operation except "=" is an inequality
            if filtr["operator"] != "=":
                # check if inequality operation has been used in previous filters
                # disallow the filter if inequality was performed on a different field before
                # track the field on which the inequality operation is performed
                if inequality_field and inequality_field != filtr["field"]:
                    raise endpoints.BadRequestException("Inequality filter is allowed on only one field.")
                else:
                    inequality_field = filtr["field"]

            formatted_filters.append(filtr)
        return (inequality_field, formatted_filters)

    @endpoints.method(ConferenceQueryForms, ConferenceForms,
            path='queryConferences',
            http_method='POST',
            name='queryConferences')
    def queryConferences(self, request):
        """Query for conferences."""
        conferences = self._getQuery(request)

        # need to fetch organiser displayName from profiles
        # get all keys and use get_multi for speed
        organisers = [(ndb.Key(Profile, conf.organizerUserId)) for conf in conferences]
        profiles = ndb.get_multi(organisers)

        # put display names in a dict for easier fetching
        names = {}
        for profile in profiles:
            names[profile.key.id()] = profile.displayName

        # return individual ConferenceForm object per Conference
        return ConferenceForms(
                items=[self._copyConferenceToForm(conf, names[conf.organizerUserId]) for conf in \
                conferences]
        )

# - - - Sessions - - -  - - - - - - - - - - - - - - - - - - -

    def _copySessionToForm(self, sess):
        """Copy relevant fields from Session to SessionForm."""
        sf = SessionForm()
        for field in sf.all_fields():
            if hasattr(sess, field.name):
                # convert t-shirt string to Enum; just copy others
                if field.name == 'typeOfSession':
                    setattr(sf, field.name, getattr(SessionType, getattr(
                        sess, field.name)))
                # convert date to date string;
                elif field.name == 'date':
                    setattr(sf, field.name, str(getattr(sess, field.name)))
                # convert startTime to time string;
                elif field.name.endswith('Time'):
                    setattr(sf, field.name, str(getattr(sess, field.name)))
                # convert startTime to time string;
                elif field.name == 'duration':
                    setattr(sf, field.name, str(getattr(sess, field.name)))
                # convert list of Speaker keys to list of strings:
                elif field.name == 'speaker':
                    setattr(sf, field.name,
                            [str(s.get().name) for s in sess.speaker])
                # just copy other fields
                else:
                    setattr(sf, field.name, getattr(sess, field.name))
            elif field.name == "websafeKey":
                setattr(sf, field.name, sess.key.urlsafe())
            elif field.name == "websafeConfKey":
                setattr(sf, field.name, sess.key.parent().urlsafe())
        sf.check_initialized()
        return sf

    def _createSessionObject(self, request):
        """Create or update Session object, returning SessionForm/request."""
        # Check if user is logged in
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')
        user_id = getUserId(user)

        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()

        # Check that conference exists
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s'
                % request.websafeConferenceKey)

        if user_id != conf.organizerUserId:
            raise endpoints.ForbiddenException(
                'The conference can only be updated by the owner.')

        if not request.name:
            raise endpoints.BadRequestException("Session 'name' field \
                required")

        # Copy SessionForm/ProtoRPC Message into dict
        data = {field.name: getattr(request, field.name) for field in
                request.all_fields()}
        del data['websafeKey']
        del data['websafeConferenceKey']

        # Add default values if values are missing
        for df in DEFAULTS_SESSION:
            if data[df] in (None, []):
                data[df] = DEFAULTS_SESSION[df]
                setattr(request, df, DEFAULTS_SESSION[df])

        # Convertions
        if data['typeOfSession']:
            data['typeOfSession'] = str(data['typeOfSession'])
        if data['date']:
            data['date'] = datetime.strptime(data['date'][:10],"%Y-%m-%d").date()
        if data['startTime']:
            data['startTime'] = datetime.strptime(data['startTime'][:5],"%H:%M").time()
        if data['duration']:
            data['duration'] = datetime.strptime(data['duration'][:5],"%H:%M").time()
        if data['speaker']:
            sess_speakers = []
            for speaker in data['speaker']:
                sess_spkr_key = Speaker.get_or_insert(
                     speaker.lower().strip().replace(" ", "_"),
                     name=speaker).key
                # Add key to sess_speakers
                sess_speakers.append(sess_spkr_key)
            # Replace data['speaker'] with sess_speakers list
            data['speaker'] = sess_speakers

        # Get Conference Key
        c_key = conf.key
        # Allocate new Session ID with Conference key as parent
        s_id = Session.allocate_ids(size=1, parent=c_key)[0]
        # Create a key for for the new Session with conference key as parent
        s_key = ndb.Key(Session, s_id, parent=c_key)
        # Add key to dictionary
        data['key'] = s_key
        # Create Session
        Session(**data).put()
        # get session to copy it back to the form as return
        sess = s_key.get()
        # Add task to queue
        taskqueue.add(params={'c_key_str': c_key.urlsafe()},url='/tasks/check_speaker')

        return self._copySessionToForm(sess)

    def _getConferenceSessions(self, request):
        """Return a conference's sessions"""
        # Convert websafeKey to conference key
        conf = ndb.Key(urlsafe=request.websafeConferenceKey).get()

        # Check if conference exists
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s'
                % request.websafeConferenceKey)
        # Get conference's key
        c_key = conf.key
        # Create an ancestor query for the current user
        sessions = Session.query(ancestor=c_key)
        return sessions

    def _getSpeakerKey(self, request):
        """Return speakers's key"""

        if not request.name:
            raise endpoints.BadRequestException("Speaker 'name' field \
                required")

        # Create a new key
        speaker_key = Speaker().key
        # Get all speakers
        getSpeakers = Speaker.query()
        # Known speakers list
        knownSpeakers = []
        for known in getSpeakers:
            knownSpeakers.append(known.name)
        # Raise an "Not Found"-exception (if speaker doesn't exist)
        if request.name not in knownSpeakers:
            raise endpoints.NotFoundException(
                'No speaker found with name: %s'
                % request.name)
        else:
            # Return speaker's key
            speaker_key = Speaker.query(Speaker.name == request.name).get().key
        return speaker_key

    @endpoints.method(SESSION_GET_REQUEST, SessionForms,
            path='conference/{websafeConferenceKey}/sessions',
            http_method='GET',
            name='getConferenceSessions')
    def getConferenceSessions(self, request):
        """Given a conference, return all sessions"""
        sessions = self._getConferenceSessions(request)
        # Return SessionForms objects
        return SessionForms(
            items=[self._copySessionToForm(sess) for sess in sessions]
        )

    @endpoints.method(SESSION_BY_TYPE_GET_REQUEST, SessionForms,
            path='conference/{websafeConferenceKey}/sessions/byType',
            http_method='GET',
            name='getConferenceSessionsByType')
    def getConferenceSessionsByType(self, request):
        """Given a conference, return all sessions of a specified type (eg lecture, keynote, workshop)"""
        sessions = self._getConferenceSessions(request)
        # Filter by typeOfSession
        sessions = sessions.filter(Session.typeOfSession == str(request.typeOfSession))
        # Return SessionForms objects
        return SessionForms(
            items=[self._copySessionToForm(sess) for sess in sessions]
        )

    @endpoints.method(SpeakerForm, SessionForms,
            path='sessions/bySpeaker',
            http_method='GET',
            name='getSessionsBySpeaker')
    def getSessionsBySpeaker(self, request):
        """Given a speaker return all sessions given by this particular speaker, across all conferences"""
        # Get speaker's key
        speaker_key = self._getSpeakerKey(request)
        # Query all sessions by speaker
        sessions = Session.query(Session.speaker == speaker_key)
        # Return SessionForms objects
        return SessionForms(
            items=[self._copySessionToForm(sess) for sess in sessions]
        )

    @endpoints.method(SESSION_POST_REQUEST, SessionForm,
            path='conference/{websafeConferenceKey}/sessions',
            http_method='POST',
            name='createSession')
    def createSession(self, request):
        """Open only to the organizer of the conference"""
        return self._createSessionObject(request)

# - - - Wishlist (Task 2) - - - - - - - - - - - - - - - - - - -    

    @endpoints.method(WISHLIST_POST_REQUEST, BooleanMessage,
            path='wishlist',
            http_method='POST',
            name='addSessionToWishlist')
    @ndb.transactional
    def addSessionToWishlist(self, request):
        """Adds the session to the user's wishlist"""
        exists = None
        # Get user's profile
        prof = self._getProfileFromUser()

        # Check if session exists (using the key)
        wssk = request.websafeSessionKey
        sess = ndb.Key(urlsafe=wssk).get()
        if not sess:
            raise endpoints.NotFoundException(
                'No session found with key: %s' % wssk)

        # Check if session exists
        if wssk in prof.sessionsKeysWishlist:
            raise ConflictException(
                "Already on your wishlist")

        # Add the session in user's wishlist
        prof.sessionsKeysWishlist.append(wssk)
        exists = True

        # Puts session to datastore
        prof.put()
        return BooleanMessage(data=exists)

    @endpoints.method(message_types.VoidMessage, SessionForms,
            path='wishlist',
            http_method='GET',
            name='getSessionsInWishlist')
    def getSessionsInWishlist(self, request):
        """Query for all the sessions in a conference that the user is interested in"""
        # Get user's profile
        prof = self._getProfileFromUser()

        # Get session keys from profile
        session_keys = [ndb.Key(urlsafe=wssk) for wssk in prof.sessionsKeysWishlist]

        # Get sessions from datastore using get_multi
        # in order to get all keys at once
        sessions = ndb.get_multi(session_keys)

        return SessionForms(items=[self._copySessionToForm(sess) for sess in sessions])

    @endpoints.method(WISHLIST_POST_REQUEST, BooleanMessage,
            path='d_wishlist',
            http_method='POST',
            name='deleteSessionInWishlist')
    def deleteSessionInWishlist(self, request):
        """Removes the session from the users list of sessions they are interested in attending"""
        exists = None
        # Get user's profile
        prof = self._getProfileFromUser()

        # Get the session and its keys
        sess_key = request.websafeSessionKey
        sess = ndb.Key(urlsafe=sess_key).get()
        conf_key = sess.key.parent().urlsafe()

        # Check conference
        conf = ndb.Key(urlsafe=conf_key).get()
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with session key: %s' % sess_key)

        # Check if the session exists
        if not sess_key in prof.sessionsKeysWishlist:
            raise ConflictException(
                "This session doesn't exist in your wishlist")
        else:
            # Delete the session
            prof.sessionsKeysWishlist.remove(sess_key)
            prof.put()
            exists = True

        return BooleanMessage(data=exists)

# - - - Additional queries (Task 3) - - - - - - - - - - - - - - - - - - -
    
    @endpoints.method(
            SESSION_BY_SPK_GET_REQUEST, SessionForms,
            path='conference/{websafeConferenceKey}/sessions/bySpeaker',
            http_method='POST', name='getConferenceSessionsBySpeaker')
    def getSessBySpeaker(self, request):
        """Return a speaker's sessions"""
        # Get conferences of a session
        conference_sessions = self._getConferenceSessions(request)

        # Get speaker's key
        speaker_key = self._getSpeakerKey(request)

        # Filter sessions by speaker
        speaker_sessions = conference_sessions.filter(Session.speaker == speaker_key)

        return SessionForms(
            items=[self._copySessionToForm(sess) for sess in speaker_sessions]
        )

    @endpoints.method(CONF_BY_CITY_REQUEST, ConferenceForms,
            path='conference/byCity/{city}',
            http_method='GET',
            name='getConferencesInCity')
    def getConferencesInCity(self, request):
        """Returns all conferences by their city"""
        # Throw an error if city name is not given
        if not request.city:
            raise endpoints.BadRequestException("Conference 'city' field \
                required")

        # Get all conferences filtered by their city and ordered by name
        conferences_in_city = Conference.query().filter(Conference.city == request.city).order(Conference.name)

        return ConferenceForms(
            items=[self._copyConferenceToForm(conf, "") for conf in conferences_in_city]
        )

# - - - Task 4 - - - - - - - - - - - - - - - - - - -

    @endpoints.method(CONF_GET_REQUEST, StringMessage,
            path='conference/featured',
            http_method='GET',
            name='getFeaturedSpeaker')
    def getFeaturedSpeaker(self, request):
        """Return featured speaker"""
        # Check if if conference exist
        wsck = request.websafeConferenceKey
        conf = ndb.Key(urlsafe=wsck).get()

        if not conf:
            raise endpoints.NotFoundException('No conference found with key: %s' % wsck)

        MEMCACHE_CONFERENCE_KEY = "FEATURED:%s" % wsck
        return StringMessage(data=memcache.get(MEMCACHE_CONFERENCE_KEY) or "There are no featured speakers.")

# - - - Profile objects - - - - - - - - - - - - - - - - - - -

    def _copyProfileToForm(self, prof):
        """Copy relevant fields from Profile to ProfileForm."""
        # copy relevant fields from Profile to ProfileForm
        pf = ProfileForm()
        for field in pf.all_fields():
            if hasattr(prof, field.name):
                # convert t-shirt string to Enum; just copy others
                if field.name == 'teeShirtSize':
                    setattr(pf, field.name, getattr(TeeShirtSize, getattr(prof, field.name)))
                else:
                    setattr(pf, field.name, getattr(prof, field.name))
        pf.check_initialized()
        return pf

    def _getProfileFromUser(self):
        """Return user Profile from datastore, creating new one if non-existent."""
        # make sure user is authed
        user = endpoints.get_current_user()
        if not user:
            raise endpoints.UnauthorizedException('Authorization required')

        # get Profile from datastore
        user_id = getUserId(user)
        p_key = ndb.Key(Profile, user_id)
        profile = p_key.get()
        # create new Profile if not there
        if not profile:
            profile = Profile(
                key = p_key,
                displayName = user.nickname(),
                mainEmail= user.email(),
                teeShirtSize = str(TeeShirtSize.NOT_SPECIFIED),
            )
            profile.put()

        return profile      # return Profile

    def _doProfile(self, save_request=None):
        """Get user Profile and return to user, possibly updating it first."""
        # get user Profile
        prof = self._getProfileFromUser()

        # if saveProfile(), process user-modifyable fields
        if save_request:
            for field in ('displayName', 'teeShirtSize'):
                if hasattr(save_request, field):
                    val = getattr(save_request, field)
                    if val:
                        setattr(prof, field, str(val))
                        #if field == 'teeShirtSize':
                        #    setattr(prof, field, str(val).upper())
                        #else:
                        #    setattr(prof, field, val)
                        prof.put()

        # return ProfileForm
        return self._copyProfileToForm(prof)

    @endpoints.method(message_types.VoidMessage, ProfileForm,
            path='profile', http_method='GET', name='getProfile')
    def getProfile(self, request):
        """Return user profile."""
        return self._doProfile()

    @endpoints.method(ProfileMiniForm, ProfileForm,
            path='profile', http_method='POST', name='saveProfile')
    def saveProfile(self, request):
        """Update & return user profile."""
        return self._doProfile(request)

# - - - Announcements - - - - - - - - - - - - - - - - - - - -

    @staticmethod
    def _cacheAnnouncement():
        """Create Announcement & assign to memcache; used by
        memcache cron job & putAnnouncement().
        """
        confs = Conference.query(ndb.AND(
            Conference.seatsAvailable <= 5,
            Conference.seatsAvailable > 0)
        ).fetch(projection=[Conference.name])

        if confs:
            # If there are almost sold out conferences,
            # format announcement and set it in memcache
            announcement = ANNOUNCEMENT_TPL % (
                ', '.join(conf.name for conf in confs))
            memcache.set(MEMCACHE_ANNOUNCEMENTS_KEY, announcement)
        else:
            # If there are no sold out conferences,
            # delete the memcache announcements entry
            announcement = ""
            memcache.delete(MEMCACHE_ANNOUNCEMENTS_KEY)

        return announcement

    @endpoints.method(message_types.VoidMessage, StringMessage,
            path='conference/announcement/get',
            http_method='GET', name='getAnnouncement')
    def getAnnouncement(self, request):
        """Return Announcement from memcache."""
        return StringMessage(data=memcache.get(MEMCACHE_ANNOUNCEMENTS_KEY) or "")

# - - - Registration - - - - - - - - - - - - - - - - - - - -

    @ndb.transactional(xg=True)
    def _conferenceRegistration(self, request, reg=True):
        """Register or unregister user for selected conference."""
        retval = None
        prof = self._getProfileFromUser() # get user Profile

        # check if conf exists given websafeConfKey
        # get conference; check that it exists
        wsck = request.websafeConferenceKey
        conf = ndb.Key(urlsafe=wsck).get()
        if not conf:
            raise endpoints.NotFoundException(
                'No conference found with key: %s' % wsck)

        # register
        if reg:
            # check if user already registered otherwise add
            if wsck in prof.conferenceKeysToAttend:
                raise ConflictException(
                    "You have already registered for this conference")

            # check if seats avail
            if conf.seatsAvailable <= 0:
                raise ConflictException(
                    "There are no seats available.")

            # register user, take away one seat
            prof.conferenceKeysToAttend.append(wsck)
            conf.seatsAvailable -= 1
            retval = True

        # unregister
        else:
            # check if user already registered
            if wsck in prof.conferenceKeysToAttend:

                # unregister user, add back one seat
                prof.conferenceKeysToAttend.remove(wsck)
                conf.seatsAvailable += 1
                retval = True
            else:
                retval = False

        # write things back to the datastore & return
        prof.put()
        conf.put()
        return BooleanMessage(data=retval)

    @endpoints.method(message_types.VoidMessage, ConferenceForms,
            path='conferences/attending',
            http_method='GET', name='getConferencesToAttend')
    def getConferencesToAttend(self, request):
        """Get list of conferences that user has registered for."""
        prof = self._getProfileFromUser() # get user Profile
        conf_keys = [ndb.Key(urlsafe=wsck) for wsck in prof.conferenceKeysToAttend]
        conferences = ndb.get_multi(conf_keys)

        # get organizers
        organisers = [ndb.Key(Profile, conf.organizerUserId) for conf in conferences]
        profiles = ndb.get_multi(organisers)

        # put display names in a dict for easier fetching
        names = {}
        for profile in profiles:
            names[profile.key.id()] = profile.displayName

        # return set of ConferenceForm objects per Conference
        return ConferenceForms(items=[self._copyConferenceToForm(conf, names[conf.organizerUserId])\
         for conf in conferences]
        )

    @endpoints.method(CONF_GET_REQUEST, BooleanMessage,
            path='conference/{websafeConferenceKey}',
            http_method='POST', name='registerForConference')
    def registerForConference(self, request):
        """Register user for selected conference."""
        return self._conferenceRegistration(request)

    @endpoints.method(CONF_GET_REQUEST, BooleanMessage,
            path='conference/{websafeConferenceKey}',
            http_method='DELETE', name='unregisterFromConference')
    def unregisterFromConference(self, request):
        """Unregister user for selected conference."""
        return self._conferenceRegistration(request, reg=False)

    @endpoints.method(message_types.VoidMessage, ConferenceForms,
            path='filterPlayground',
            http_method='GET', name='filterPlayground')
    def filterPlayground(self, request):
        """Filter Playground"""
        q = Conference.query()
        # field = "city"
        # operator = "="
        # value = "London"
        # f = ndb.query.FilterNode(field, operator, value)
        # q = q.filter(f)
        q = q.filter(Conference.city=="London")
        q = q.filter(Conference.topics=="Medical Innovations")
        q = q.filter(Conference.month==6)

        return ConferenceForms(
            items=[self._copyConferenceToForm(conf, "") for conf in q]
        )

api = endpoints.api_server([ConferenceApi]) # register API
