# -*- coding: utf-8 -*-

"""Classes and methods for interacting with Feedly."""

__author__ = "Elena Caceres"
__credits__ = ["https://github.com/uraxy/qiidly", "https://github.com/zgw21cn/FeedlyClient"]
__email__ = "elcaceres@gmail.com"

import feedparser
import requests
import json


class FeedlyClient(object):
    """Used to read and interact with the feedly website"""
   
    
    def __init__(self, **options):
        """
        Initialize a FeedlyReader object with the developer access token and the feedly URL. Also sets info URLs.

        """
        
        self.access_token = options.get("access_token", None)
        self.base_url = options.get("base_url", "https://cloud.feedly.com")
        
        self.info_urls = {
            "preferences": "/v3/preferences",
            "categories": "/v3/categories",
            "topics": "/v3/topics",
            "markers": "/v3/markers",
            "tags": "/v3/tags",
            "subscriptions": "/v3/subscriptions",
            "ids": "/v3/streams/ids",
            "contents": "/v3/streams/contents",
            "entries": "/v3/entries",
            "entries_from_ids": "/v3/entries/.mget",
            "token" : "/v3/auth/token",
            "feeds" : "/v3/feeds",

        }

    def _headers(self):
        """
        Get headers to interact with the feedly api
        
        Returns
        -------
        dict
            dict containing content type and authorization formatted with the OAuth access token provided at initialization

        """
        return {
            'content-type': 'application/json',
            'Authorization': 'OAuth ' + self.access_token
        }
    
    
    def get_user_subscriptions(self):
        """
        Get the user’s subscriptions.
        https://developer.feedly.com/v3/subscriptions/#get-the-users-subscriptions
        GET /v3/subscriptions
        (Authorization is required)
        
        Returns
        -------
        json
            dict containing list of subscriptions
        """
        res = requests.get(url=self.base_url + self.info_urls["subscriptions"], headers=self._headers())
        return res.json()      
    
    
    def get_entries_from_ids(self, entryIds):
        """
        Get the entryIds for a stream with options for a date since last pull and max IDs.
        https://developer.feedly.com/v3/entries/
        POST /v3/entries/.mget

        Parameters
        ----------
        entryIds : list of str
            list of entryIDs (ex. results from get_entry_ids()["id"]

        Returns
        -------
        json
            dict containing list of entries under ["ids"] and any continuation stored in ["continuation"]
        """
        params = dict(type="entries", entryIds=entryIds)
        res = requests.post(url = self.base_url + self.info_urls["entries_from_ids"], 
                            headers=self._headers(), data=json.dumps(entryIds))
        return res.json()
    
    
    def get_entry_ids(self, streamID, newerThan=None, continuation=None, maxcount=1000, unreadOnly=False):
        """
        Get the entryIds for a stream with options for a date since last pull and max IDs.
        https://developer.feedly.com/v3/streams/#get-the-content-of-a-stream
        GET /v3/streams/ids?streamId=:streamId
        or
        GET /v3/streams/:streamId/ids


        Parameters
        ----------
        streamID : str
            ID for a stream of interest (e.g. result from get_streams())
        newerThan : long, optional
            long (or int) representation of oldest allowable entry in ms (do not use delta time, just standard time)
        continuation : str, optional
            if given, will fetch IDs continuing from the last query without duplicates
        maxcount : int, optional
            maximum number (0, 1e4] of entry IDs to return at one time. If number of entries exceeds maxcount, a continuation identifier is returned in the result under result_name['continuation'].
        unreadOnly : bool, optional
            retrieve only unread entries (default: False)
            
            
        Returns
        -------
        json
            dict containing list of entryIDs under ["ids"] and any continuation stored in ["continuation"]
        """
        
        params = dict(streamId=streamID, count=maxcount)
        if newerThan:
            params["newerThan"] = newerThan
        if continuation:
            params["continuation"] = continuation
        if unreadOnly:
            params["unreadOnly"] = unreadOnly
        res = requests.get(url = self.base_url + self.info_urls["ids"], 
                           headers=self._headers(), params=params)
        return res.json()
    
    
    def get_feed_content(self, streamID, newerThan=None, maxcount=1000, continuation=None, unreadOnly=False):
        """
        Get entries from a feed. This is different from get_entry_ids because it returns the entries instead of just their IDs. However, fewer entries may be retrieved at a time without a continuation.
        
        https://developer.feedly.com/v3/streams/#get-the-content-of-a-stream
        GET /v3/streams/contents?streamId=:streamId
        or 
        GET /v3/streams/:streamId/contents
        Authorization optional
        
        Parameters
        ----------
        streamID : str
            ID for a stream of interest (e.g. result from get_streams())
        newerThan : long, optional
            long (or int) representation of oldest allowable entry in ms (do not use delta time, just standard time)
        continuation : str, optional
            if given, will fetch IDs continuing from the last query without duplicates
        maxcount : int, optional
            maximum number (0, 1000] of entry IDs to return at one time. If number of entries exceeds maxcount, a continuation identifier is returned in the result under result_name['continuation'].
        unreadOnly : bool, optional
            retrieve only unread entries (default: False)
            
        Returns
        -------
        json
            dict containing list of entries under ["ids"] and any continuation stored in ["continuation"]
        
        """
        params = dict(streamId=streamID, count=maxcount)
        if newerThan:
            params["newerThan"] = newerThan
        if continuation:
            params["continuation"] = continuation
        if unreadOnly:
            params["unreadOnly"] = unreadOnly
            
        res = requests.get(url = self.base_url + self.info_urls["contents"], 
                           headers=self._headers(), params=params)
        return res.json()
    
    def mark_articles(self, entryIds, action, xtype="entries"):
        """
        Mark one or multiple articles as the specified action. 
        https://developer.feedly.com/v3/markers/
        POST /v3/markers
        
        Parameters
        ----------
        entryIds : list of str
            list of ID for entries to mark as read (e.g. result from get_entry_ids() as a list)
        
        Returns
        -------
        str
            expected status 200 ok
        
        """
        params = dict(action=action, type=xtype, entryIds=entryIds)
        res = requests.post(url = self.base_url + self.info_urls["markers"], 
                           headers=self._headers(), data=json.dumps(params))
        return res
    
    def mark_articles_read(self, entryIds):
        """
        Wrapper to mark one or multiple articles as read. 

        Parameters
        ----------
        entryIds : list of str
            list of ID for entries to mark as read (e.g. result from get_entry_ids() as a list)
        
        Returns
        -------
        str
            expected status 200 ok
        
        """
        return self.mark_articles(entryIds, "markAsRead", xtype="entries")
  
    def mark_articles_unread(self, entryIds):
        """
        Wrapper to mark one or multiple articles as unread. 

        Parameters
        ----------
        entryIds : list of str
            list of ID for entries to mark as unread (e.g. result from get_entry_ids() as a list)
        
        Returns
        -------
        str
            expected status 200 ok
        
        """
        return self.mark_articles(entryIds, "keepUnread", xtype="entries")
    
    
    def save_articles(self, entryIds):
        """
        Wrapper to mark one or multiple articles as saved for later. 

        Parameters
        ----------
        entryIds : list of str
            list of ID for entries to mark as read (e.g. result from get_entry_ids() as a list)
        
        Returns
        -------
        str
            expected status 200 ok
        
        """
        return self.mark_articles(entryIds, "markAsSaved", xtype="entries")
    
    def unsave_articles(self, entryIds):
        """
        Wrapper to mark one or multiple articles as saved for later. 

        Parameters
        ----------
        entryIds : list of str
            list of ID for entries to mark as read (e.g. result from get_entry_ids() as a list)
        
        Returns
        -------
        str
            expected status 200 ok
        
        """
        return self.mark_articles(entryIds, "markAsUnsaved", xtype="entries")
