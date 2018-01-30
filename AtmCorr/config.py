#!/usr/bin/env python
"""An example config.py file."""


import ee
import os.path

EE_ACCOUNT = '<your service account>'

EE_PRIVATE_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'<your service file>')

EE_CREDENTIALS = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)

OAUTH_CLIENT_ID = '<your-client-id>'
OAUTH_CLIENT_SECRET = '<your-client-secret>'
