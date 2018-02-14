#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `cliently` package."""

import unittest
from cliently import client
import os

# TODO: This hard coding needs to be fixed with a sandbox when doing things for realsies
ACCESS_TOKEN=os.getenv("FEEDLY_ACCESS_TOKEN")
UID = os.getenv("FEEDLY_UID")
BASE_URL = "https://cloud.feedly.com"

VALID_STREAM_ID = os.getenv("FEEDLY_STREAM_ID")
VALID_JOURNAL = os.getenv("FEEDLY_TEST_JOURNAL")
VALID_ENTRY_IDS = os.getenv("FEEDLY_ENTRY_IDS")


class TestCliently(unittest.TestCase):
    """Tests for `cliently` package
    """
    def setUp(self):
        """Set up test fixtures, if any."""
        options = dict(access_token=ACCESS_TOKEN, base_url=BASE_URL)
        self.myclient = client.FeedlyClient(**options)

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_set_access_token(self):
        """Set the access token"""
        self.assertEqual(self.myclient.access_token, ACCESS_TOKEN)
        
    def test_set_base_url(self):
        """Set the base_url"""
        self.assertEqual(self.myclient.base_url, BASE_URL)
        
    def test_get_user_subscriptions(self):
        """Get a valid streamID & Journal name from list of subscriptions"""
        subscriptions = self.myclient.get_user_subscriptions()
        streamIDs = set(i["categories"][0]["id"] for i in subscriptions)
        subscribed_journals = set(i["title"] for i in subscriptions)
        self.assertIn(VALID_JOURNAL, subscribed_journals)
        self.assertIn(VALID_STREAM_ID, streamIDs)
        
    def test_count_get_entry_ids(self):
        """Test getting entry IDs work"""
        # test that count returns the correct number of things
        self.assertEqual(len(self.myclient.get_entry_ids(VALID_STREAM_ID, maxcount=1)["ids"]), 1)
        
    def test_continuation_entry_ids(self):
        """Test continuation works"""
        # test that count returns the correct number of things
        continuation = self.myclient.get_entry_ids(VALID_STREAM_ID, maxcount=1)["continuation"]
        self.assertEqual(len(self.myclient.get_entry_ids(VALID_STREAM_ID, continuation=continuation, maxcount=1)["ids"]), 1)

    def test_mark_read(self):
        self.assertTrue(self.myclient.mark_article_read(VALID_ENTRY_IDS).ok)
        
    def test_get_single_entry_from_id(self):
        """Retrieve a single entry from an entryId"""
        self.assertEqual(self.myclient.get_entries_from_ids(VALID_ENTRY_IDS[0])[0]["id"], VALID_ENTRY_IDS[0])
    
    def test_get_multiple_entries_from_ids(self):
        """Retrieve multiple entries from an entryId"""
        res = [i["id"] for i in self.myclient.get_entries_from_ids(VALID_ENTRY_IDS)]
        self.assertEqual(res, VALID_ENTRY_IDS)