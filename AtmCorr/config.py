#!/usr/bin/env python
"""An example config.py file."""


import ee
import os.path

# The service account email address authorized by your Google contact.
# Set up a service account as described in the README.
EE_ACCOUNT = 'n-khanal@appspot.gserviceaccount.com'

# The private key associated with your service account in JSON format.
EE_PRIVATE_KEY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)),'nkhanal-default4bc5.json')

EE_CREDENTIALS = ee.ServiceAccountCredentials(EE_ACCOUNT, EE_PRIVATE_KEY_FILE)
