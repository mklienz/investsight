# from requests_oauthlib import OAuth2Session
# import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

import os
from dotenv import load_dotenv

# Load environmental variables (for secrets)
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI")

# Backend legacy method
auth = HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
client = BackendApplicationClient(client_id=CLIENT_ID)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url="https://api.sharesight.com/oauth2/token", auth=auth)