import json

import praw
import firebase_admin
from firebase_admin import credentials
from requests import request

from definitions import Definition, Definitions

class Femra:
    def __init__(self, config):
        cred=credentials.Certificate(config['firebaseConfig'])
        self.db = firebase_admin.initialize_app(cred)
        redditConfig=config['reddit']
        self.reddit=praw.Reddit( Reddit(
            client_id = redditConfig['client_id'],
            client_secret = redditConfig['client_secret'],
            user_agent="{}:{}:{} (by {})".format(
                redditConfig['user_agent']['platform'],
                redditConfig['user_agent']['name'],
                redditConfig['user_agent']['version'],
                redditConfig['user_agent']['author']
            ),
            username = redditConfig["auth"]["username"],
            password = redditConfig["auth"]["password"]
        )
        self.definitions= Definitions("https://raw.githubusercontent.com/femradebates/femraWebsite/master/src/data/definitions.json")
