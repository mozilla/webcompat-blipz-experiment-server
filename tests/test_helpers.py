#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for helper methods."""

from io import BufferedIOBase
import json
import os
import sys
import unittest

import responses

# Add issue module to import path
sys.path.append(os.path.realpath(os.pardir))
from app import app  # noqa
from app.helpers import get_screenshot  # noqa
from app.helpers import has_valid_screenshot  # noqa
from app.helpers import valid_issue_request  # noqa

GIF = 'data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACwAAAAAAQABAAACAkQBADs='
PNG = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVQYV2NgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII='  # noqa
JPEG = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD/2wBDAAIBAQIBAQICAgICAgICAwUDAwMDAwYEBAMFBwYHBwcGBwcICQsJCAgKCAcHCg0KCgsMDAwMBwkODw0MDgsMDAz/2wBDAQICAgMDAwYDAwYMCAcIDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMDAz/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD9/KKKKAP/2Q=='  # noqa


class TesHelpers(unittest.TestCase):
    """Module for testing the helpers module."""

    def setUp(self):
        """Set up."""
        app.config['TESTING'] = True
        self.app = app.test_client()

    def tearDown(self):
        """Tear down."""
        pass

    def test_valid_issue_request(self):
        # Note, we're just testing truthiness, and not exhaustively.
        self.assertTrue(valid_issue_request("cool", "hi"))
        self.assertFalse(valid_issue_request("cool", ""))
        self.assertFalse(valid_issue_request("", "hi"))

    def test_has_valid_screenshot(self):
        self.assertTrue(has_valid_screenshot(JPEG))
        self.assertTrue(has_valid_screenshot(PNG))
        self.assertFalse(has_valid_screenshot(GIF))
        self.assertFalse(has_valid_screenshot(None))

    def test_get_screenshot(self):
        data, type_ = get_screenshot(JPEG)
        self.assertTrue(isinstance(data, BufferedIOBase))
        self.assertIn('jpeg', type_)
        data, type_ = get_screenshot(PNG)
        self.assertTrue(isinstance(data, BufferedIOBase))
        self.assertIn('png', type_)
        self.assertTrue(isinstance(data, BufferedIOBase))
        data, type_ = get_screenshot(GIF)
        self.assertIs(type_, None)
