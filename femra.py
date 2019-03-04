import json

import praw
import firebase_admin
from firebase_admin import credentials, firestore
from requests import request

from definitions import Definitions
from redditors import Redditors

class Femra:
    def __init__(self, config):
        cred=credentials.Certificate(config['firebaseConfig'])
        self.db = firestore.client(firebase_admin.initialize_app(cred))
        redditConfig=config['reddit']
        self.reddit=praw.Reddit(
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

        self._definitions_ = Definitions("https://raw.githubusercontent.com/femradebates/femraWebsite/master/src/data/definitions.json")
        self._redditors_ = Redditors(self.db,self.reddit)
    
    @property
    def definitions(self):
        return self._definitions_
    
    @property
    def redditors(self):
        return self._redditors_

femra=None

with open('config.json','r') as configFile:
    femra=Femra(json.load(configFile))

for Def in femra.definitions:
    print(Def)

print(femra.redditors["wazzup987"])