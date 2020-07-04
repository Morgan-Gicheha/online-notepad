from configs.auth_config import GITHUB_CONSUMER_KEY,GITHUB_CONSUMER_SECRET
from flask_oauthlib.client import OAuth
from flask import g

oauth = OAuth()

github = oauth.remote_app('github',
    base_url='https://api.github.com',
    request_token_params={'scope': 'user:email'},
    consumer_key=GITHUB_CONSUMER_KEY,
    consumer_secret=GITHUB_CONSUMER_SECRET,
    access_token_method="POST",
    access_token_url="https://github.com/login/oauth/access_token", #what we send the data to in order to get the access token
    authorize_url= "https://github.com/login/oauth/authorize", #where we send the user in the initial request
    request_token_url=None,


)

