#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) - 2011 @rogeliorv
# Based on work by jbc dot develop at gmail dot com

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#===============================================================================
# DOCS
#===============================================================================

"""Leverage influence in your application. Knowing who's important on any given
topic or in a certain situation is a game-changer for many applications

More info:
    http://developer.klout.com/api_gallery

"""

#===============================================================================
# META
#===============================================================================

__version__ = "0.3"
__license__ = "GPL3"
__author__ = "rogeliorv"
__since__ = "0.1"
__date__ = "2011-07-07"


#===============================================================================
# IMPORTS
#===============================================================================

try:
    import simplejson as json
except:
    import json
import urllib
import urllib2
import string
import datetime
import time
from kloutpy_util import make_chunks


#===============================================================================
# CONSTANTS
#===============================================================================

_CMD = string.Template("http://api.klout.com/1/${method}.json?key=${api_key}&${params}")


ERROR_STATUS = {
    # "200: "OK: Success", IS A GOOD STATUS
    202: "Accepted: Your request was accepted and the user was queued for processing.",
    401: "Not Authorized: either you need to provide authentication credentials, or the credentials provided aren't valid.",
    403: "Bad Request: your request is invalid, This is the status code returned if you've exceeded the rate limit or if you are over QPS.",
    404: "Not Found: either you're requesting an invalid URI or the resource in question doesn't exist (ex: no such user in our system).",
    500: "Internal Server Error: we did something wrong.",
    502: "Bad Gateway: returned if Klout is down or being upgraded.",
    503: "Service Unavailable: the Klout servers are up, but are overloaded with requests. Try again later.",
}


#===============================================================================
# CLASS ERROR
#===============================================================================

class KloutError(BaseException):
    def __init__(self, code, msg):
        super(KloutError, self).__init__()
        self.code = code
        self.msg = msg
            
    def __str__(self):
        return repr(self)
    
    def __repr__(self):
        return "%i: %s" % (self.code, self.msg)
    
    
#===============================================================================
# Klout Class
#===============================================================================

class Klout(object):
    
    MAX_API_CALLS = 10000
    KLOUT_MAX_USERS_PER_SCORE_REQUEST = 5
    NO_INFLUENCE = -1
    
    def __init__(self, api_key):
        """Create a new instance of Klout api
        
        @param api_key: the api key (register for one in http://developer.klout.com/)
         
        """
        self._api_key = api_key
    
    def _request(self, method, **params):
        url = _CMD.substitute(api_key=self._api_key,
                              method=method,
                              params=urllib.urlencode(params))
        try:
            data = urllib2.urlopen(url).read()
            data = json.loads(data)
        except urllib2.HTTPError as err:
            msg = err.read() or ERROR_STATUS.get(err.code, err.message)
            raise KloutError(err.code, msg)
        except ValueError:
            msg = "Invalid json data: '%s'" % data
            raise KloutError(0, msg)
        else:
            status = data.pop("status") 
            if status in ERROR_STATUS:
                msg = ERROR_STATUS.get(status, "Unknow Error") 
                raise KloutError(status, msg)
            return data
    
    def score(self, users):
        """This method allows you to retrieve a Klout score"""
        if isinstance(users, (list, tuple)):
            users = ",".join(users)
        
        result = self._request("klout", users=users)
        if 'users' not in result:
            error = result.get('body', {}).get('error', 'Users %s not found' % unicode(users))
            raise KloutError(404, error)
        
        return result['users']
        
        print "%s %s" % (unicode(result), unicode(users))
    
    def users_show(self, users):
        """This method allows you to retrieve user objects"""
        if isinstance(users, (list, tuple)):
            users = ",".join(users)
        return self._request("users/show", users=users)["users"]
        
    def users_topics(self, users):
        """This method allows you to retrieve the top 3 topic objects"""
        if isinstance(users, (list, tuple)):
            users = ",".join(users)
        return self._request("users/topics", users=users)["users"]

    def soi_influenced_by(self, users):
        """Returns the top 25 user score pairs that are influenced by the given
        user(s)
        
        """
        if isinstance(users, (list, tuple)):
            users = ",".join(users)
        return self._request("soi/influenced_by", users=users)["users"]

    def soi_influencer_of(self, users):
        """Returns the top 25 user score pairs that are influencers of the given
        user(s).
        
        """
        if isinstance(users, (list, tuple)):
            users = ",".join(users)
        return self._request("soi/influencer_of", users=users)["users"]
    
        def get_reset_time_in_seconds(self):
            return time.time() + self.get_seconds_to_reset()
    
    def get_seconds_to_reset(self):
        '''Klout resets the api calls every day at GMT(UTC). This function
        returns the number of seconds remaining to the reset time'''
        now = datetime.datetime.utcnow()
        today_midnight = datetime.datetime(now.year, now.month, now.day)
        one_day = datetime.timedelta(1)
        tomorrow = today_midnight + one_day
        return (tomorrow - now).total_seconds()
    
    def get_users_influence(self, *screen_names):
        '''This function is aimed to replace the score function, which returns the influence score for 
        the given users.
        
        Score only returns the results for up to five users (since that is the limit of users per request), so
        we divide the screen_names in chunks of that size and make several requests, yielding them as 
        they come.
        
        The return value from this function is a generator with elements of the form:
                {u'kscore': float, u'twitter_screen_name': unicode_string}
                
        score returns 404 if one or more of the elements you asked for does not exist in their db yet. Instead
        this function returns NO_INFLUENCE for a user that does not exist yet
        '''
        grouped = make_chunks(screen_names, self.KLOUT_MAX_USERS_PER_SCORE_REQUEST)
        # Klout limits five users per request for the score
        for group in grouped:
            try:
                for result in self.score(group): yield result                
            except KloutError, e:
                if e.code != 404: raise e
                # There is an unexisting user in this group, try individually to find it
                for user in group: 
                    try:
                        yield self.score(user)[0]
                    except KloutError, e:
                        print "User %s is not a resource in Klout" % user                        
                        if e.code == 404: 
                            yield {u'kscore': self.NO_INFLUENCE, u'twitter_screen_name': user}
                        else:
                            raise e
                        continue
                continue
    
    @classmethod    
    def api_client_from_django_settings(cls):
        '''Utility function for django users'''
        try:
            from django.conf import settings
            return cls(settings.KLOUT_API_KEY)
        except ImportError:
            print "Could not find django. Is it installed in your system?"
        except AttributeError:
            print "Could not find KLOUT_API_KEY in your settings file."
        
                
    
        

#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print __doc__
